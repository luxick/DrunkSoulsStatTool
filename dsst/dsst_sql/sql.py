from peewee import *

connection = MySQLDatabase('dsst', user='dsst', password='dsst')


class Season(Model):
    id = AutoField()
    number = IntegerField()
    game_name = CharField()
    start_date = DateField(null=True)
    end_date = DateField(null=True)

    class Meta:
        database = connection


class Episode(Model):
    id = AutoField()
    seq_number = IntegerField()
    number = CharField()
    date = DateTimeField(null=True)
    season = ForeignKeyField(Season, backref='episodes')

    class Meta:
        database = connection


class Player(Model):
    id = AutoField()
    name = CharField()
    hex_id = CharField(null=True)

    class Meta:
        database = connection


class Drink(Model):
    id = AutoField()
    name = CharField()
    vol = DecimalField()

    class Meta:
        database = connection


class Enemy(Model):
    id = AutoField()
    name = CharField()

    class Meta:
        database = connection


class Death(Model):
    id = AutoField()
    info = CharField(null=True)
    player = ForeignKeyField(Player)
    enemy = ForeignKeyField(Enemy)
    penalty = ForeignKeyField(Drink)

    class Meta:
        database = connection


class Victory(Model):
    id = AutoField()
    info = CharField(null=True)
    player = ForeignKeyField(Player)
    enemy = ForeignKeyField(Enemy)

    class Meta:
        database = connection


class EpisodePlayer(Model):
    id = AutoField()
    episode = ForeignKeyField(Episode)
    player = ForeignKeyField(Player)

    class Meta:
        database = connection


class EpisodeDeath(Model):
    id = AutoField()
    episode = ForeignKeyField(Episode)
    death = ForeignKeyField(Death)

    class Meta:
        database = connection


class EpisodeVictory(Model):
    id = AutoField()
    episode = ForeignKeyField(Episode)
    victory = ForeignKeyField(Victory)

    class Meta:
        database = connection


def create_tables():
    models = [Season, Episode, Player, Drink, Enemy, Death, Victory, EpisodePlayer, EpisodeDeath,
              EpisodeVictory]
    for model in models:
        model.create_table()


