"""
This modules contains general utilities for the GTK application to use.
"""
import json
import os
from zipfile import ZipFile

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'dsst', 'config.json')
DEFAULT_CONFIG = {
    'auto_connect': False,
    'sql_connections': [{
        'host': 'localhost',
        'port': 3306,
        'db_name': 'dsst',
        'user': 'dsst',
        'password': 'dsst'}
    ]
}


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
    with open(full_path, 'r') as file:
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


def load_config(config_path: str) -> dict:
    with open(config_path) as config_file:
        return json.load(config_file)


def save_config(config: dict, config_path: str):
    path = os.path.dirname(config_path)
    if not os.path.isdir(path):
        os.mkdir(path)
    with open(config_path, 'wb') as file:
        file.write(json.dumps(config, sort_keys=True, indent=4, separators=(',', ': ')).encode('utf-8'))
