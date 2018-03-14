"""
This module contains UI functions for displaying different dialogs
"""
import datetime
from gi.repository import Gtk
from common import models
from dsst_gtk3 import gtk_ui, util


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


def edit_season(builder: 'Gtk.Builder', season: 'models.Season'=None):
    if not season:
        season = models.Season()
    builder.get_object('season_number_spin').set_value(season.number or 1)
    builder.get_object('season_game_entry').set_text(season.game_name or '')
    builder.get_object('season_start_entry').set_text(season.start_date or '')
    builder.get_object('season_end_entry').set_text(season.end_date or '')

    dialog = builder.get_object('edit_season_dialog')
    result = dialog.run()
    dialog.hide()

    if result != Gtk.ResponseType.OK:
        return None

    season.number = builder.get_object('season_number_spin').get_value()
    season.game_name = builder.get_object('season_game_entry').get_text()
    start_string = builder.get_object('season_start_entry').get_text()
    if start_string:
        season.start_date = datetime.datetime.strptime(start_string, '%Y-%m-%d')
    end_string = builder.get_object('season_end_entry').get_text()
    if end_string:
        season.end_date = datetime.datetime.strptime(end_string, '%Y-%m-%d')
    return season


def edit_episode(app: 'gtk_ui.GtkUi', season_id: int, episode: 'models.Episode'=None):
    """Show an dialog to create or edit episodes
    :param app: Reference to main UI application
    :param season_id: Is of the season in which the episode appears
    :param episode: Existing episode object to edit
    :return: Edited episode object, or None if the process was canceled
    """
    if not episode:
        episode = models.Episode()
        episode.date = datetime.datetime.today()
        episode.number = 1
        episode.name = ''
        episode.players = []

    app.ui.get_object('episode_name_entry').set_text(episode.name)
    app.ui.get_object('episode_no_spin_button').set_value(episode.number)
    app.ui.get_object('episode_calendar').select_month(episode.date.month, episode.date.year)
    app.ui.get_object('episode_calendar').select_day(episode.date.day)
    app.ui.get_object('episode_players_store').clear()
    for player in episode.players:
        app.ui.get_object('episode_players_store').append([player.id, player.name, player.hex_id])

    dialog = app.ui.get_object('edit_episode_dialog')  # type: Gtk.Dialog
    result = dialog.run()
    dialog.hide()

    if result != Gtk.ResponseType.OK:
        return None

    episode.name = app.ui.get_object('episode_name_entry').get_text()
    episode.number = app.ui.get_object('episode_no_spin_button').get_value()
    cal_value = app.ui.get_object('episode_calendar').get_date()
    selected_date = datetime.datetime(*cal_value).date()
    episode.date = selected_date
    player_ids = [row[0] for row in app.ui.get_object('episode_players_store')]
    episode.players = [app.get_by_id(app.players, player_id) for player_id in player_ids]
    episode.season = season_id
    return episode


def edit_death(app: 'gtk_ui.GtkUi', death: 'models.Death'=None):
    """Show a dialog to create or edit death events for an episode
    :param app: Main Gtk application
    :param death: (Optional) Existing death object to edit
    :return: Death object or None if dialog was canceled
    """
    if not death:
        death = models.Death()
        death.episode = app.get_selected_episode_id()
        death.info = ""
        death.penalties = []
        death.time = datetime.time(0, 0)
    hour_spin = app.ui.get_object('death_hour_spin')
    min_spin = app.ui.get_object('death_min_spin')
    # Set time of death
    hour_spin.set_value(death.time.hour)
    min_spin.set_value(death.time.minute)
    # Set Enemy
    if death.enemy:
        index = util.get_index_of_combo_model(app.ui.get_object('edit_death_enemy_combo'), 0, death.enemy.id)
        app.ui.get_object('edit_death_enemy_combo').set_active(index)
    # Set player
    if death.player:
        index = util.get_index_of_combo_model(app.ui.get_object('edit_death_player_combo'), 0, death.player.id)
        app.ui.get_object('edit_death_player_combo').set_active(index)
    # Set shot size
    if death.penalties:
        app.ui.get_object('edit_death_size_spin').set_value(death.penalties[0].size)
    # Set info comment
    app.ui.get_object('edit_death_comment_entry').set_text(death.info)
    # Set penalties
    default_drink = app.drinks.data[0].name
    store = app.ui.get_object('player_penalties_store')
    store.clear()
    if death.penalties:
        for penalty in death.penalties:
            store.append([penalty.id, penalty.player.name, penalty.drink.name, penalty.player.id])
    else:
        for player in app.ui.get_object('episode_players_store'):
            store.append([None, player[1], default_drink, player[0]])

    # Run the dialog
    dialog = app.ui.get_object("edit_death_dialog")  # type: Gtk.Dialog
    result = dialog.run()
    dialog.hide()
    if result != Gtk.ResponseType.OK:
        return None

    # Parse the inputs
    death.time = datetime.time(int(hour_spin.get_value()), int(min_spin.get_value()))
    death.enemy = util.get_combo_value(app.ui.get_object('edit_death_enemy_combo'), 4)
    death.player = util.get_combo_value(app.ui.get_object('edit_death_player_combo'), 0)
    death.info = app.ui.get_object('edit_death_comment_entry').get_text()
    store = app.ui.get_object('player_penalties_store')
    size = app.ui.get_object('edit_death_size_spin').get_value()
    death.penalties.clear()
    for entry in store:
        drink_id = [drink.id for drink in app.drinks.data if drink.name == entry[2]][0]
        penalty = models.Penalty({'id': entry[0], 'size': size, 'drink': drink_id, 'player': entry[3]})
        death.penalties.append(penalty)

    return death


def show_edit_victory_dialog(builder: Gtk.Builder, episode_id: int, victory):
    pass
    # """Show a dialog for editing or creating victory events.
    # :param builder: A Gtk.Builder object
    # :param episode_id: ID to witch the victory event belongs to
    # :param victory: (Optional) Victory event witch should be edited
    # :return: Gtk.ResponseType of the dialog
    # """
    # dialog = builder.get_object("edit_victory_dialog")  # type: Gtk.Dialog
    # dialog.set_transient_for(builder.get_object("main_window"))
    # with sql.db.atomic():
    #     if victory:
    #         infos = [['edit_victory_player_combo', victory.player.id],
    #                  ['edit_victory_enemy_combo', victory.enemy.id]]
    #         for info in infos:
    #             combo = builder.get_object(info[0])
    #             index = util.get_index_of_combo_model(combo, 0, info[1])
    #             combo.set_active(index)
    #         builder.get_object('victory_comment_entry').set_text(victory.info)
    #
    #     # Run the dialog
    #     result = dialog.run()
    #     dialog.hide()
    #     if result != Gtk.ResponseType.OK:
    #         sql.db.rollback()
    #         return result
    #
    #     # Collect info from widgets and save to database
    #     player_id = util.get_combo_value(builder.get_object('edit_victory_player_combo'), 0)
    #     enemy_id = util.get_combo_value(builder.get_object('edit_victory_enemy_combo'), 3)
    #     comment = builder.get_object('victory_comment_entry').get_text()
    #     if not victory:
    #         sql.Victory.create(episode=episode_id, player=player_id, enemy=enemy_id, info=comment)
    #     else:
    #         victory.player = player_id
    #         victory.enemy = enemy_id
    #         victory.info = comment
    #         victory.save()
    #
    #     return result
