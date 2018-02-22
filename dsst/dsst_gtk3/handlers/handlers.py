import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from dsst_gtk3.handlers.season_and_episodes import SeasonAndEpisodesHandlers
from dsst_gtk3.handlers.players import PlayerHandlers


class Handlers(SeasonAndEpisodesHandlers, PlayerHandlers):
    """ Class containing all signal handlers for the GTK GUI """
    def __init__(self, app):
        """ Initialize handler class
        :param app: reference to the main application object
        """
        self.app = app
        # Call constructors of superclasses
        SeasonAndEpisodesHandlers.__init__(self, app)
        PlayerHandlers.__init__(self, app)

    @staticmethod
    def do_delete_event(*args):
        """ Signal will be sent when app should close
        :param args: Arguments to the delete event
        """
        Gtk.main_quit()