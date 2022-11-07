import tkinter as tk

from components.menus.file_menu import FileMenu
from components.menus.interactions_menu import InteractionsMenu


class MenuBar(tk.Menu):
    """
    Class that is the menu bar with the tabs of the
    main screen
    """

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)

        self._file_menu = FileMenu(self)
        self._interactions_menu = InteractionsMenu(self)

        self._add_submenus()

    def _add_submenus(self):
        self.add_cascade(label="Imagens", menu=self._file_menu)
        self.add_cascade(label="Interações", menu=self._interactions_menu)

    @property
    def file_menu(self) -> FileMenu:
        return self._file_menu

    @property
    def interactions_menu(self) -> InteractionsMenu:
        return self._interactions_menu