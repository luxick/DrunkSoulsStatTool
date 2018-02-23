import gi
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from dsst_gtk3.handlers import handlers
from dsst_gtk3 import util

from dsst_sql import sql, sql_func


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

        self.reload_base_data()
        self.reload_seasons()

    def reload_base_data(self):
        # Rebuild all players store
        self.ui.get_object('all_players_store').clear()
        for player in sql.Player.select():
            self.ui.get_object('all_players_store').append([player.id, player.name, player.hex_id])
        # Rebuild drink store
        self.ui.get_object('drink_store').clear()
        for drink in sql.Drink.select():
            self.ui.get_object('drink_store').append([drink.id, drink.name, str(drink.vol)])

    def reload_seasons(self):
        # Rebuild seasons store
        store = self.ui.get_object('seasons_store')
        store.clear()
        for season in sql.Season.select().order_by(sql.Season.number):
            store.append([season.id, season.game_name])

    def reload_for_season(self, season_id):
        if season_id is None or season_id == -1:
            return
        # Rebuild episodes store
        store = self.ui.get_object('episodes_store')
        store.clear()
        for episode in sql_func.get_episodes_for_season(season_id):
            store.append([episode.id, episode.number, str(episode.date)])
        # Load player stats for season
        player_stats = {}
        for episode in sql_func.get_episodes_for_season(season_id):
            for player in episode.players:
                player_stats[player.name] = [sql_func.get_player_deaths_for_season(season_id, player.id),
                                             sql_func.get_player_victories_for_season(season_id, player.id)]
        store = self.ui.get_object('player_season_store')
        store.clear()
        for name, stats in player_stats.items():
            store.append([name, stats[0], stats[1]])
        # Load enemy stats for season
        enemy_stats = {enemy.name: [0, 0] for enemy in sql.Season.get(sql.Season.id == season_id).enemies}
        store = self.ui.get_object('enemy_season_store')
        store.clear()
        for name, stats in enemy_stats.items():
            store.append([name, stats[0], stats[1]])

    def reload_for_episode(self, episode_id):
        pass

    def get_selected_season_id(self):
        season_id = util.Util.get_combo_value(self.ui.get_object('season_combo_box'), 0)
        return season_id if season_id != -1 else None


if __name__ == '__main__':
    DSSTGtkUi()
    Gtk.main()
