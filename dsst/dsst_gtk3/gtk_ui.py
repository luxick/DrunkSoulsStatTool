import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from dsst_gtk3.handlers import handlers
from dsst_gtk3 import util, reload, client


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
        # Set the status bar logo
        dd_logo = ['dsst_gtk3', 'resources', 'images', 'dd.png']
        logo_pixbuf = util.load_image_resource(dd_logo, 60, 13)
        logo = self.ui.get_object('status_bar_logo').set_from_pixbuf(logo_pixbuf)
        # Connect signal handlers to UI
        self.handlers = handlers.Handlers(self)
        self.ui.connect_signals(self.handlers)
        # Show all widgets
        self.ui.get_object('main_window').show_all()
        # Connect to data server
        config = config['servers'][0]
        self.data_client = client.Access(config)
        self.data = {}
        self.meta = {'connection': '{}:{}'.format(config.get('host'), config.get('port'))}
        self.season_changed = True
        self.ep_changed = False
        # Load base data and seasons
        self.initial_load()
        self.update_status_bar_meta()

    def initial_load(self):
        with util.network_operation(self):
            self.data['players'] = self.data_client.send_request('load_players')
            self.data['drinks'] = self.data_client.send_request('load_drinks')
            self.data['seasons'] = self.data_client.send_request('load_seasons')
            self.meta['database'] = self.data_client.send_request('load_db_meta')
            reload.reload_base_data(self.ui, self)

    def reload(self):
        if self.season_changed:
            with util.network_operation(self):
                season_id = self.get_selected_season_id()
                self.data['episodes'] = self.data_client.send_request('load_episodes', season_id)
                self.data['season_stats'] = self.data_client.send_request('load_season_stats', season_id)
                reload.reload_episodes(self.ui, self)
                reload.reload_season_stats(self)
            self.season_changed = False

        if self.ep_changed:
            reload.reload_episode_stats(self)

    def update_status_bar_meta(self):
        self.ui.get_object('connection_label').set_text(self.meta.get('connection'))
        self.ui.get_object('db_label').set_text(self.meta.get('database') or '')

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


if __name__ == '__main__':
    main()
