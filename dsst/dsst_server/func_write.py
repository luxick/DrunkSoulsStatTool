from common import models
from dsst_server.data_access import sql


class WriteFunctions:
    @staticmethod
    def create_season(season: 'models.Season'):
        return 'Season created.'

    @staticmethod
    def update_enemy(enemy: 'models.Enemy', *_):
        (sql.Enemy
         .insert(id=enemy.id, boss=enemy.boss, name=enemy.name, season=enemy.season)
         .on_conflict(update={sql.Enemy.name: enemy.name,
                              sql.Enemy.boss: enemy.boss,
                              sql.Enemy.season: enemy.season})
         .execute())

    @staticmethod
    def update_player(player: 'models.Player', *_):
        (sql.Player
         .insert(id=player.id, name=player.name, hex_id=player.hex_id)
         .on_conflict(update={sql.Player.name: player.name,
                              sql.Player.hex_id: player.hex_id})
         .execute())

    @staticmethod
    def update_drink(drink: 'models.Drink', *_):
        (sql.Drink
         .insert(id=drink.id, name=drink.name, vol=drink.vol)
         .on_conflict(update={sql.Drink.name: drink.name,
                              sql.Drink.vol: drink.vol})
         .execute())

    @staticmethod
    def save_death(death: 'models.Death'):
        with sql.db.atomic():
            created_id = (sql.Death
                          .insert(info=death.info, player=death.player, enemy=death.enemy, episode=death.episode,
                                  time=death.time)
                          .execute())
            for penalty in death.penalties:
                sql.Penalty.create(death=created_id, size=penalty.size, drink=penalty.drink, player=penalty.player)

    @staticmethod
    def save_victory(victory: 'models.Victory'):
        (sql.Victory
         .insert(info=victory.info, player=victory.player, enemy=victory.enemy, time=victory.time,
                 episode=victory.episode, id=victory.id)
         .execute())

    @staticmethod
    def update_season(season: 'models.Season', *_):
        (sql.Season
         .insert(id=season.id, number=season.number, game_name=season.game_name, start_date=season.start_date,
                 end_date=season.end_date)
         .on_conflict(
            update={sql.Season.number: season.number,
                    sql.Season.game_name: season.game_name,
                    sql.Season.start_date: season.start_date,
                    sql.Season.end_date: season.end_date})
         .execute())

    @staticmethod
    def update_episode(episode: 'models.Episode', *_):
        players = list(sql.Player.select().where(sql.Player.id << [player.id for player in episode.players]))
        new_ep_id = (sql.Episode
                     .insert(id=episode.id, number=episode.number, seq_number=episode.number, name=episode.name,
                             date=episode.date, season=episode.season)
                     .on_conflict(update={sql.Episode.name: episode.name,
                                          sql.Episode.seq_number: episode.seq_number,
                                          sql.Episode.number: episode.number,
                                          sql.Episode.date: episode.date,
                                          sql.Episode.season: episode.season})
                     .execute())
        db_episode = sql.Episode.get(sql.Episode.id == new_ep_id)
        db_episode.players = players
        db_episode.save()
