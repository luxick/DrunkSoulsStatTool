import datetime
from dsst_core import models, sql


class DSSTCore:
    def __init__(self):
        # Set DB Connection
        sql.create_tables()

    @staticmethod
    def insert_player(model: models.Player):
        sql.Player.create(name=model.name, hex_id=model.hex_id)

    @staticmethod
    def insert_enemy(enemy: models.Enemy):
        sql.Enemy.create(name=enemy.name)

    @staticmethod
    def insert_drink(model: models.Drink):
        sql.Drink.create(name=model.name, vol=model.vol)

    @staticmethod
    def insert_season(season: models.Season):
        sql.Season.create(number=season.number, game_name=season.game_name, start_date=season.start_date,
                          end_date=season.end_date)

    @staticmethod
    def insert_episode(episode: models.Episode):
        sql.Episode.update()

if __name__ == '__main__':
    core = DSSTCore()
    # Insert player
    # player = models.Player()
    # player.name = 'Marvin'
    # core.insert_player(player)

    # Insert a Season
    # season = models.Season()
    # season.number = 1
    # season.game_name = 'Dark Souls'
    # season.start_date = datetime.date(2017, 1, 1)
    # core.insert_season(season)

    # core.insert_drink(models.Drink({'name': 'Pfeffi', 'vol': 22.5}))

    # core.insert_enemy(models.Enemy({'name': 'Newton'}))

    # Insert an episode
    ep = models.Episode()
    ep.date = datetime.date(2017, 2, 5)
    ep.number = 1
    ep.seq_number = 1
    ep.players = [models.Player({'id': 1,}), models.Player({'id': 2})]
    ep.deaths = [models.Death({
        'player': 1,
        'enemy': 1,
        'penalty': 1,
    })]
