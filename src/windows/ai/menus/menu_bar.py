import tkinter as tk

from windows.ai.menus.files_menu import FilesMenu
from windows.ai.menus.model_menu import ModelMenu


class MenuBar(tk.Menu):
    """ 
    The menu bar for the ai window. 
    Agregate submenus in a single bar
    """

    def __init__(self, parent: tk.Toplevel):
        super().__init__(parent)

        self._files_menu = FilesMenu(self)
        self._model_menu = ModelMenu(self)

        self._add_menu_items()

    def _add_menu_items(self):
        self.add_cascade(label="Arquivos", menu=self._files_menu)
        self.add_cascade(label="Modelo", menu=self._model_menu)
