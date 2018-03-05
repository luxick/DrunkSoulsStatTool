import pickle
import socket

import sys

import os

from common import util, models
from dsst_server import read_functions, write_functions, tokens
from dsst_server.func_proxy import FunctionProxy
from dsst_server.data_access import sql

PORT = 12345
HOST = socket.gethostname()
BUFFER_SIZE = 1024


class DsstServer:
    def __init__(self):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Created socket')

        self.socket_server.bind((HOST, PORT))
        print(f'Bound socket to {PORT} on host {HOST}')

        # Initialize database
        sql.db.init('dsst', user='dsst', password='dsst')
        print(f'Database initialized ({sql.db.database})')

        # Load access tokens and map them to their allowed methods
        read_actions = util.list_class_methods(read_functions.ReadFunctions)
        write_actions = util.list_class_methods(write_functions.WriteFunctions)
        parm_access = {
            'r': read_actions,
            'rw': read_actions + write_actions
        }
        self.tokens = {token: parm_access[perms] for token, perms in tokens.TOKENS}
        print(f'Loaded auth tokens: {self.tokens.keys()}')

    def run(self):
        self.socket_server.listen(5)
        print('Socket is listening')

        while True:
            client, address = self.socket_server.accept()
            try:
                print(f'Connection from {address}')
                data = util.recv_msg(client)
                request = pickle.loads(data)
                print(f'Request: {request}')
                # Validate auth token in request
                token = request.get('auth_token')
                if token not in self.tokens:
                    util.send_msg(client, pickle.dumps({'success': False, 'message': 'Auth token invalid'}))
                    print(f'Rejected request from {address}. Auth token invalid ({token})')
                    continue
                # Check read functions
                action_name = request.get('action')
                if action_name in self.tokens[token]:
                    action = getattr(FunctionProxy, action_name)
                    try:
                        value = action(request.get('args'))
                    except Exception as e:
                        response = {'success': False, 'message': f'Exception was thrown on server.\n{e}'}
                        util.send_msg(client, pickle.dumps(response))
                        raise
                    response = {'success': True, 'data': value}
                    util.send_msg(client, pickle.dumps(response))
                    continue
                else:
                    msg = f'Action does not exist on server ({request.get("action")})'
                    util.send_msg(client, pickle.dumps({'success': False, 'message': msg}))
            except Exception as e:
                print(e)
            finally:
                client.close()
                print('Connection to client closed')


if __name__ == '__main__':
    server = DsstServer()
    try:
        server.run()
    except KeyboardInterrupt:
        print('Server stopped')
        server.socket_server.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
