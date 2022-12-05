import tkinter as tk

from globals import configs
from windows.images.images_window import ImagesWindow
from windows.ai.ai_window import AiWindow


class MainWindow(tk.Tk):
    """ Class that represents the main app window """

    def __init__(self):
        super().__init__()
        self.title("Trabalho de Processamento e Análise de Imagens")
        self.configure(width=configs.MAIN_WINDOW_WIDTH)
        self.configure(height=configs.MAIN_WINDOW_HEIGHT)
        self.resizable(False, False)
        self.update()

        self._add_components()

    def _add_components(self):
        self._add_images_button()
        self._add_ai_button()

    def _add_images_button(self):
        """ Add the button to open the images window """

        images_button = tk.Button(self, text="Imagens")
        images_button.configure(borderwidth=1)
        images_button.configure(font=("", 13))
        images_button.configure(command=self._create_images_window)
        images_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    def _add_ai_button(self):
        """ Add the button to open the ai window """

        images_button = tk.Button(self, text="IA")
        images_button.configure(borderwidth=1)
        images_button.configure(font=("", 13))
        images_button.configure(command=self._create_ai_related_window)
        images_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

    def _create_images_window(self):
        self._images_window = ImagesWindow()

    def _create_ai_related_window(self):
        self._ai_window = AiWindow()
