from typing import Tuple
from PIL.Image import Image

from components.main_window import MainWindow
from components.main_canvas import MainCanvas
from components.menus.menu_bar import MenuBar


class App:
    """
    The class that represents the hole application
    """

    # mutable shared state
    selected_image: Tuple[Image, None]
    cropped_image: Tuple[Image, None]
    cross_correlation_points: Tuple[Tuple[int, int], Tuple[int, int], None]

    def __init__(self):
        self._main_window = MainWindow()
        self._main_canvas = MainCanvas(self._main_window)
        self._menu_bar = MenuBar(self._main_window)

        self._setup()

    def _setup(self):
        self._main_window.config(menu=self._menu_bar)

    @property
    def window(self):
        return self._main_window

    @property
    def canvas(self):
        return self._main_canvas

    @property
    def menubar(self):
        return self._menu_bar

    def run(self):
        self._main_window.mainloop()
