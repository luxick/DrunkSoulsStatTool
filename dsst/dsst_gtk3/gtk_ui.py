from collections import Counter

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from dsst_gtk3.handlers import handlers
from dsst_gtk3 import util
from dsst_sql import sql, sql_func


class GtkUi:
    """ The main UI class """
    def __init__(self):
        # Load Glade UI files
        self.ui = Gtk.Builder()
        glade_resources = [
            ['dsst_gtk3', 'resources', 'glade', 'window.glade'],
            ['dsst_gtk3', 'resources', 'glade', 'dialogs.glade']
        ]
        for path in glade_resources:
            self.ui.add_from_string(util.Util.load_ui_resource_string(path))
        # Connect signal handlers to UI
        self.handlers = handlers.Handlers(self)
        self.ui.connect_signals(self.handlers)
        # Show all widgets
        self.ui.get_object('main_window').show_all()
        # Initialize the database
        # TODO User input to select database
        sql.db.init('dsst', user='dsst', password='dsst')
        # Create database if not exists
        sql_func.create_tables()

        self.reload_base_data()

    def reload_base_data(self):
        """Reload function for all base data witch is not dependant on selected season or episode"""
        # Rebuild all players store
        self.ui.get_object('all_players_store').clear()
        for player in sql.Player.select():
            self.ui.get_object('all_players_store').append([player.id, player.name, player.hex_id])
        # Rebuild drink store
        self.ui.get_object('drink_store').clear()
        for drink in sql.Drink.select():
            self.ui.get_object('drink_store').append([drink.id, drink.name, str(drink.vol)])
        # Rebuild seasons store
        store = self.ui.get_object('seasons_store')
        store.clear()
        for season in sql.Season.select().order_by(sql.Season.number):
            store.append([season.id, season.game_name])

    # Reload after season was changed ##################################################################################
    def reload_for_season(self):
        """Reload all data that is dependant on a selected season"""
        season_id = self.get_selected_season_id()
        if season_id is None or season_id == -1:
            return
        # Rebuild episodes store
        selection = self.ui.get_object('episodes_tree_view').get_selection()
        selection.handler_block_by_func(self.handlers.on_selected_episode_changed)
        model, selected_paths = selection.get_selected_rows()
        model.clear()
        for episode in sql_func.get_episodes_for_season(season_id):
            model.append([episode.id, episode.name, str(episode.date), episode.number])
        if selected_paths:
            selection.select_path(selected_paths[0])
        selection.handler_unblock_by_func(self.handlers.on_selected_episode_changed)

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
        season = sql.Season.get(sql.Season.id == season_id)
        enemy_stats = {
            enemy.name: [False, len(sql.Death.select().where(sql.Death.enemy == enemy)), enemy.id]
            for enemy in season.enemies}
        store = self.ui.get_object('enemy_season_store')
        store.clear()
        for name, stats in enemy_stats.items():
            store.append([name, stats[0], stats[1], stats[2]])

    # Reload after episode was changed #################################################################################
    def reload_for_episode(self):
        """Reload all data that is dependant on a selected episode"""
        episode_id = self.get_selected_episode_id()
        if not episode_id:
            return
        episode = sql.Episode.get(sql.Episode.id == episode_id)
        store = self.ui.get_object('episode_players_store')
        store.clear()
        for player in episode.players:
            store.append([player.id, player.name, player.hex_id])
        # Reload death store for notebook view
        store = self.ui.get_object('episode_deaths_store')
        store.clear()
        for death in episode.deaths:
            penalties = [x.drink.name for x in death.penalties]
            penalties = [f'{number}x {drink}' for drink, number in Counter(penalties).items()]
            penalty_string = ', '.join(penalties)
            store.append([death.id, death.player.name, death.enemy.name, penalty_string])

        # Stat grid
        self.ui.get_object('ep_death_count_label').set_text(str(len(episode.deaths)))
        drink_count = sum(len(death.penalties) for death in episode.deaths)
        self.ui.get_object('ep_drinks_label').set_text(str(drink_count))
        cl_booze = sum(len(death.penalties) * death.penalties[0].size for death in episode.deaths)
        self.ui.get_object('ep_booze_label').set_text(str(cl_booze) + "cl")
        enemy_list = [death.enemy.name for death in episode.deaths]
        sorted_list = Counter(enemy_list).most_common(1)
        if sorted_list:
            enemy_name, deaths = sorted_list[0]
            self.ui.get_object('ep_enemy_name_label').set_text(f'{enemy_name} ({deaths} Deaths)')

    def get_selected_season_id(self) -> int:
        """Read ID of the selected season from the UI
        :return: ID of the selected season
        """
        season_id = util.Util.get_combo_value(self.ui.get_object('season_combo_box'), 0)
        return season_id if season_id != -1 else None

    def get_selected_episode_id(self):
        """Parse ID of the selected episode from the UI
        :return: ID of the selected episode
        """
        (model, tree_iter) = self.ui.get_object('episodes_tree_view').get_selection().get_selected()
        return model.get_value(tree_iter, 0) if tree_iter else None


def main():
    GtkUi()
    Gtk.main()
