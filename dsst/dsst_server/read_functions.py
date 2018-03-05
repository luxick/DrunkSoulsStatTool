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
    def load_episodes(season_id, *_):
        if not season_id:
            raise Exception('Exception: Missing argument (season_id)')
        return [mapping.db_to_episode(ep) for ep in sql.Season.get(sql.Season.id == season_id).episodes]

    @staticmethod
    def load_players(*_):
        return [mapping.db_to_player(player) for player in sql.Player.select()]

    @staticmethod
    def load_drinks(*_):
        return [mapping.db_to_drink(drink) for drink in sql.Drink.select()]