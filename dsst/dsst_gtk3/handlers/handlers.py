import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from dsst_gtk3.handlers.season_handlers import SeasonHandlers
from dsst_gtk3.handlers.base_data_handlers import BaseDataHandlers
from dsst_gtk3.handlers.dialog_handlers import DialogHandlers
from dsst_gtk3.handlers.death_handlers import DeathHandlers
from dsst_gtk3.handlers.victory_handlers import VictoryHandlers
from dsst_sql import sql_func


class Handlers(SeasonHandlers, BaseDataHandlers, DialogHandlers, DeathHandlers, VictoryHandlers):
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
        VictoryHandlers.__init__(self, app)

    @staticmethod
    def do_delete_event(*_):
        """ Signal will be sent when app should close
        :param _: Arguments to the delete event
        """
        Gtk.main_quit()

    # DEBUG Functions ##################################################################################################

    @staticmethod
    def do_delete_database(*_):
        sql_func.drop_tables()
        sql_func.create_tables()
