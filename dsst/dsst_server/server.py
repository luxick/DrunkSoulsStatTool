import pickle
import socket

import sys

import os

from common import util, models
from dsst_server import read_functions, write_functions
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

        self.read_actions = util.list_class_methods(read_functions.ReadFunctions)
        self.write_actions = util.list_class_methods(write_functions.WriteFunctions)
        sql.db.init('dsst', user='dsst', password='dsst')

        self.key_access = {'a': self.read_actions,
                           'b': self.read_actions + self.write_actions}

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
                # Validate auth key in request
                key = request.get('auth_key')
                if key not in self.key_access:
                    util.send_msg(client, pickle.dumps({'success': False, 'message': 'Auth Key invalid'}))
                    print(f'Rejected request from {address}. Auth key invalid ({key})')
                    continue
                # Check read functions
                action_name = request.get('action')
                if action_name in self.key_access[key]:
                    action = getattr(FunctionProxy, action_name)
                    value = action(request.get('args'))
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
