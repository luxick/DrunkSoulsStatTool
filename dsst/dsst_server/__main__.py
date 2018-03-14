import os.path
import sys

# Add current directory to python path
path = os.path.realpath(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

from dsst_server import server

if __name__ == '__main__':
    server.main()
