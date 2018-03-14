from gi.repository import Gtk
from dsst_gtk3 import dialogs, gtk_ui


class DeathHandlers:
    """Callback handlers for signals related to managing death events"""
    def __init__(self, app: 'gtk_ui.GtkUi'):
        self.app = app

    def do_add_death(self, *_):
        ep_id = self.app.get_selected_episode_id()
        if not ep_id:
            return
        death = dialogs.create_death(self.app)
        if death:
            self.app.save_death(death)

    def on_penalty_drink_changed(self, _, path, text):
        self.app.ui.get_object('player_penalties_store')[path][2] = text
