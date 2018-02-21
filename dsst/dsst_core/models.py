class Season:
    def __init__(self, arg={}):
        self.id = arg.get('id')
        self.game_name = arg.get('game_name')
        self.number = arg.get('number')
        self.start_date = arg.get('start_date')
        self.end_date = arg.get('end_date')

        self.players = arg.get('players')
        self.enemies = arg.get('enemies')
        self.episodes = arg.get('episodes')


class Episode:
    def __init__(self, arg={}):
        self.id = arg.get('id')
        self.seq_number = arg.get('seq_number')
        self.number = arg.get('number')
        self.date = arg.get('date')

        self.players = arg.get('players')
        self.enemies = arg.get('enemies')
        self.deaths = arg.get('deaths')
        self.victories = arg.get('victories')


class GameEvent:
    def __init__(self, arg={}):
        self.id = arg.get('id')
        self.player = arg.get('player')
        self.enemy = arg.get('enemy')
        self.info = arg.get('info')


class Death(GameEvent):
    def __init__(self, arg={}):
        GameEvent.__init__(self, arg)
        self.penalty = arg.get('penalty')


class Victory(GameEvent):
    def __init__(self, arg={}):
        GameEvent.__init__(self, arg)


class Player:
    def __init__(self, arg={}):
        self.id = arg.get('id')
        self.name = arg.get('name')
        self.hex_id = arg.get('hex_id')


class Enemy:
    def __init__(self, arg={}):
        self.id = arg.get('id')
        self.name = arg.get('name')


class Drink:
    def __init__(self, arg={}):
        self.id = arg.get('id')
        self.name = arg.get('name')
        self.vol = arg.get('vol')