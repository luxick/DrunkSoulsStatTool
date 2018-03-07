from gi.repository import Gtk
from dsst_gtk3 import dialogs


class VictoryHandlers:
    """Callback handlers for signals related to managing victory events"""
    def __init__(self, app: 'gtk_ui.GtkUi'):
        self.app = app

    def do_add_victory(self, *_):
        ep_id = self.app.get_selected_episode_id()
        if not ep_id:
            return
        result = dialogs.show_edit_victory_dialog(self.app.ui, ep_id)
        if result == Gtk.ResponseType.OK:
            self.app.reload()
