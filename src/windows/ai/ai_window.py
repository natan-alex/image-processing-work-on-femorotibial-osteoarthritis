import tkinter as tk
import tkinter.messagebox as tk_boxes
from typing import Union

from globals import events, aliases, configs
from windows.ai.components.operations_frame import OperationsFrame

from windows.ai.menus.menu_bar import MenuBar
from windows.ai.components.files_infos_frame import FilesInfosFrame

from services.folders_and_files_service import FoldersAndFilesService


class AiWindow(tk.Toplevel):
    """
    Class that represents the window with ai
    related things and operations
    """

    _folders_classes_and_files: Union[aliases.FoldersClassesAndFiles, None] = None

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
        self._files_infos_frame = FilesInfosFrame(self)
        self._operations_frame = OperationsFrame(self)

        self._files_infos_frame.pack(
            fill=tk.Y, side=tk.LEFT, anchor=tk.CENTER)
        self._operations_frame.pack(
            fill=tk.Y, side=tk.RIGHT, anchor=tk.CENTER)

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

        result = FoldersAndFilesService.read_model_related_folders_and_files()

        if result.error is not None:
            tk_boxes.showerror("Falha ao treinar modelo", message=result.error)
            return

        self._folders_classes_and_files = result.folder_classes_and_files

        self._files_infos_frame.display_folders_classes_and_files_infos(self._folders_classes_and_files)
        self._operations_frame.display_things()

    def _on_train_neural_network_button_clicked(self):
        self._operations_frame.hide_things()

    def _on_train_normal_classifier_button_clicked(self):
        self._operations_frame.hide_things()
