from dsst_gtk3 import dialogs, gtk_ui, reload


class SeasonHandlers:
    """Callback handlers related to signals for managing seasonal data"""
    def __init__(self, app: 'gtk_ui.GtkUi'):
        self.app = app

    def do_add_season(self, *_):
        season = dialogs.edit_season(self.app.ui)
        if season:
            self.app.update_season(season)
            self.app.reload()

    def do_season_selected(self, *_):
        self.app.episodes.valid = False
        self.app.season_stats.valid = False
        self.app.reload()

    def do_add_episode(self, *_):
        season_id = self.app.get_selected_season_id()
        if not season_id:
            return
        ep = dialogs.edit_episode(self.app, season_id)
        if ep:
            self.app.update_episode(ep)
            self.app.reload()

    def on_selected_episode_changed(self, *_):
        reload.reload_episode_stats(self.app)

    def on_episode_double_click(self, *_):
        self.app.ui.get_object('stats_notebook').set_current_page(1)
