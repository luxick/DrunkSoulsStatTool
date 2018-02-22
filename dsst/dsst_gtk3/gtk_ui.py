import gi
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from dsst_gtk3.handlers import handlers

from dsst_sql import sql


class DSSTGtkUi:
    """ The main UI class """
    def __init__(self):
        # Load Glade UI files
        self.ui = Gtk.Builder()
        self.ui.add_from_file(os.path.join(os.path.dirname(__file__), 'resources', 'glade', 'window.glade'))
        self.ui.add_from_file(os.path.join(os.path.dirname(__file__), 'resources', 'glade', 'dialogs.glade'))
        # Connect signal handlers to UI
        self.handlers = handlers.Handlers(self)
        self.ui.connect_signals(self.handlers)
        # Show all widgets
        self.ui.get_object('main_window').show_all()
        # Create database if not exists
        sql.create_tables()

        self.reload_view_data()

    def reload_view_data(self):
        # Rebuild all players store
        self.ui.get_object('all_players_store').clear()
        for player in sql.Player.select():
            self.ui.get_object('all_players_store').append([player.id, player.name, player.hex_id])
        # Rebuild seasons store
        store = self.ui.get_object('seasons_store')
        store.clear()
        for season in sql.Season.select().order_by(sql.Season.number):
            store.append([season.id, season.game_name])



if __name__ == '__main__':
    DSSTGtkUi()
    Gtk.main()
