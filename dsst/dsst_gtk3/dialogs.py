import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
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


def show_episode_dialog(builder: Gtk.Builder, title: str, episode: sql.Episode=None):
    dialog = builder.get_object("edit_episode_dialog")  # type: Gtk.Dialog
    dialog.set_transient_for(builder.get_object("main_window"))
    dialog.set_title(title)
    if episode:
        builder.get_object("episode_no_spin_button").set_value(episode.number)
        ep_players = sql.Player.select().join(sql.EpisodePlayer).join(sql.Episode).get()

    result = dialog.run()
    dialog.hide()

    if result == Gtk.ResponseType.OK:
        player_ids = [row[0] for row in builder.get_object('episode_players_store')]
        query = sql.EpisodePlayer\
            .delete()\
            .wher(sql.EpisodePlayer.episode == episode.id)\
            .where(sql.EpisodePlayer.player.not_in(player_ids))
        #query = sql.EpisodePlayer.get_or_create(episode=episode.id, player=pl)

        return episode
    else:
        return None


def show_manage_players_dialog(builder: Gtk.Builder, title: str):
    dialog = builder.get_object("manage_players_dialog")  # type: Gtk.Dialog
    dialog.set_transient_for(builder.get_object("main_window"))
    dialog.set_title(title)

    result = dialog.run()
    dialog.hide()

    if result == Gtk.ResponseType.OK:
        pass