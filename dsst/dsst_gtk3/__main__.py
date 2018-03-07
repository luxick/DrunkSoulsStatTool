import os.path
import sys

# Add current directory to python path
path = os.path.realpath(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

from dsst_gtk3 import gtk_ui

if __name__ == '__main__':
    gtk_ui.main()
