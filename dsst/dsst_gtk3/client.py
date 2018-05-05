import pprint
import socket
from common import util, models
try:
    import cPickle as pickle
except ImportError:
    import pickle
from dsst_gtk3 import gtk_ui


def gui_handled(func):
    def wrapper(*args, **kwargs):
        self.app.ui.get_object('status_bar').push(0, 'Connecting to server')
        try:
            yield func(*args, **kwargs)
        except Exception as e:
            print(e)
            self.app.ui.get_object('status_bar').push(0, str(e))
        else:
            self.app.ui.get_object('status_bar').push(0, '')
            self.app.full_reload()

    return wrapper

class DataClient:
    def __init__(self, app: 'gtk_ui.GtkUi', conn_dict):
        self.app = app
        self.host = conn_dict.get('host')
        self.port = conn_dict.get('port')
        self.buffer = conn_dict.get('buffer_size')
        self.auth_token = conn_dict.get('auth_token')

    def send_request(self, action: str, *args):
        request = {'auth_token': self.auth_token,
                   'action': action,
                   'args': args}
        request = pickle.dumps(request)
        soc = socket.socket()
        try:
            soc.connect((self.host, self.port))
            util.send_msg(soc, request)
            message = util.recv_msg(soc)
            message = pickle.loads(message)
            if not message.get('success'):
                raise Exception(message.get('message'))
        finally:
            soc.close()
        return message.get('data')



    @gui_handled
    def update_enemy(self, enemy: 'models.Enemy'):
        self.send_request('update_enemy', enemy)

    def update_player(self, player: 'models.Player'):
        self.send_request('update_player', player)

    def update_drink(self, drink: 'models.Drink'):
        self.send_request('update_drink', drink)

    def save_death(self, death: 'models.Death'):
        self.send_request('save_death', death)

    def delete_death(self, death_id: int):
        with util.network_operation(self):
            self.data_client.send_request('delete_death', death_id)
        self.full_reload()

    def save_victory(self, victory: 'models.Victory'):
        with util.network_operation(self):
            self.data_client.send_request('save_victory', victory)
        self.full_reload()

    def delete_victory(self, victory_id: int):
        with util.network_operation(self):
            self.data_client.send_request('delete_victory', victory_id)
        self.full_reload()

    def update_season(self, season: 'models.Season'):
        with util.network_operation(self):
            self.data_client.send_request('update_season', season)
            self.seasons.valid = False

    def update_episode(self, episode: 'models.Episode'):
        with util.network_operation(self):
            self.data_client.send_request('update_episode', episode)
            self.episodes.valid = False
            self.season_stats.valid = False

if __name__ == '__main__':
    access = DataClient({'host': 'europa', 'port': 12345, 'buffer_size': 1024, 'auth_token': 'a'})
    action = 'load_seasons'
    response = access.send_request(action)
    pp = pprint.PrettyPrinter(indent=1)
    for s in response:
        pp.pprint(s.__dict__)
import pprint
import socket
from common import util, models
from functools import wraps
try:
    import cPickle as pickle
except ImportError:
    import pickle
from dsst_gtk3 import gtk_ui


def reload_after_update(method):
    """ Method decorator to handle GUI while updating data.
    Adds error display in case of an exception and causes data reloading after an successful change.
    :param method: The method to decorate
    :return: The decorated function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Set info in statusbar
        self.app.ui.get_object('status_bar').push(0, 'Connecting to server')
        try:
            method(self, *args, **kwargs)
        except Exception as e:
            print(e)
            self.app.ui.get_object('status_bar').push(0, str(e))
        else:
            self.app.ui.get_object('status_bar').push(0, '')
            # Cause local data to be reloaded, if method was executed successfully
            self.app.full_reload()
    return wrapper


class DataClient:
    """ The access class for reading and writing data from and to the dsst API """
    def __init__(self, app: 'gtk_ui.GtkUi', conn_dict):
        self.app = app
        self.host = conn_dict.get('host')
        self.port = conn_dict.get('port')
        self.buffer = conn_dict.get('buffer_size')
        self.auth_token = conn_dict.get('auth_token')

    def send_request(self, action: str, *args):
        request = {'auth_token': self.auth_token,
                   'action': action,
                   'args': args}
        request = pickle.dumps(request)
        soc = socket.socket()
        try:
            soc.connect((self.host, self.port))
            util.send_msg(soc, request)
            message = util.recv_msg(soc)
            message = pickle.loads(message)
            if not message.get('success'):
                raise Exception(message.get('message'))
        finally:
            soc.close()
        return message.get('data')

    @reload_after_update
    def update_enemy(self, enemy: 'models.Enemy'):
        self.send_request('update_enemy', enemy)

    @reload_after_update
    def update_player(self, player: 'models.Player'):
        self.send_request('update_player', player)

    @reload_after_update
    def update_drink(self, drink: 'models.Drink'):
        self.send_request('update_drink', drink)

    @reload_after_update
    def save_death(self, death: 'models.Death'):
        self.send_request('save_death', death)

    @reload_after_update
    def delete_death(self, death_id: int):
        self.send_request('delete_death', death_id)

    @reload_after_update
    def save_victory(self, victory: 'models.Victory'):
        self.send_request('save_victory', victory)

    @reload_after_update
    def delete_victory(self, victory_id: int):
        self.send_request('delete_victory', victory_id)

    @reload_after_update
    def update_season(self, season: 'models.Season'):
        self.send_request('update_season', season)

    @reload_after_update
    def update_episode(self, episode: 'models.Episode'):
        self.send_request('update_episode', episode)
