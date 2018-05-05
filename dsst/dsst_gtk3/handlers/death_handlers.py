from gi.repository import Gtk
from dsst_gtk3 import dialogs, gtk_ui, util


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
            self.app.data_client.save_death(death)

    def on_penalty_drink_changed(self, _, path, text):
        self.app.ui.get_object('player_penalties_store')[path][2] = text

    def death_tree_clicked(self, widget, event):
        if event.button == 3:  # right click
            popup = self.app.ui.get_object('p_death')
            util.show_context_menu(widget, event, popup)
            return True

    def do_delete_death(self, *_):
        death_id = util.get_tree_selection_value(self.app.ui.get_object('episode_deaths_tree_view'), 0)
        self.app.data_client.delete_death(death_id)

