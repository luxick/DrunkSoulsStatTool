from dsst_server.data_access import sql, sql_func, mapping
from common import models
from playhouse import shortcuts


class ReadFunctions:
    @staticmethod
    def load_db_meta(*_):
        return sql.db.database

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
    def load_enemies(season_id, *_):
        pass

    @staticmethod
    def load_drinks(*_):
        return [mapping.db_to_drink(drink) for drink in sql.Drink.select()]

    @staticmethod
    def load_season_stats(season_id, *_):
        season = sql.Season.get(sql.Season.id == season_id)
        players = sql_func.players_for_season(season_id)
        model = models.SeasonStats()
        model.player_kd = [(player.name,
                            sql_func.get_player_victories_for_season(season_id, player.id),
                            sql_func.get_player_deaths_for_season(season_id, player.id))
                           for player in players]
        model.enemies = [(enemy.id,
                          enemy.name,
                          sql_func.enemy_attempts(enemy.id),
                          sql.Victory.select().where(sql.Victory.enemy == enemy.id).exists(),
                          enemy.boss)
                         for enemy in season.enemies]
        return model
