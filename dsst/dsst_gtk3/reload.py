from collections import Counter

from gi.repository import Gtk

from data_access import sql, sql_func
from dsst_gtk3 import util, gtk_ui


def reload_base_data(builder: Gtk.Builder, app: 'gtk_ui.GtkUi',):
    """Reload function for all base data witch is not dependant on a selected season or episode
    :param app: GtkUi instance
    :param builder: Gtk.Builder with loaded UI
    """
    # Rebuild all players store
    builder.get_object('all_players_store').clear()
    for player in app.data['players']:
        builder.get_object('all_players_store').append([player.id, player.name, player.hex_id])
    # Rebuild drink store
        builder.get_object('drink_store').clear()
    for drink in app.data['drinks']:
        builder.get_object('drink_store').append([drink.id, drink.name, '{:.2f}%'.format(drink.vol)])
    # Rebuild seasons store
    combo = builder.get_object('season_combo_box')  # type: Gtk.ComboBox
    active = combo.get_active()
    with util.block_handler(combo, app.handlers.do_season_selected):
        store = builder.get_object('seasons_store')
        store.clear()
        for season in app.data['seasons']:
            store.append([season.id, season.game_name])
        combo.set_active(active)


def reload_episodes(builder: Gtk.Builder, app: 'gtk_ui.GtkUi'):
    """Reload all data that is dependant on a selected season
    :param app: GtkUi instance
    :param builder: Gtk.Builder with loaded UI
    """
    # Rebuild episodes store
    selection = builder.get_object('episodes_tree_view').get_selection()
    with util.block_handler(selection, app.handlers.on_selected_episode_changed):
        model, selected_paths = selection.get_selected_rows()
        model.clear()
        for episode in app.data['episodes']:
            model.append([episode.id, episode.name, str(episode.date), episode.number])
        if selected_paths:
            selection.select_path(selected_paths[0])


def reload_season_stats(builder: Gtk.Builder, app: 'gtk_ui.GtkUi', season_id: int):
    """Load statistic data for selected season
    :param builder: Gtk.Builder with loaded UI
    :param app: GtkUi instance
    :param season_id: ID of the season for witch to load data
    """
    player_stats = {}
    for episode in sql_func.get_episodes_for_season(season_id):
        for player in episode.players:
            player_stats[player.name] = [sql_func.get_player_deaths_for_season(season_id, player.id),
                                         sql_func.get_player_victories_for_season(season_id, player.id)]
    store = builder.get_object('player_season_store')
    store.clear()
    for name, stats in player_stats.items():
        store.append([name, stats[0], stats[1]])
    # Load enemy stats for season
    season = sql.Season.get(sql.Season.id == season_id)
    enemy_stats = {
        enemy.name: [False, len(sql.Death.select().where(sql.Death.enemy == enemy)), enemy.id]
        for enemy in season.enemies}
    store = builder.get_object('enemy_season_store')
    store.clear()
    for name, stats in enemy_stats.items():
        store.append([name, stats[0], stats[1], stats[2]])


def reload_episode_stats(builder: Gtk.Builder, app: 'gtk_ui.GtkUi', episode_id: int):
    """Reload all data that is dependant on a selected episode
    :param builder: builder: Gtk.Builder with loaded UI
    :param app: app: GtkUi instance
    :param episode_id: ID of the episode for witch to load data
    """
    episode = sql.Episode.get(sql.Episode.id == episode_id)
    store = builder.get_object('episode_players_store')
    store.clear()
    for player in episode.players:
        store.append([player.id, player.name, player.hex_id])
    # Reload death store for notebook view
    store = builder.get_object('episode_deaths_store')
    store.clear()
    for death in episode.deaths:
        penalties = [x.drink.name for x in death.penalties]
        penalties = [f'{number}x {drink}' for drink, number in Counter(penalties).items()]
        penalty_string = ', '.join(penalties)
        store.append([death.id, death.player.name, death.enemy.name, penalty_string])
    # Reload victory store for notebook view
    store = builder.get_object('episode_victories_store')
    store.clear()
    for victory in episode.victories:
        store.append([victory.id, victory.player.name, victory.enemy.name, victory.info])

    # Stat grid
    builder.get_object('ep_stat_title').set_text('Stats for episode {}\n{}'.format(episode.number, episode.name))
    builder.get_object('ep_death_count_label').set_text(str(len(episode.deaths)))
    drink_count = sum(len(death.penalties) for death in episode.deaths)
    builder.get_object('ep_drinks_label').set_text(str(drink_count))
    builder.get_object('ep_player_drinks_label').set_text(str(len(episode.deaths)))
    dl_booze = sum(len(death.penalties) * death.penalties[0].size for death in episode.deaths)
    l_booze = round(dl_booze / 10, 2)
    builder.get_object('ep_booze_label').set_text('{}l'.format(l_booze))
    dl_booze = sum(len(death.penalties) * death.penalties[0].size for death in episode.deaths)
    ml_booze = round(dl_booze * 10, 0)
    builder.get_object('ep_player_booze_label').set_text('{}ml'.format(ml_booze))
    enemy_list = [death.enemy.name for death in episode.deaths]
    sorted_list = Counter(enemy_list).most_common(1)
    if sorted_list:
        enemy_name, deaths = sorted_list[0]
        builder.get_object('ep_enemy_name_label').set_text(f'{enemy_name} ({deaths} Deaths)')


def fill_list_store(store: Gtk.ListStore, models: list):
    store.clear()
    for model in models:
        pass