"""
This modules contains general utilities for the GTK application to use.
"""
import json
import os
from contextlib import contextmanager
from gi.repository import Gtk, GdkPixbuf
from typing import Callable
from dsst_gtk3 import gtk_ui
from zipfile import ZipFile

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'dsst', 'config.json')
DEFAULT_CONFIG = {
    'auto_connect': False,
    'servers': [{
        'host': 'localhost',
        'port': 55225,
        'buffer_size': 1024,
        'auth_token': ''}
    ]
}


class Cache:
    def __init__(self, data={}, valid=False):
        self._data = data
        self.valid = valid

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.valid = True


@contextmanager
def block_handler(widget: 'Gtk.Widget', handler_func: Callable):
    """Run an operation while a signal handler for a widget is blocked
    :param widget: A Gtk widget
    :param handler_func: Signal handler of the widget to block
    """
    widget.handler_block_by_func(handler_func)
    yield
    widget.handler_unblock_by_func(handler_func)


@contextmanager
def network_operation(app: 'gtk_ui.GtkUi'):
    """Run operation in try/except block and display exception in a dialog
    :param app: Reference to main Gtk Application
    """
    app.ui.get_object('status_bar').push(0, 'Connecting to server')
    try:
        yield
    except Exception as e:
        print(e)
        app.ui.get_object('status_bar').push(0, str(e))
    else:
        app.ui.get_object('status_bar').push(0, '')


def get_combo_value(combo, index: int):
    """ Retrieve the selected value of a combo box at the selected index in the model
    :param combo: Any Gtk Widget that supports 'get_active_iter()'
    :param index: Index of the value in the widgets model to be retrieved
    :return: The value of the model at the selected index (Default -1)
    """
    tree_iter = combo.get_active_iter()
    if tree_iter:
        return combo.get_model().get_value(tree_iter, index)
    else:
        return -1


def get_tree_selection_value(tree: 'Gtk.TreeView', column: int):
    """ Retrieve the a cell value of a tree view based on selected row and the choosen column
    :param tree: Gtk.TreeView widget
    :param column: Number of the column from which to retrieve the value
    """
    (model, pathlist) = tree.get_selection().get_selected_rows()
    for path in pathlist:
        tree_iter = model.get_iter(path)
        return model.get_value(tree_iter, 0)


def get_index_of_combo_model(widget, column: int, value: int):
    """Get the index of a value within a Gtk widgets model based on column an value
    :param widget: Any Gtk widget that can be bound to a ListStore or TreeStore
    :param column: Column in the model where to look for the value
    :param value: Value to look for in the model
    :return: List of the indexes where the value occurs
    """
    model = widget.get_model()
    return [model.index(entry) for entry in model if entry[column] == value]


def load_ui_resource_from_file(resource_path: list) -> str:
    project_base_dir = os.path.dirname(os.path.dirname(__file__))
    full_path = os.path.join(project_base_dir, *resource_path)
    with open(full_path, 'r', encoding='utf8') as file:
        return file.read()


def load_ui_resource_from_archive(resource_path: list) -> str:
    zip_path = os.path.dirname(os.path.dirname(__file__))
    with ZipFile(zip_path, 'r') as archive:
        return archive.read(str(os.path.join(*resource_path))).decode('utf-8')


def load_ui_resource_string(resource_path: list) -> str:
    """ Load content of Glade UI files from resources path
    :param resource_path: List of directory names from 'dsst' base directory
    :return: String content of the Glade file
    """
    if os.path.isdir(os.path.dirname(__file__)):
        return load_ui_resource_from_file(resource_path)
    else:
        return load_ui_resource_from_archive(resource_path)


def load_image_resource_file(resource_path: list, width: int, height: int) -> GdkPixbuf:
    project_base_dir = os.path.dirname(os.path.dirname(__file__))
    full_path = os.path.join(project_base_dir, *resource_path)
    return GdkPixbuf.Pixbuf.new_from_file_at_scale(full_path, width=width, height=height, preserve_aspect_ratio=False)


def load_image_resource_archive(resource_path: list, width: int, height: int) -> GdkPixbuf:
    resource_path = os.path.join(*resource_path)
    zip_path = os.path.dirname(os.path.dirname(__file__))
    with ZipFile(zip_path, 'r') as archive:
        with archive.open(resource_path) as data:
            loader = GdkPixbuf.PixbufLoader()
            loader.write(data.read())
            pixbuf = loader.get_pixbuf()    # type: GdkPixbuf.Pixbuf
            pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
            loader.close()
            return pixbuf


def load_image_resource(resource_path: list, width: int, height: int) -> GdkPixbuf:
    if os.path.isdir(os.path.dirname(__file__)):
        return load_image_resource_file(resource_path, width, height)
    else:
        return load_image_resource_archive(resource_path, width, height)


def load_config(config_path: str) -> dict:
    with open(config_path) as config_file:
        return json.load(config_file)


def save_config(config: dict, config_path: str):
    path = os.path.dirname(config_path)
    if not os.path.isdir(path):
        os.mkdir(path)
    with open(config_path, 'wb') as file:
        file.write(json.dumps(config, sort_keys=True, indent=4, separators=(',', ': ')).encode('utf-8'))


def show_context_menu(tree: 'Gtk.TreeView', event, popup: 'Gtk.Menu'):
    path = tree.get_path_at_pos(int(event.x), int(event.y))
    # Get the selection
    selection = tree.get_selection()
    # Get the selected path(s)
    rows = selection.get_selected_rows()
    # If not clicked on selection, change selected rows
    if path:
        if path[0] not in rows[1]:
            selection.unselect_all()
            selection.select_path(path[0])
        popup.popup(None, None, None, None, 0, event.time)
