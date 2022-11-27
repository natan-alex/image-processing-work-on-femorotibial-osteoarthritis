import tkinter as tk

from windows.images.menus.selection_menu import SelectionMenu
from windows.images.menus.actions_menu import ActionsMenu


class MenuBar(tk.Menu):
    def __init__(self, parent: tk.Toplevel):
        super().__init__(parent)

        self._selection_menu = SelectionMenu(self)
        self._actions_menu = ActionsMenu(self)

        self._add_submenus()

    def _add_submenus(self):
        self.add_cascade(
            label="Ações",
            menu=self._actions_menu)

        self.add_cascade(
            label="Seleção",
            menu=self._selection_menu)
