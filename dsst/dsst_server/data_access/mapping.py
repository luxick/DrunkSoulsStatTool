from dsst_server.data_access import sql
from common import models


def map_base_fields(cls, db_model):
    """Automatically map fields of db models to common models
    :param cls: common.models class to create
    :param db_model: database model from which to map
    :return: An common.models object
    """
    model = cls()
    attrs = [attr for attr in db_model._meta.fields]
    for attr in attrs:
        db_attr = getattr(db_model, attr)
        # Check if the attribute is an relation to another db model
        # In that case just take its id
        if hasattr(db_attr, 'id'):
            setattr(model, attr, getattr(db_attr, 'id'))
        else:
            setattr(model, attr, getattr(db_model, attr))
    return model


def db_to_drink(drink: 'sql.Drink'):
    return map_base_fields(models.Drink, drink)


def db_to_enemy(enemy: 'sql.Enemy'):
    return map_base_fields(models.Enemy, enemy)


def db_to_player(player: 'sql.Player'):
    return map_base_fields(models.Player, player)


def db_to_penalty(penalty: 'sql.Penalty'):
    model = map_base_fields(models.Penalty, penalty)
    model.drink = db_to_drink(penalty.drink)
    model.player = db_to_player(penalty.player)
    return model


def db_to_death(death: 'sql.Death'):
    model = map_base_fields(models.Death, death)
    model.player = db_to_player(death.player)
    model.enemy = db_to_enemy(death.enemy)
    model.penalties = [db_to_penalty(penalty) for penalty in death.penalties]
    return model


def db_to_victory(victory: 'sql.Victory'):
    model = map_base_fields(models.Victory, victory)
    model.player = db_to_player(victory.player)
    model.enemy = db_to_enemy(victory.enemy)
    return model


def db_to_episode(episode: 'sql.Episode'):
    model = map_base_fields(models.Episode, episode)
    model.players = [db_to_player(player) for player in episode.players]
    model.deaths = [db_to_death(death) for death in episode.deaths]
    model.victories = [db_to_victory(victory) for victory in episode.victories]
    return model


def db_to_season(season: 'sql.Season'):
    model = map_base_fields(models.Season, season)
    model.enemies = [db_to_enemy(enemy) for enemy in season.enemies]
    model.episodes = [db_to_episode(ep) for ep in season.episodes]
    return model
