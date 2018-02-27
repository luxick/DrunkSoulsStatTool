"""
This module contains the ORM class definitions for peewee.
To access the database import this module an run queries on the classes
Example:
from sql import Episode
query = Episode.select().where(Episode.name == 'MyName')
"""

from peewee import *

db = MySQLDatabase(None)


class Season(Model):
    id = AutoField()
    number = IntegerField()
    game_name = CharField()
    start_date = DateField(null=True)
    end_date = DateField(null=True)

    class Meta:
        database = db


class Player(Model):
    id = AutoField()
    name = CharField()
    hex_id = CharField(null=True)

    class Meta:
        database = db


class Episode(Model):
    id = AutoField()
    seq_number = IntegerField()
    number = CharField()
    date = DateField(null=True)
    season = ForeignKeyField(Season, backref='episodes')
    players = ManyToManyField(Player, backref='episodes')

    class Meta:
        database = db


class Drink(Model):
    id = AutoField()
    name = CharField()
    vol = DecimalField()

    class Meta:
        database = db


class Enemy(Model):
    id = AutoField()
    name = CharField()
    season = ForeignKeyField(Season, backref='enemies')

    class Meta:
        database = db


class Death(Model):
    id = AutoField()
    info = CharField(null=True)
    player = ForeignKeyField(Player)
    enemy = ForeignKeyField(Enemy)
    episode = ForeignKeyField(Episode, backref='deaths')

    class Meta:
        database = db


class Penalty(Model):
    id = AutoField()
    size = DecimalField()
    ForeignKeyField(Drink)
    ForeignKeyField(Player, backref='penalties')
    ForeignKeyField(Death, backref='penalties')

    class Meta:
        database = db


class Victory(Model):
    id = AutoField()
    info = CharField(null=True)
    player = ForeignKeyField(Player)
    enemy = ForeignKeyField(Enemy)
    episode = ForeignKeyField(Episode, backref='victories')

    class Meta:
        database = db
