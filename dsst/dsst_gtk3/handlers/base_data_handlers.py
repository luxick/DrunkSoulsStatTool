from dsst_gtk3 import dialogs, gtk_ui
from dsst_sql import sql


class BaseDataHandlers:
    """Callback handlers for signals related to the manipulation of base data (players, drinks, ...)"""
    def __init__(self, app: 'gtk_ui.GtkUi'):
        self.app = app

    def do_manage_players(self, *_):
        result = dialogs.show_manage_players_dialog(self.app.ui, 'Manage Players')

    def do_add_player(self, entry):
        if entry.get_text():
            sql.Player.create(name=entry.get_text())
            entry.set_text('')
            self.app.reload_base_data()

    def do_manage_enemies(self, *_):
        result = dialogs.show_manage_enemies_dialog(self.app.ui, self.app.get_selected_season_id())