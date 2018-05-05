from dsst_gtk3 import dialogs, gtk_ui
from common import models


class BaseDataHandlers:
    """Callback handlers for signals related to the manipulation of base data (players, drinks, ...)"""
    def __init__(self, app: 'gtk_ui.GtkUi'):
        self.app = app

    def do_add_player(self, entry):
        if entry.get_text():
            self.app.data_client.update_player(models.Player({'name': entry.get_text()}))
            entry.set_text('')

    def on_player_name_edited(self, _, index, value):
        row = self.app.ui.get_object('all_players_store')[index]
        player = models.Player({'id': row[0],
                                'name': value,
                                'hex_id': row[2]})
        self.app.data_client.update_player(player)

    def on_player_hex_edited(self, _, index, value):
        row = self.app.ui.get_object('all_players_store')[index]
        player = models.Player({'id': row[0],
                                'name': row[1],
                                'hex_id': value})
        self.app.data_client.update_player(player)

    def do_add_drink(self, entry):
        if entry.get_text():
            drink = models.Drink({'name': entry.get_text(), 'vol': 0.00})
            self.app.data_client.update_drink(drink)
            entry.set_text('')

    def on_drink_name_edited(self, _, index, value):
        row = self.app.ui.get_object('drink_store')[index]
        drink = [d for d in self.app.drinks.data if d.id == row[0]][0]
        drink.name = value
        self.app.data_client.update_drink(drink)

    def on_drink_vol_edited(self, _, index, value):
        row = self.app.ui.get_object('drink_store')[index]
        drink = [d for d in self.app.drinks.data if d.id == row[0]][0]
        drink.vol = value
        self.app.data_client.update_drink(drink)