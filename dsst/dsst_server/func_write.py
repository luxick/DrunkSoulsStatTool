from common import models
from dsst_server.data_access import sql


class WriteFunctions:
    @staticmethod
    def create_season(season: 'models.Season'):
        return 'Season created.'

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
