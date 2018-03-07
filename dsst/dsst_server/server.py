import json
import pickle
import socket

import sys

import os

from common import util, models
from dsst_server import func_read, func_write, tokens
from dsst_server.func_proxy import FunctionProxy
from dsst_server.data_access import sql, sql_func

PORT = 12345
HOST = socket.gethostname()
BUFFER_SIZE = 1024


class DsstServer:
    def __init__(self, config={}):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Created socket')

        self.socket_server.bind((HOST, PORT))
        print('Bound socket to {} on host {}'.format(PORT, HOST))

        # Initialize database
        db_config = config.get('database')
        sql.db.init(db_config.get('db_name'), user=db_config.get('user'), password=db_config.get('password'))
        sql_func.create_tables()
        print('Database initialized ({})'.format(sql.db.database))

        # Load access tokens and map them to their allowed methods
        read_actions = util.list_class_methods(func_read.ReadFunctions)
        write_actions = util.list_class_methods(func_write.WriteFunctions)
        parm_access = {
            'r': read_actions,
            'rw': read_actions + write_actions
        }
        self.tokens = {token: parm_access[perms] for token, perms in tokens.TOKENS}
        print('Loaded auth tokens: {}'.format(self.tokens.keys()))

    def run(self):
        self.socket_server.listen(5)
        print('Socket is listening')

        while True:
            client, address = self.socket_server.accept()
            try:
                print('Connection from {}'.format(address))
                data = util.recv_msg(client)
                request = pickle.loads(data)
                print('Request: {}'.format(request))
                # Validate auth token in request
                token = request.get('auth_token')
                if token not in self.tokens:
                    util.send_msg(client, pickle.dumps({'success': False, 'message': 'Auth token invalid'}))
                    print('Rejected request from {}. Auth token invalid ({})'.format(address, token))
                    continue
                # Check read functions
                action_name = request.get('action')
                if action_name in self.tokens[token]:
                    action = getattr(FunctionProxy, action_name)
                    try:
                        value = action(request.get('args'))
                    except Exception as e:
                        response = {'success': False, 'message': 'Exception was thrown on server.\n{}'.format(e)}
                        util.send_msg(client, pickle.dumps(response))
                        raise
                    response = {'success': True, 'data': value}
                    util.send_msg(client, pickle.dumps(response))
                    continue
                else:
                    msg = 'Action does not exist on server ({})'.format(request.get('action'))
                    util.send_msg(client, pickle.dumps({'success': False, 'message': msg}))
            except Exception as e:
                print(e)
            finally:
                client.close()
                print('Connection to client closed')


def load_config(config_path: str) -> dict:
    with open(config_path) as config_file:
        return json.load(config_file)


def main():
    config = os.path.join(os.path.expanduser('~'), '.config', 'dsst', 'server.json')
    server = DsstServer(load_config(config))
    try:
        server.run()
    except KeyboardInterrupt:
        print('Server stopped')
        server.socket_server.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
