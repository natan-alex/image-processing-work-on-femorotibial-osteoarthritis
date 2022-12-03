import tkinter as tk

from typing import Union

from globals import aliases

from entities.model_related.model_classes import ModelClasses
from entities.model_related.expected_subfolders import ExpectedSubfolders

from services.dataset_service import DatasetService


subfolders_and_titles = {
    ExpectedSubfolders.TRAIN: "Para o treinamento:",
    ExpectedSubfolders.TEST: "Para o teste:",
    ExpectedSubfolders.VALIDATION: "Para a validação:"
}


class MainFrame(tk.Frame):
    """
    Class for displaying the selected directory 
    infos with the amount of files for each folder
    and model class
    """

    def __init__(self, parent: tk.Toplevel):
        super().__init__(parent)

        self.configure(width=parent.winfo_width())
        self.configure(height=parent.winfo_height())

        self.pack(fill=tk.BOTH)

        self.update()

        self._centered_inner_frame = tk.Frame(self)
        self._centered_inner_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def _clear_centered_frame(self):
        for child in self._centered_inner_frame.winfo_children():
            child.destroy()

    def _create_label_with_dataset_infos(self, dataset: aliases.Dataset):
        """ Display the file count for each model class """

        file_count_per_class = DatasetService.get_file_count_per_class_in(dataset)

        for clasz, file_count in file_count_per_class.items():
            tk.Label(
                self._centered_inner_frame, font=("", 9),
                text=f"Para a classe {clasz.value}: {file_count} imagens"
            ).pack()

    def display_datasets_infos(self, infos: aliases.Datasets):
        """ Creates widgets on screen to display the files infos """

        old_frame = self._centered_inner_frame
        self._centered_inner_frame = tk.Frame(self)

        tk.Label(self._centered_inner_frame, text="Sobre o diretório escolhido:").pack()

        for subfolder, title in subfolders_and_titles.items():
            tk.Label(self._centered_inner_frame, text=title).pack()

            self._create_label_with_dataset_infos(infos[subfolder])

        old_frame.destroy()
        self._centered_inner_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def _clear_centered_frame_and_display_message(self, message: str):
        self._clear_centered_frame()

        tk.Label(self._centered_inner_frame, text=message).pack()

    def display_no_folder_and_files_message(self):
        self._clear_centered_frame_and_display_message("Nenhum diretório escolhido")

    def display_loading_message(self):
        self._clear_centered_frame_and_display_message("Lendo arquivos...")