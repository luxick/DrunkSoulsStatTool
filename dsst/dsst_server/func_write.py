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
