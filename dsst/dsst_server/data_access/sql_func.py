"""
This module contains shorthand functions for common queries to ease access from the UI
"""
from dsst_server.data_access import sql


def get_episodes_for_season(season_id: int) -> list:
    """Load list of episodes for a specific season
    :param season_id: ID of a season
    :return: List of sql.Episode or empty list
    """
    try:
        return list(sql.Season.get(sql.Season.id == season_id).episodes)
    except sql.Episode.DoesNotExist:
        return []


def get_player_deaths_for_season(season_id: int, player_id: int) -> int:
    """Load all the aggregate count of all deaths for a player in a given season
    :param season_id: ID of a season
    :param player_id: ID of a player
    :return: Number of deaths of the player in the season
    """
    deaths = 0
    for episode in list(sql.Season.get(sql.Season.id == season_id).episodes):
        deaths = deaths + len([death for death in list(episode.deaths) if death.player.id == player_id])
    return deaths


def get_player_victories_for_season(season_id: int, player_id: int) -> int:
    """Load all the aggregate count of all victories for a player in a given season
    :param season_id: ID of a season
    :param player_id: ID of a player
    :return: Number of all victories of the player in the season
    """
    victories = 0
    for episode in list(sql.Season.get(sql.Season.id == season_id).episodes):
        victories = victories + len([vic for vic in list(episode.victories) if vic.player.id == player_id])
    return victories


def players_for_season(season_id: int) -> set:
    season_eps = list(sql.Season.get(sql.Season.id == season_id).episodes)
    players = set()
    for ep in season_eps:
        players.update([player for player in ep.players])
    return players


def enemy_attempts(enemy_id: int) -> int:
    return sql.Death.select().where(sql.Death.enemy == enemy_id).count()


def create_tables():
    """Create all database tables"""
    models = [sql.Season, sql.Episode, sql.Player, sql.Drink, sql.Enemy, sql.Death, sql.Victory, sql.Penalty,
              sql.Episode.players.get_through_model()]
    for model in models:
        model.create_table()


def drop_tables():
    """Drop all data in database"""
    models = [sql.Season, sql.Episode, sql.Player, sql.Drink, sql.Enemy, sql.Death, sql.Victory, sql.Penalty,
              sql.Episode.players.get_through_model()]
    sql.db.drop_tables(models)