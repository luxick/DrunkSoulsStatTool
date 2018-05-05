from gi.repository import Gtk
from dsst_gtk3 import dialogs, gtk_ui, util


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
            self.app.data_client.save_victory(victory)

    def victory_tree_clicked(self, widget, event):
        if event.button == 3:  # right click
            popup = self.app.ui.get_object('p_victory')
            util.show_context_menu(widget, event, popup)
            return True

    def do_delete_victory(self, *_):
        victory_id = util.get_tree_selection_value(self.app.ui.get_object('episode_victories_tree_view'), 0)
        self.app.data_client.delete_victory(victory_id)
