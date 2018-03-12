from dsst_gtk3 import dialogs


class BaseDataHandlers:
    """Callback handlers for signals related to the manipulation of base data (players, drinks, ...)"""
    def __init__(self, app: 'gtk_ui.GtkUi'):
        self.app = app

    def do_manage_players(self, *_):
        dialogs.run_management_dialog(self.app.ui, 'manage_players_dialog')

    def do_add_player(self, entry):
        if entry.get_text():
            # sql.Player.create(name=entry.get_text())
            entry.set_text('')
            self.app.reload()

    def do_manage_enemies(self, *_):
        dialogs.run_management_dialog(self.app.ui, 'manage_enemies_dialog')

    def on_player_name_edited(self, _, index, value):
        row = self.app.ui.get_object('all_players_store')[index]
        # sql.Player.update(name=value)\
        #           .where(sql.Player.id == row[0])\
        #           .execute()
        self.app.reload()

    def on_player_hex_edited(self, _, index, value):
        row = self.app.ui.get_object('all_players_store')[index]
        # sql.Player.update(hex_id=value)\
        #           .where(sql.Player.id == row[0])\
        #           .execute()
        self.app.reload()

    def do_add_drink(self, entry):
        if entry.get_text():
            sql.Drink.create(name=entry.get_text(), vol=0)
            entry.set_text('')
            self.app.reload()

    def on_drink_name_edited(self, _, index, value):
        row = self.app.ui.get_object('drink_store')[index]
        # sql.Drink.update(name=value)\
        #          .where(sql.Drink.id == row[0])\
        #          .execute()
        self.app.reload()

    def on_drink_vol_edited(self, _, index, value):
        row = self.app.ui.get_object('drink_store')[index]
        # sql.Drink.update(vol=value) \
        #          .where(sql.Drink.id == row[0]) \
        #          .execute()
        self.app.reload()