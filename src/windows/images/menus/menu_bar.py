import tkinter as tk

from windows.images.menus.selection_menu import SelectionMenu
from windows.images.menus.image_menu import ImageMenu
from windows.images.menus.data_increase_menu import DataIncreaseMenu
from windows.images.menus.correlations_menu import CorrelationsMenu


class MenuBar(tk.Menu):
    def __init__(self, parent: tk.Toplevel):
        super().__init__(parent)

        self._selection_menu = SelectionMenu(self)
        self._image_menu = ImageMenu(self)
        self._data_increase_menu = DataIncreaseMenu(self)
        self._correlations_menu = CorrelationsMenu(self)

        self._add_submenus()

    def _add_submenus(self):
        self.add_cascade(
            label="Exibição",
            menu=self._image_menu)

        self.add_cascade(
            label="Seleção",
            menu=self._selection_menu)

        self.add_cascade(
            label="Aumento de dados",
            menu=self._data_increase_menu)

        self.add_cascade(
            label="Correlação",
            menu=self._correlations_menu)
