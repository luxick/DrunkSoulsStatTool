from dsst_gtk3 import dialogs, util, gtk_ui
from dsst_sql import sql


class DialogHandlers:
    """ Callback handlers for signals emitted from dialogs of the main window"""
    def __init__(self, app: 'gtk_ui.GtkUi'):
        self.app = app

    def do_add_player_to_episode(self, combo):
        """ Signal Handler for Add Player to Episode Button in Manage Episode Dialog
        :param combo: Combo box with all the available players
        """
        player_id = util.Util.get_combo_value(combo, 0)
        if player_id:
            self.app.ui.get_object('add_player_combo_box').set_active(-1)
            player = sql.Player.get(sql.Player.id == player_id)
            store = self.app.ui.get_object('episode_players_store')
            if not any(row[0] == player_id for row in store):
                store.append([player_id, player.name, player.hex_id])

    def do_add_enemy(self, entry):
        if entry.get_text():
            store = self.app.ui.get_object('enemy_season_store')
            enemy = sql.Enemy.create(name=entry.get_text(), season=self.app.get_selected_season_id())
            store.append([enemy.name, False, 0, enemy.id])
            entry.set_text('')

    def do_manage_drinks(self, *_):
        result = dialogs.show_manage_drinks_dialog(self.app.ui)

    def do_add_drink(self, entry):
        if entry.get_text():
            store = self.app.ui.get_object('drink_store')
            drink = sql.Drink.create(name=entry.get_text(), vol='0')
            store.append([drink.id, drink.name, drink.vol])
            entry.set_text('')