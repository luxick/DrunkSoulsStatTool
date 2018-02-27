from dsst_sql import sql
from dsst_gtk3 import dialogs, gtk_ui


class SeasonHandlers:
    """Callback handlers related to signals for managing seasonal data"""
    def __init__(self, app: 'gtk_ui.GtkUi'):
        self.app = app

    def do_add_season(self, *_):
        name = dialogs.enter_string_dialog(self.app.ui, 'Name for the new Season')
        if name:
            sql.Season.create(game_name=name, number=1)
            self.app.reload_base_data()

    def do_season_selected(self, *_):
        self.app.reload_for_season()

    def do_add_episode(self, *_):
        season_id = self.app.get_selected_season_id()
        if not season_id:
            return
        episode = dialogs.show_episode_dialog(self.app.ui, 'Create new Episode', season_id)
        self.app.reload_for_season()

    def on_selected_episode_changed(self, *_):
        self.app.reload_for_episode()