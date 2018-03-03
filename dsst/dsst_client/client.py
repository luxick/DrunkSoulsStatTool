import socket

try:
    import cPickcle as pickle
except ImportError:
    print('cPickle package not installed, falling back to pickle')
    import pickle

from common import util, models

PORT = 12345
HOST = 'europa'
BUFFER_SIZE = 1024

s = socket.socket()
s.connect((HOST, PORT))

try:
    data = 'get_dummy'
    message = pickle.dumps(data)
    util.send_msg(s, message)
    response = util.recv_msg(s)
    result = pickle.loads(response)
    print(result, result.__dict__)

finally:
    s.close()

