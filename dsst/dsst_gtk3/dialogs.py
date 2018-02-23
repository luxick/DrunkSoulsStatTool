import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from datetime import datetime
from dsst_sql import sql


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
    with sql.connection.atomic():
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
            sql.connection.rollback()
            return False

        # Save all changes to Database
        player_ids = [row[0] for row in builder.get_object('episode_players_store')]
        # Insert new Players
        episode.players = sql.Player.select().where(sql.Player.id << player_ids)
        # Update Date of the Episode
        cal_value = builder.get_object('episode_calendar').get_date()
        selected_date = datetime(*cal_value).date()
        query = sql.Episode.update(date=selected_date,
                                   number=int(builder.get_object("episode_no_spin_button").get_value()))\
                           .where(sql.Episode.id == episode.id)
        query.execute()
        return True


def show_manage_players_dialog(builder: Gtk.Builder, title: str):
    dialog = builder.get_object("manage_players_dialog")  # type: Gtk.Dialog
    dialog.set_transient_for(builder.get_object("main_window"))
    dialog.set_title(title)

    result = dialog.run()
    dialog.hide()

    if result == Gtk.ResponseType.OK:
        pass


def show_manage_enemies_dialog(builder: Gtk.Builder, season_id: int):
    dialog = builder.get_object("manage_enemies_dialog")  # type: Gtk.Dialog
    dialog.set_transient_for(builder.get_object("main_window"))

    result = dialog.run()
    dialog.hide()

    return result


def show_manage_drinks_dialog(builder: Gtk.Builder):
    dialog = builder.get_object("manage_drinks_dialog")  # type: Gtk.Dialog
    dialog.set_transient_for(builder.get_object("main_window"))
    result = dialog.run()
    dialog.hide()
    return result
