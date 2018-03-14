class Season:
    def __init__(self, arg={}):
        self.id = arg.get('id')
        self.number = arg.get('number')
        self.game_name = arg.get('game_name')
        self.start_date = arg.get('start_date')
        self.end_date = arg.get('end_date')

        self.episodes = arg.get('episodes')
        self.enemies = arg.get('enemies')


class Player:
    def __init__(self, arg={}):
        self.id = arg.get('id')
        self.name = arg.get('name')
        self.hex_id = arg.get('hex_id')
        
        self.deaths = arg.get('deaths')
        self.victories = arg.get('victories')
        self.penalties = arg.get('penalties')
        

class Episode:
    def __init__(self, arg={}):
        self.id = arg.get('id')
        self.seq_number = arg.get('seq_number')
        self.number = arg.get('number')
        self.name = arg.get('name')
        self.date = arg.get('date')
        self.season = arg.get('season')
        self.players = arg.get('players')
        self.deaths = arg.get('deaths')
        self.victories = arg.get('victories')


class Drink:
    def __init__(self, arg={}):
        self.id = arg.get('id')
        self.name = arg.get('name')
        self.vol = arg.get('vol')
        
        
class Enemy:
    def __init__(self, arg={}):
        self.id = arg.get('id')
        self.name = arg.get('name')
        self.boss = arg.get('boss')
        self.season = arg.get('season')


class Death:
    def __init__(self, arg={}):
        self.id = arg.get('id')
        self.info = arg.get('info')
        self.player = arg.get('player')
        self.enemy = arg.get('enemy')
        self.episode = arg.get('episode')
        self.penalties = arg.get('penalties')
        self.time = arg.get('time')


class Penalty:
    def __init__(self, arg={}):
        self.id = arg.get('id')
        self.size = arg.get('size')
        self.drink = arg.get('drink')
        self.player = arg.get('player')
        self.death = arg.get('death')


class Victory:
    def __init__(self, arg={}):
        self.id = arg.get('id')
        self.info = arg.get('info')
        self.player = arg.get('player')
        self.enemy = arg.get('enemy')
        self.episode = arg.get('episode')


class SeasonStats:
    def __init__(self, arg={}):
        self.player_kd = arg.get('player_kd')
        self.enemies = arg.get('enemies')
