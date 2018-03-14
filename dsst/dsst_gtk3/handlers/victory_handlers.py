from gi.repository import Gtk
from dsst_gtk3 import dialogs, gtk_ui


class VictoryHandlers:
    """Callback handlers for signals related to managing victory events"""
    def __init__(self, app: 'gtk_ui.GtkUi'):
        self.app = app

    def do_add_victory(self, *_):
        ep_id = self.app.get_selected_episode_id()
        if not ep_id:
            return
        victory = dialogs.create_victory(self.app)
        if victory:
            self.app.save_victory(victory)
