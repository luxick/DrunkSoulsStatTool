from dsst_gtk3 import dialogs, gtk_ui
from common import models


class BaseDataHandlers:
    """Callback handlers for signals related to the manipulation of base data (players, drinks, ...)"""
    def __init__(self, app: 'gtk_ui.GtkUi'):
        self.app = app

    def do_add_player(self, entry):
        if entry.get_text():
            self.app.update_player(models.Player({'name': entry.get_text()}))
            entry.set_text('')

    def on_player_name_edited(self, _, index, value):
        row = self.app.ui.get_object('all_players_store')[index]
        player = models.Player({'id': row[0],
                                'name': value,
                                'hex_id': row[2]})
        self.app.update_player(player)

    def on_player_hex_edited(self, _, index, value):
        row = self.app.ui.get_object('all_players_store')[index]
        player = models.Player({'id': row[0],
                                'name': row[1],
                                'hex_id': value})
        self.app.update_player(player)

    def do_add_drink(self, entry):
        if entry.get_text():
            sql.Drink.create(name=entry.get_text(), vol=0)
            entry.set_text('')
            self.app.full_reload()

    def on_drink_name_edited(self, _, index, value):
        row = self.app.ui.get_object('drink_store')[index]
        # sql.Drink.update(name=value)\
        #          .where(sql.Drink.id == row[0])\
        #          .execute()
        self.app.full_reload()

    def on_drink_vol_edited(self, _, index, value):
        row = self.app.ui.get_object('drink_store')[index]
        # sql.Drink.update(vol=value) \
        #          .where(sql.Drink.id == row[0]) \
        #          .execute()
        self.app.full_reload()