import json
import pickle
import socket
import sys
import os

from common import util, models
from dsst_server import func_read, func_write, auth
from dsst_server.func_proxy import FunctionProxy
from dsst_server.data_access import sql, sql_func
from dsst_server.config import DEFAULT_CONFIG


class DsstServer:
    def __init__(self, config):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Created socket')
        server_conf = config.get('server')
        self.socket_server.bind(('', server_conf.get('port')))
        print('Bound socket to port {}'.format(server_conf.get('port')))

        # Initialize database
        db_config = config.get('database')
        sql.db.init(db_config.get('db_name'), user=db_config.get('user'), password=db_config.get('password'))
        sql_func.create_tables()
        print('Database initialized ({})'.format(sql.db.database))

        # Load access tokens
        auth.READ_TOKENS = config.get('tokens').get('readonly')
        auth.WRITE_TOKENS = config.get('tokens').get('readwrite')
        print('Auth tokens loaded')

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
                # Get requested function from function proxy
                action_name = request.get('action')
                action = getattr(FunctionProxy, action_name)
                try:
                    value = action(request.get('auth_token'), *request.get('args'))
                except auth.AuthenticationError as e:
                    response = e.get_response()
                    util.send_msg(client, pickle.dumps(response))
                    raise
                except Exception as e:
                    response = {'success': False, 'message': 'Exception was thrown on server.\n{}'.format(e)}
                    util.send_msg(client, pickle.dumps(response))
                    raise
                response = {'success': True, 'data': value}
                util.send_msg(client, pickle.dumps(response))
            except Exception as e:
                print('Exception: ' + str(e))
            finally:
                client.close()
                print('Connection to client closed')


def load_config(config_path: str) -> dict:
    with open(config_path) as config_file:
        return json.load(config_file)


def save_config(config: dict, config_path: str):
    path = os.path.dirname(config_path)
    if not os.path.isdir(path):
        os.mkdir(path)
    with open(config_path, 'wb') as file:
        file.write(json.dumps(config, sort_keys=True, indent=4, separators=(',', ': ')).encode('utf-8'))


def main():
    config = os.path.join(os.path.expanduser('~'), '.config', 'dsst', 'server.json')
    if not os.path.isfile(config):
        save_config(DEFAULT_CONFIG, config)
        print('No server config file found.\nCopied default config to "{}"\nPlease edit file before starting server.'
              .format(config))
        sys.exit(0)
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
