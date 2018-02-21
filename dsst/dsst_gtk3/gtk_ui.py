import gi
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class DSSTGtkUi:
    def __init__(self):
        self.ui = Gtk.Builder()
        self.ui.add_from_file(os.path.join(os.path.dirname(__file__), 'resources', 'glade', 'window.glade'))
        self.ui.get_object('main_window').show_all()

if __name__ == '__main__':
    DSSTGtkUi()
    Gtk.main()
