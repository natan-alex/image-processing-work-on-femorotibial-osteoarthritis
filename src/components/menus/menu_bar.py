import tkinter as tk

from components.menus.image_menu import ImageMenu
from components.menus.selection_menu import SelectionMenu
from components.menus.data_increase_menu import DataIncreaseMenu
from components.menus.ia_related_menu import IaRelatedMenu


class MenuBar(tk.Menu):
    """
    Class that is the menu bar with the tabs of the
    main screen
    """

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)

        self._image_menu = ImageMenu(self)
        self._selection_menu = SelectionMenu(self)
        self._data_increase_menu = DataIncreaseMenu(self)
        self._ia_related_menu = IaRelatedMenu(self)

        self._add_submenus()

    def _add_submenus(self):
        self.add_cascade(label="Imagem", menu=self._image_menu)
        self.add_cascade(label="Seleção", menu=self._selection_menu)
        # self.add_cascade(
        #     label="Aumento de dados",
        #     menu=self._data_increase_menu)
        self.add_cascade(label="IA", menu=self._ia_related_menu)
