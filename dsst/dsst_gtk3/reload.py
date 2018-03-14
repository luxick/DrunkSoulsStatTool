from collections import Counter
from gi.repository import Gtk
from dsst_gtk3 import util, gtk_ui


def reload_base_data(app: 'gtk_ui.GtkUi',):
    """Reload function for all base data witch is not dependant on a selected season or episode
    :param app: GtkUi instance
    :param builder: Gtk.Builder with loaded UI
    """
    # Rebuild all players store
    app.ui.get_object('all_players_store').clear()
    for player in app.players.data:
        app.ui.get_object('all_players_store').append([player.id, player.name, player.hex_id])
    # Rebuild drink store
        app.ui.get_object('drink_store').clear()
    for drink in app.drinks.data:
        app.ui.get_object('drink_store').append([drink.id, drink.name, '{:.2f}%'.format(drink.vol)])
    # Rebuild seasons store
    combo = app.ui.get_object('season_combo_box')  # type: Gtk.ComboBox
    active = combo.get_active()
    with util.block_handler(combo, app.handlers.do_season_selected):
        store = app.ui.get_object('seasons_store')
        store.clear()
        for season in app.seasons.data:
            store.append([season.id, season.game_name])
        combo.set_active(active)


def reload_episodes(app: 'gtk_ui.GtkUi'):
    """Reload all data that is dependant on a selected season
    :param app: GtkUi instance
    :param builder: Gtk.Builder with loaded UI
    """
    # Rebuild episodes store
    if not app.get_selected_season_id(): return
    selection = app.ui.get_object('episodes_tree_view').get_selection()
    with util.block_handler(selection, app.handlers.on_selected_episode_changed):
        model, selected_paths = selection.get_selected_rows()
        model.clear()
        for episode in app.episodes.data:
            model.append([episode.id, episode.name, str(episode.date), episode.number])
        if selected_paths:
            selection.select_path(selected_paths[0])


def reload_season_stats(app: 'gtk_ui.GtkUi'):
    """Load statistic data for selected season
    :param app: GtkUi instance
    """
    if not app.season_stats.valid: return
    season_stats = app.season_stats.data
    # Load player kill/death data
    store = app.ui.get_object('player_season_store')
    store.clear()
    for player_name, kills, deaths in season_stats.player_kd:
        store.append([player_name, deaths, kills])

    # Load enemy stats for season
    store = app.ui.get_object('enemy_season_store')
    store.clear()
    for enemy_id, enemy_name, deaths, defeated, boss in season_stats.enemies:
        store.append([enemy_name, defeated, deaths, boss, enemy_id])


def reload_episode_stats(app: 'gtk_ui.GtkUi'):
    """Reload all data that is dependant on a selected episode
    :param app: app: GtkUi instance
    """
    ep_id = app.get_selected_episode_id()
    if not app.episodes.valid or not ep_id: return
    episode = [ep for ep in app.episodes.data if ep.id == ep_id][0]
    store = app.ui.get_object('episode_players_store')
    store.clear()
    for player in episode.players:
        store.append([player.id, player.name, player.hex_id])
    # Reload death store for notebook view
    store = app.ui.get_object('episode_deaths_store')
    store.clear()
    for death in episode.deaths:
        penalties = [x.drink.name for x in death.penalties]
        penalties = ['{}x {}'.format(number, drink) for drink, number in Counter(penalties).items()]
        penalty_string = ', '.join(penalties)
        time_string = '{}:{}'.format(death.time.hour, death.time.minute)
        store.append([death.id, death.player.name, death.enemy.name, penalty_string, time_string])
    # Reload victory store for notebook view
    store = app.ui.get_object('episode_victories_store')
    store.clear()
    for victory in episode.victories:
        store.append([victory.id, victory.player.name, victory.enemy.name, victory.info])

    # Stat grid
    app.ui.get_object('ep_stat_title').set_text('Stats for episode {}\n{}'.format(episode.number, episode.name))
    app.ui.get_object('ep_death_count_label').set_text(str(len(episode.deaths)))
    drink_count = sum(len(death.penalties) for death in episode.deaths)
    app.ui.get_object('ep_drinks_label').set_text(str(drink_count))
    app.ui.get_object('ep_player_drinks_label').set_text(str(len(episode.deaths)))
    dl_booze = sum(len(death.penalties) * death.penalties[0].size for death in episode.deaths)
    l_booze = round(dl_booze / 10, 2)
    app.ui.get_object('ep_booze_label').set_text('{}l'.format(l_booze))
    dl_booze = sum(len(death.penalties) * death.penalties[0].size for death in episode.deaths)
    ml_booze = round(dl_booze * 10, 0)
    app.ui.get_object('ep_player_booze_label').set_text('{}ml'.format(ml_booze))
    enemy_list = [death.enemy.name for death in episode.deaths]
    sorted_list = Counter(enemy_list).most_common(1)
    if sorted_list:
        enemy_name, deaths = sorted_list[0]
        app.ui.get_object('ep_enemy_name_label').set_text('{} ({} Deaths)'.format(enemy_name, deaths))


def fill_list_store(store: Gtk.ListStore, models: list):
    store.clear()
    for model in models:
        pass


def rebuild_view_data(app: 'gtk_ui.GtkUi'):
    reload_base_data(app)
    reload_episodes(app)
    reload_episode_stats(app)
    reload_season_stats(app)

