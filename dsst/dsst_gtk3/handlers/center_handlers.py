from dsst_gtk3.gtk_ui import DSSTGtkUi
from dsst_sql import sql
from dsst_gtk3 import dialogs, util

class CenterHandlers:
    def __init__(self, app: DSSTGtkUi):
        self.app = app

    def do_add_death(self, *_):
        pass