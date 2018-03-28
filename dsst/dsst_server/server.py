import json
import pickle
import socket
import sys
import os
import logging
from logging.config import dictConfig

from common import util
from dsst_server import auth
from dsst_server.func_proxy import FunctionProxy
from dsst_server.data_access import sql, sql_func
from dsst_server.config import DEFAULT_CONFIG


class DsstServer:
    def __init__(self, config):
        # Initialize the logger
        try:
            logger_dict = config.get('logging')
            logfile = os.path.join(os.path.expanduser("~"), '.config', 'dsst', 'server.log')
            logger_dict.get('handlers').get('logfile')['filename'] = logfile
            dictConfig(logger_dict)
        except Exception as e:
            print(e)
            sys.exit(1)
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info('Created socket')
        server_conf = config.get('server')
        self.socket_server.bind(('', server_conf.get('port')))
        logging.info('Bound socket to port {}'.format(server_conf.get('port')))

        # Initialize database
        db_config = config.get('database')
        sql.db.init(db_config.get('db_name'), user=db_config.get('user'), password=db_config.get('password'))
        sql_func.create_tables()
        logging.info('Database initialized ({})'.format(sql.db.database))

        # Load access tokens
        auth.READ_TOKENS = config.get('tokens').get('readonly')
        auth.WRITE_TOKENS = config.get('tokens').get('readwrite')
        logging.info('Auth tokens loaded')

    def run(self):
        self.socket_server.listen(5)
        logging.info('Socket is listening')

        while True:
            client, address = self.socket_server.accept()
            try:
                logging.info('Connection from {}'.format(address))
                data = util.recv_msg(client)
                request = pickle.loads(data)
                logging.info('Request: {}'.format(request))
                # Get requested function from function proxy
                action_name = request.get('action')
                action = getattr(FunctionProxy, action_name)
                # Execute requested function
                value = action(request.get('auth_token'), *request.get('args'))
                # Send results back to client
                response = {'success': True, 'data': value}
                util.send_msg(client, pickle.dumps(response))
                logging.info('Operation executed successfully')
            except auth.AuthenticationError as e:
                logging.error(e.get_response())
                response = e.get_response()
                util.send_msg(client, pickle.dumps(response))
            except Exception as e:
                logging.error('Exception was thrown: ' + str(e))
                response = {'success': False, 'message': 'Exception was thrown on server.'}
                util.send_msg(client, pickle.dumps(response))
            finally:
                client.close()
                logging.info('Connection to client closed')


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
        logging.error('No server config file found.\n'
                      'Copied default config to "{}"\n'
                      'Please edit file before starting server.'
                      .format(config))
        sys.exit(0)
    server = DsstServer(load_config(config))
    try:
        server.run()
    except KeyboardInterrupt:
        logging.info('Server stopped')
        server.socket_server.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
