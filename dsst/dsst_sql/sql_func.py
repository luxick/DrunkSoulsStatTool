from dsst_sql.sql import *


def get_episodes_for_season(season_id):
    try:
        return list(Season.get(Season.id == season_id).episodes)
    except Episode.DoesNotExist:
        return []


def get_player_deaths_for_season(season_id: int, player_id: int) -> int:
    deaths = 0
    for episode in list(Season.get(Season.id == season_id).episodes):
        deaths = deaths + len([death for death in list(episode.deaths) if death.player.id == player_id])
    return deaths


def get_player_victories_for_season(season_id: int, player_id: int) -> int:
    victories = 0
    for episode in list(Season.get(Season.id == season_id).episodes):
        victories = victories + len([vic for vic in list(episode.victories) if vic.player.id == player_id])
    return victories
