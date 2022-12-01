import tkinter as tk
import tkinter.messagebox as tk_boxes
from typing import Union

from globals import events, aliases, configs

from windows.ai.menus.menu_bar import MenuBar
from windows.ai.components.main_frame import MainFrame

from services.model_service import ModelService
from services.dataset_service import DatasetService


class AiWindow(tk.Toplevel):
    """
    Class that represents the window with ai
    related things and operations
    """

    _model_datasets: Union[aliases.Datasets, None] = None

    def __init__(self):
        super().__init__()

        self.title("IA")
        self.configure(width=configs.AI_WINDOW_WIDTH)
        self.configure(height=configs.AI_WINDOW_HEIGHT)
        self.resizable(False, False)
        self.update()

        self._init_components()
        self._handle_events()

    def _init_components(self):
        self.config(menu=MenuBar(self))
        self._main_frame = MainFrame(self)
        self._main_frame.display_no_folder_and_files_message()

    def _handle_events(self):
        events.read_model_main_directory_button_clicked.subscribe(
            self._on_read_model_main_directory_button_clicked)
        events.train_neural_network_button_clicked.subscribe(
            self._on_train_neural_network_button_clicked)
        events.train_normal_classifier_button_clicked.subscribe(
            self._on_train_normal_classifier_button_clicked)

    def _on_read_model_main_directory_button_clicked(self):
        """
        Ask the user to select a directory and validate
        its folder structure looking for train, test and
        validation folders with the model images
        """

        self._main_frame.display_loading_message()

        result = DatasetService.read_datasets()

        if result.error is not None:
            tk_boxes.showerror("Falha ao ler diretório", message=result.error)
            self._main_frame.display_no_folder_and_files_message()
            return

        self._model_datasets = result.datasets

        self._main_frame.display_datasets_infos(self._model_datasets)

    def _on_train_neural_network_button_clicked(self):
        if self._model_datasets is None:
            tk_boxes.showwarning(message="Necessário ler antes um diretório com os arquivos para o treinamento")
            return

        self._model = ModelService.build_model(self._model_datasets)

    def _on_train_normal_classifier_button_clicked(self):
        if self._model_datasets is None:
            tk_boxes.showwarning(message="Necessário ler antes um diretório com os arquivos para o treinamento")
            return
