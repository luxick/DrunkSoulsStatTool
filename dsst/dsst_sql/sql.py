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


class Player(Model):
    id = AutoField()
    name = CharField()
    hex_id = CharField(null=True)

    class Meta:
        database = connection


class Episode(Model):
    id = AutoField()
    seq_number = IntegerField()
    number = CharField()
    date = DateField(null=True)
    season = ForeignKeyField(Season, backref='episodes')
    players = ManyToManyField(Player, backref='episodes')

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
    season = ForeignKeyField(Season, backref='enemies')

    class Meta:
        database = connection


class Death(Model):
    id = AutoField()
    info = CharField(null=True)
    player = ForeignKeyField(Player)
    enemy = ForeignKeyField(Enemy)
    episode = ForeignKeyField(Episode, backref='deaths')

    class Meta:
        database = connection


class Penalty(Model):
    id = AutoField()
    size = DecimalField()
    ForeignKeyField(Drink)
    ForeignKeyField(Player, backref='penalties')
    ForeignKeyField(Death, backref='penalties')

    class Meta:
        database = connection


class Victory(Model):
    id = AutoField()
    info = CharField(null=True)
    player = ForeignKeyField(Player)
    enemy = ForeignKeyField(Enemy)
    episode = ForeignKeyField(Episode, backref='victories')

    class Meta:
        database = connection


def create_tables():
    models = [Season, Episode, Player, Drink, Enemy, Death, Victory, Penalty, Episode.players.get_through_model()]
    for model in models:
        model.create_table()


def drop_tables():
    models = [Season, Episode, Player, Drink, Enemy, Death, Victory, Penalty, Episode.players.get_through_model()]
    connection.drop_tables(models)
