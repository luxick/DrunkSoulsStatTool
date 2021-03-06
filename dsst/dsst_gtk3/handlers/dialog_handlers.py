import datetime

from dsst_gtk3 import dialogs, util, gtk_ui, reload
from common import models
from gi.repository import Gtk


class DialogHandlers:
    """ Callback handlers for signals emitted from dialogs of the main window"""
    def __init__(self, app: 'gtk_ui.GtkUi'):
        self.app = app

    @staticmethod
    def do_run_manage_dialog(dialog: 'Gtk.Dialog'):
        dialog.run()
        dialog.hide()

    def do_add_player_to_episode(self, combo):
        """ Signal Handler for Add Player to Episode Button in Manage Episode Dialog
        :param combo: Combo box with all the available players
        """
        player_id = util.get_combo_value(combo, 0)
        if player_id:
            self.app.ui.get_object('add_player_combo_box').set_active(-1)
            player = self.app.get_by_id(self.app.players, player_id)
            store = self.app.ui.get_object('episode_players_store')
            if not any(row[0] == player_id for row in store):
                store.append([player_id, player.name, player.hex_id])

    def do_add_enemy(self, entry):
        if entry.get_text():
            enemy = models.Enemy()
            enemy.name = entry.get_text()
            enemy.season = self.app.get_selected_season_id()
            enemy.boss = not self.app.ui.get_object('enemy_optional_ckeck').get_active()
            self.app.ui.get_object('enemy_optional_ckeck').set_active(False)
            entry.set_text('')

            self.app.data_client.update_enemy(enemy)

    def on_enemy_name_edited(self, _, index, value):
        row = self.app.ui.get_object('enemy_season_store')[index]
        enemy = [enemy for enemy in self.app.enemies.data if enemy.id == row[4]][0]
        enemy.name = value
        self.app.data_client.update_enemy(enemy)

    def on_enemy_optional_edited(self, renderer, index):
        new_optional_value = not renderer.get_active()
        row = self.app.ui.get_object('enemy_season_store')[index]
        enemy = [enemy for enemy in self.app.enemies.data if enemy.id == row[4]][0]
        enemy.boss = new_optional_value
        self.app.data_client.update_enemy(enemy)

    def do_show_date_picker(self, entry: 'Gtk.Entry', *_):
        dialog = self.app.ui.get_object('date_picker_dialog')
        result = dialog.run()
        dialog.hide()
        if result == Gtk.ResponseType.OK:
            date = self.app.ui.get_object('date_picker_calendar').get_date()
            date_string = '{}-{:02d}-{:02d}'.format(date.year, date.month +1, date.day)
            entry.set_text(date_string)

    @staticmethod
    def do_set_today(cal: 'Gtk.Calendar'):
        """Set date of a Gtk Calendar to today
        :param cal: Gtk.Calendar
        """
        cal.select_month = datetime.date.today().month
        cal.select_day = datetime.date.today().day
