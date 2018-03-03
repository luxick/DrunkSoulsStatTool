from dsst_server.data_access import sql
from common import models


def map_base_fields(cls, db_model):
    model = cls()
    attrs = [attr for attr in db_model._meta.fields]
    for attr in attrs:
        setattr(model, attr, getattr(db_model, attr))
    return model


def db_to_enemy(enemy: 'sql.Enemy'):
    return map_base_fields(models.Enemy, enemy)


def db_to_player(player: 'sql.Player'):
    model = map_base_fields(models.Player, player)
    return model


def db_to_episode(episode: 'sql.Episode'):
    model = map_base_fields(models.Episode, episode)
    model.players = [db_to_player(player) for player in episode.players]
    model.deaths = []
    model.victories = []


def db_to_season(season: 'sql.Season'):
    model = map_base_fields(models.Season, season)
    model.enemies = [db_to_enemy(enemy) for enemy in season.enemies]
    model.episodes = [db_to_episode(ep) for ep in season.episodes]
    return model
