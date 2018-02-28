"""
This module contains UI functions for displaying different dialogs
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from datetime import datetime
from dsst_sql import sql
from dsst_gtk3 import util


def enter_string_dialog(builder: Gtk.Builder, title: str, value=None) -> str:
    """ Simple modal dialog for entering a string value
    :param builder: GtkBuilder with loaded dialogs.glade file
    :param title: Dialog title
    :param value: Pre set value for dialog
    :return:
    """
    dialog = builder.get_object("nameEnterDialog")  # type: Gtk.Dialog
    dialog.set_transient_for(builder.get_object("main_window"))
    dialog.set_title(title)
    entry = builder.get_object("nameEnterEntry")
    if value:
        entry.set_text(value)
    entry.grab_focus()

    result = dialog.run()
    dialog.hide()

    if result == Gtk.ResponseType.OK:
        return entry.get_text()
    else:
        return value


def show_episode_dialog(builder: Gtk.Builder, title: str, season_id: int, episode: sql.Episode=None):
    """ Shows a dialog to edit an episode
    :param builder: GtkBuilder with loaded 'dialogs.glade'
    :param title: Title of the dialog window
    :param season_id: Season to witch the episode should be added
    :param episode: (Optional) Existing episode to edit
    :return True if changes where saved False if discarded
    """
    # Set up the dialog
    dialog = builder.get_object("edit_episode_dialog")  # type: Gtk.Dialog
    dialog.set_transient_for(builder.get_object("main_window"))
    dialog.set_title(title)
    with sql.db.atomic():
        if not episode:
            nxt_number = len(sql.Season.get_by_id(season_id).episodes) + 1
            episode = sql.Episode.create(seq_number=nxt_number, number=nxt_number, date=datetime.today(),
                                         season=season_id)
        # Set episode number
        builder.get_object("episode_no_spin_button").set_value(episode.number)
        # Set episode date
        builder.get_object('episode_calendar').select_month(episode.date.month, episode.date.year)
        builder.get_object('episode_calendar').select_day(episode.date.day)
        # Set participants for the episode
        builder.get_object('episode_players_store').clear()
        for player in episode.players:
            builder.get_object('episode_players_store').append([player.id, player.name, player.hex_id])

        result = dialog.run()
        dialog.hide()

        if result != Gtk.ResponseType.OK:
            sql.db.rollback()
            return False

        # Save all changes to Database
        player_ids = [row[0] for row in builder.get_object('episode_players_store')]
        # Insert new Players
        episode.players = sql.Player.select().where(sql.Player.id << player_ids)
        # Update Date of the Episode
        cal_value = builder.get_object('episode_calendar').get_date()
        selected_date = datetime(*cal_value).date()
        episode.update(date=selected_date,
                       number=str(builder.get_object("episode_no_spin_button").get_value()),
                       name=builder.get_object("episode_name_entry").get_text())\
                .execute()
        return True


def show_manage_players_dialog(builder: Gtk.Builder, title: str):
    """Show a dialog for managing player base data.
    :param builder: Gtk.Builder object
    :param title: Title for the dialog
    """
    dialog = builder.get_object("manage_players_dialog")  # type: Gtk.Dialog
    dialog.set_transient_for(builder.get_object("main_window"))
    dialog.run()
    dialog.hide()


def show_manage_enemies_dialog(builder: Gtk.Builder, season_id: int):
    dialog = builder.get_object("manage_enemies_dialog")  # type: Gtk.Dialog
    dialog.set_transient_for(builder.get_object("main_window"))
    dialog.run()
    dialog.hide()


def show_manage_drinks_dialog(builder: Gtk.Builder):
    dialog = builder.get_object("manage_drinks_dialog")  # type: Gtk.Dialog
    dialog.set_transient_for(builder.get_object("main_window"))
    dialog.run()
    dialog.hide()


def show_edit_death_dialog(builder: Gtk.Builder, episode_id: int, death: sql.Death=None):
    """Show a dialog for editing or creating death events.
    :param builder: A Gtk.Builder object
    :param episode_id: ID to witch the death event belongs to
    :param death: (Optional) Death event witch should be edited
    :return: Gtk.ResponseType of the dialog
    """
    dialog = builder.get_object("edit_death_dialog")  # type: Gtk.Dialog
    dialog.set_transient_for(builder.get_object("main_window"))
    with sql.db.atomic():
        if death:
            index = util.Util.get_index_of_combo_model(builder.get_object('edit_death_enemy_combo'), 0, death.enemy.id)
            builder.get_object('edit_death_enemy_combo').set_active(index)

        # TODO Default drink should be set in config
        default_drink = sql.Drink.get().name
        store = builder.get_object('player_penalties_store')
        store.clear()
        for player in builder.get_object('episode_players_store'):
            store.append([None, player[1], default_drink, player[0]])

        # Run the dialog
        result = dialog.run()
        dialog.hide()
        if result != Gtk.ResponseType.OK:
            sql.db.rollback()
            return result

        # Collect info from widgets and save to database
        player_id = util.Util.get_combo_value(builder.get_object('edit_death_player_combo'), 0)
        enemy_id = util.Util.get_combo_value(builder.get_object('edit_death_enemy_combo'), 3)
        comment = builder.get_object('edit_death_comment_entry').get_text()
        if not death:
            death = sql.Death.create(episode=episode_id, player=player_id, enemy=enemy_id, info=comment)

        store = builder.get_object('player_penalties_store')
        size = builder.get_object('edit_death_size_spin').get_value()
        for entry in store:
            drink_id = sql.Drink.get(sql.Drink.name == entry[2])
            sql.Penalty.create(size=size, player=entry[3], death=death.id, drink=drink_id)

        return result
