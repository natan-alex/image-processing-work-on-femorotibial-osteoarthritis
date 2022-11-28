import tkinter as tk
import tkinter.messagebox as tk_boxes
from typing import Union

from globals import events, aliases, configs

from windows.ai.menus.menu_bar import MenuBar
from windows.ai.components.files_infos_box import FilesInfosBox

from services.training_model_service import TrainingModelService


class AiWindow(tk.Toplevel):
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
        self._files_infos_box = FilesInfosBox(self)
        self._files_infos_box.pack(fill=tk.Y, side=tk.RIGHT)

    def _handle_events(self):
        events.read_model_main_directory_button_clicked.subscribe(
            self._on_read_model_main_directory_button_clicked)

    def _on_read_model_main_directory_button_clicked(self):
        result = TrainingModelService.read_model_related_folders_and_files()

        if result.error is not None:
            tk_boxes.showerror("Falha ao treinar modelo", message=result.error)
            return

        self._folders_classes_and_files = result.folder_classes_and_files

        self._files_infos_box.display_folders_classes_and_files_infos(self._folders_classes_and_files)
