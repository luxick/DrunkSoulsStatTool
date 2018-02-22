from dsst_gtk3.gtk_ui import DSSTGtkUi
from dsst_gtk3 import dialogs, util
from dsst_sql import sql


class PlayerHandlers:
    def __init__(self, app: DSSTGtkUi):
        self.app = app

    def do_manage_players(self, *_):
        result = dialogs.show_manage_players_dialog(self.app.ui, 'Manage Players')

    def do_add_player(self, entry):
        if entry.get_text():
            sql.Player.create(name=entry.get_text())
            entry.set_text('')
            self.app.reload_view_data()

    def do_add_player_to_episode(self, combo):
        player_id = util.Util.get_combo_value(combo, 0)
        if player_id:
            self.app.ui.get_object('add_player_combo_box').set_active(-1)
            player = sql.Player.get(sql.Player.id == player_id)
            store = self.app.ui.get_object('episode_players_store')
            if not any(row[0] == player_id for row in store):
                store.append([player_id, player.name, player.hex_id])

