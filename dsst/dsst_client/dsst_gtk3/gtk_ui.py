import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from dsst_gtk3.handlers import handlers
from dsst_gtk3 import util, reload
import sql_func
import sql


class GtkUi:
    """ The main UI class """
    def __init__(self, config: dict):
        # Load Glade UI files
        self.ui = Gtk.Builder()
        glade_resources = [
            ['dsst_gtk3', 'resources', 'glade', 'window.glade'],
            ['dsst_gtk3', 'resources', 'glade', 'dialogs.glade']
        ]
        for path in glade_resources:
            self.ui.add_from_string(util.load_ui_resource_string(path))
        # Connect signal handlers to UI
        self.handlers = handlers.Handlers(self)
        self.ui.connect_signals(self.handlers)
        # Show all widgets
        self.ui.get_object('main_window').show_all()
        db_config = config['sql_connections'][0]
        # Initialize the database
        sql.db.init(db_config['db_name'], host=db_config['host'], port=db_config['port'],
                    user=db_config['user'], password=db_config['password'])
        # Show database info in status bar
        self.set_db_status_label(db_config)
        # Create database if not exists
        sql_func.create_tables()
        self.reload()

    def reload(self):
        reload.reload_base_data(self.ui, self)
        season_id = self.get_selected_season_id()
        if season_id:
            reload.reload_episodes(self.ui, self, season_id)
            reload.reload_season_stats(self.ui, self, season_id)
        else:
            return
        episode_id = self.get_selected_episode_id()
        if episode_id:
            reload.reload_episode_stats(self.ui, self, episode_id)

    def set_db_status_label(self, db_conf: dict):
        self.ui.get_object('connection_label').set_text(f'{db_conf["user"]}@{db_conf["host"]}')
        self.ui.get_object('db_label').set_text(f'{db_conf["db_name"]}')

    def get_selected_season_id(self) -> int:
        """Read ID of the selected season from the UI
        :return: ID of the selected season
        """
        season_id = util.get_combo_value(self.ui.get_object('season_combo_box'), 0)
        return season_id if season_id != -1 else None

    def get_selected_episode_id(self):
        """Parse ID of the selected episode from the UI
        :return: ID of the selected episode
        """
        (model, tree_iter) = self.ui.get_object('episodes_tree_view').get_selection().get_selected()
        return model.get_value(tree_iter, 0) if tree_iter else None


def main():
    if not os.path.isfile(util.CONFIG_PATH):
        util.save_config(util.DEFAULT_CONFIG, util.CONFIG_PATH)
    config = util.load_config(util.CONFIG_PATH)
    GtkUi(config)
    Gtk.main()
