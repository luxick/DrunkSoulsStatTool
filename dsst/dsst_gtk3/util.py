class Util:
    @staticmethod
    def get_combo_value(combo, index: int):
        """ Retrieve the selected value of a combo box at the selected index in the model """
        tree_iter = combo.get_active_iter()
        if tree_iter:
            return combo.get_model().get_value(tree_iter, index)
        else:
            return -1
