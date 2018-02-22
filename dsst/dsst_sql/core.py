from dsst_sql import models, sql


class DSSTCore:
    def __init__(self):
        # Set DB Connection
        sql.create_tables()

    @staticmethod
    def insert_player(model: models.Player):
        return sql.Player.create(name=model.name, hex_id=model.hex_id)

    @staticmethod
    def insert_enemy(enemy: models.Enemy):
        return sql.Enemy.create(name=enemy.name)

    @staticmethod
    def insert_drink(model: models.Drink):
        return sql.Drink.create(name=model.name, vol=model.vol)

    @staticmethod
    def insert_season(season: models.Season):
        return sql.Season.create(number=season.number, game_name=season.game_name, start_date=season.start_date,
                                 end_date=season.end_date)

    @staticmethod
    def insert_death(death: models.Death):
        return sql.Death.create(info=death.info, player=death.player.id, enemy=death.enemy.id, penalty=death.penalty.id)

    @staticmethod
    def insert_victory(victory: models.Victory):
        return sql.Death.create(info=victory.info, player=victory.player.id, enemy=victory.enemy.id)

    @staticmethod
    def insert_episode(season_id: int, episode: models.Episode):
        with sql.connection.atomic():
            # Insert Episode Row
            new_ep = sql.Episode.create(seq_number=episode.seq_number, number=episode.number, date=episode.date,
                                        season=season_id)
            # Insert participating players
            for player in episode.players:
                sql.EpisodePlayer.insert(episode=new_ep.id, player=player.id)
            # Insert deaths in this episode
            if episode.deaths:
                for death in episode.deaths:
                    new_death = DSSTCore.insert_death(death)
                    sql.EpisodeDeath.create(death=new_death.id, episode=new_ep.id)
            # Insert victories in this episode
            if episode.victories:
                for victory in episode.victories:
                    new_vic = DSSTCore.insert_victory(victory)
                    sql.EpisodeVictory.create(victory=new_vic.id, episode=new_ep.id)


if __name__ == '__main__':
    core = DSSTCore()