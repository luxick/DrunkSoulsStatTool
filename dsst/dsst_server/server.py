import pickle
import socket

from data_access import sql
from common import util, models

PORT = 12345
HOST = socket.gethostname()
BUFFER_SIZE = 1024


class DsstServer:
    def __init__(self):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Created socket')

        self.socket_server.bind((HOST, PORT))
        print(f'Bound socket to {PORT} on host {HOST}')

    def run(self):
        self.socket_server.listen(5)
        print('Socket is listening')

        while True:
            client, address = self.socket_server.accept()
            try:
                print(f'Connection from {address}')
                data = util.recv_msg(client)
                request = pickle.loads(data)
                print(f'Received data: {request}')
                dummy = models.Player()
                dummy.name = 'Player 1'
                dummy.hex_id = '0xC2'
                dummy.deaths = [1, 2, 3]
                util.send_msg(client, pickle.dumps(dummy))
            finally:
                client.close()
                print('Connection to client closed')

if __name__ == '__main__':
    server = DsstServer()
    server.run()
