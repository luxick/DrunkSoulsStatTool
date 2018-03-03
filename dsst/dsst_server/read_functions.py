from dsst_server.data_access import sql, sql_func, mapping
from common import models
from playhouse import shortcuts


class ReadFunctions:

    @staticmethod
    def load_seasons(*_):
        return [mapping.db_to_season(season) for season in sql.Season.select()]

    @staticmethod
    def load_seasons_all(*_):
        return [shortcuts.model_to_dict(season, backrefs=True, max_depth=2) for season in sql.Season.select()]

    @staticmethod
    def load_players(*_):
        return [mapping.db_to_player(player) for player in sql.Player.select()]

