from dsst_gtk3.gtk_ui import DSSTGtkUi
from dsst_gtk3.util import Util
from dsst_sql import sql
from dsst_gtk3 import dialogs


class SeasonAndEpisodesHandlers:
    def __init__(self, app: DSSTGtkUi):
        self.app = app

    def do_add_season(self, *_):
        name = dialogs.enter_string_dialog(self.app.ui, 'Name for the new Season')
        if name:
            sql.Season.create(game_name=name, number=1)
            self.app.reload_view_data()

    def do_season_selected(self, *_):
        combo = self.app.ui.get_object('season_combo_box')
        season_id = Util.get_combo_value(combo, 0)
        if not season_id: return
        season = sql.Season.get(sql.Season.id == season_id)
        for episode in season.episodes:
            print(episode)

    def do_add_episode(self, *_):
        episode = dialogs.show_episode_dialog(self.app.ui, 'Create new Episode')
