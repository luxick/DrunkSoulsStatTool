import pprint
import socket
from common import util, models
try:
    import cPickle as pickle
except ImportError:
    import pickle


class Access:
    def __init__(self, connection):
        self.host = connection.get('host')
        self.port = connection.get('port')
        self.buffer = connection.get('buffer_size')
        self.auth_key = connection.get('auth_key')
        self.socket = socket.socket()

    def send_request(self, action: str, *args):
        request = {'auth_key': self.auth_key,
                   'action': action,
                   'args': args}
        request = pickle.dumps(request)
        try:
            self.socket.connect((self.host, self.port))
            util.send_msg(self.socket, request)
            response = util.recv_msg(self.socket)
            response = pickle.loads(response)
            if not response.get('success'):
                raise Exception(response.get('message'))
        finally:
            self.socket.close()
        return response.get('data')

if __name__ == '__main__':
    access = Access({'host': 'europa', 'port': 12345, 'buffer_size': 1024, 'auth_key': 'a'})
    action = 'load_seasons'
    response = access.send_request(action)
    pp = pprint.PrettyPrinter(indent=1)
    for s in response:
        pp.pprint(s.__dict__)
