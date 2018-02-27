from gi.repository import Gtk
from dsst_gtk3 import dialogs, gtk_ui


class DeathHandlers:
    """Callback handlers for signals related to managing death events"""
    def __init__(self, app: 'gtk_ui.GtkUi'):
        self.app = app

    def do_add_death(self, *_):
        ep_id = self.app.get_selected_episode_id()
        result = dialogs.show_edit_death_dialog(self.app.ui, ep_id)
        if result == Gtk.ResponseType.OK:
            self.app.reload_for_season()
            self.app.reload_for_episode()

    def on_penalty_drink_changed(self, widget, path, text):
        self.app.ui.get_object('player_penalties_store')[path][2] = text
