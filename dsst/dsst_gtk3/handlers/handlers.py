import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from dsst_gtk3.handlers.left_column_handlers import LeftColumnHandlers
from dsst_gtk3.handlers.players import PlayerHandlers
from dsst_gtk3.handlers.dialog_handlers import DialogHandlers
from dsst_gtk3.handlers.center_handlers import CenterHandlers

from dsst_sql import sql


class Handlers(LeftColumnHandlers, PlayerHandlers, DialogHandlers, CenterHandlers):
    """ Class containing all signal handlers for the GTK GUI """
    def __init__(self, app):
        """ Initialize handler class
        :param app: reference to the main application object
        """
        self.app = app
        # Call constructors of superclasses
        LeftColumnHandlers.__init__(self, app)
        PlayerHandlers.__init__(self, app)
        DialogHandlers.__init__(self, app)
        CenterHandlers.__init__(self, app)

    @staticmethod
    def do_delete_event(*args):
        """ Signal will be sent when app should close
        :param args: Arguments to the delete event
        """
        Gtk.main_quit()

    # DEBUG Functions ##################################################################################################

    @staticmethod
    def do_delete_database(*_):
        sql.drop_tables()
        sql.create_tables()