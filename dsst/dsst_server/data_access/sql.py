"""
This module contains the ORM class definitions for peewee.
To access the database import this module an run queries on the classes
Example:
from sql import Episode
query = Episode.select().where(Episode.name == 'MyName')
"""
import sys
import datetime

try:
    from peewee import *
except ImportError:
    print('peewee package not installed')
    sys.exit(0)

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
    name = CharField(null=True)
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
    boss = BooleanField()
    season = ForeignKeyField(Season, backref='enemies')

    class Meta:
        database = db


class Death(Model):
    id = AutoField()
    info = CharField(null=True)
    time = TimeField(default=datetime.time(0, 0))
    player = ForeignKeyField(Player)
    enemy = ForeignKeyField(Enemy)
    episode = ForeignKeyField(Episode, backref='deaths')

    class Meta:
        database = db


class Penalty(Model):
    id = AutoField()
    size = DecimalField()
    drink = ForeignKeyField(Drink)
    player = ForeignKeyField(Player, backref='penalties')
    death = ForeignKeyField(Death, backref='penalties')

    class Meta:
        database = db


class Victory(Model):
    id = AutoField()
    info = CharField(null=True)
    time = TimeField(default=datetime.time(0, 0))
    player = ForeignKeyField(Player)
    enemy = ForeignKeyField(Enemy)
    episode = ForeignKeyField(Episode, backref='victories')

    class Meta:
        database = db
