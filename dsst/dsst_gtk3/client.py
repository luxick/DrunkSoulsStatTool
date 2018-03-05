import pprint
import socket
from common import util, models
try:
    import cPickle as pickle
except ImportError:
    import pickle


class Access:
    def __init__(self, conn_dict):
        self.host = conn_dict.get('host')
        self.port = conn_dict.get('port')
        self.buffer = conn_dict.get('buffer_size')
        self.auth_token = conn_dict.get('auth_token')

    def send_request(self, action: str, *args):
        request = {'auth_token': self.auth_token,
                   'action': action,
                   'args': args}
        request = pickle.dumps(request)
        soc = socket.socket()
        try:
            soc.connect((self.host, self.port))
            util.send_msg(soc, request)
            message = util.recv_msg(soc)
            message = pickle.loads(message)
            if not message.get('success'):
                raise Exception(message.get('message'))
        finally:
            soc.close()
        return message.get('data')

if __name__ == '__main__':
    access = Access({'host': 'europa', 'port': 12345, 'buffer_size': 1024, 'auth_token': 'a'})
    action = 'load_seasons'
    response = access.send_request(action)
    pp = pprint.PrettyPrinter(indent=1)
    for s in response:
        pp.pprint(s.__dict__)
