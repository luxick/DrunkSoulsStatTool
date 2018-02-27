import gi
import sql_func
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from dsst_gtk3.handlers.season_handlers import SeasonHandlers
from dsst_gtk3.handlers.base_data_handlers import BaseDataHandlers
from dsst_gtk3.handlers.dialog_handlers import DialogHandlers
from dsst_gtk3.handlers.death_handlers import DeathHandlers


class Handlers(SeasonHandlers, BaseDataHandlers, DialogHandlers, DeathHandlers):
    """Single callback handler class derived from specialized handler classes"""
    def __init__(self, app):
        """ Initialize handler class
        :param app: reference to the main application object
        """
        self.app = app
        # Call constructors of superclasses
        SeasonHandlers.__init__(self, app)
        BaseDataHandlers.__init__(self, app)
        DialogHandlers.__init__(self, app)
        DeathHandlers.__init__(self, app)

    @staticmethod
    def do_delete_event(*args):
        """ Signal will be sent when app should close
        :param args: Arguments to the delete event
        """
        Gtk.main_quit()

    # DEBUG Functions ##################################################################################################

    @staticmethod
    def do_delete_database(*_):
        sql_func.drop_tables()
        sql_func.create_tables()