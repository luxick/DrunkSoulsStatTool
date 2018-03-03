import os.path
import sys

# Add current directory to python path
path = os.path.realpath(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(path))

import gtk_ui

if __name__ == '__main__':
    gtk_ui.main()