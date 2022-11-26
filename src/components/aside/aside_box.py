import tkinter as tk

import aliases
from definitions.models.classes import ModelClasses
from definitions.models.expected_subfolders import (
    ExpectedSubfoldersInChosenFolder as Folders
)


class AsideBox(tk.Frame):
    def __init__(self, parent: tk.Frame):
        super().__init__(parent)

        self._parent = parent

    def display_folders_classes_and_files_infos(
        self,
        folders_classes_and_files: aliases.FoldersClassesAndFiles
    ):
        tk.Label(self._parent, text="Sobre o diretório escolhido:").pack()

        tk.Label(self._parent, text="Para o treinamento:").pack()
        train = folders_classes_and_files[Folders.TRAIN]
        self._display_file_count_for_each_model_class(train)

        tk.Label(self._parent, text="Para o teste:").pack()
        test = folders_classes_and_files[Folders.TEST]
        self._display_file_count_for_each_model_class(test)

        tk.Label(self._parent, text="Para a validação:").pack()
        validation = folders_classes_and_files[Folders.VALIDATION]
        self._display_file_count_for_each_model_class(validation)

    def _display_file_count_for_each_model_class(
        self,
        classes_and_files: aliases.ClassesAndFiles
    ):
        label_text = ""

        for clasz in list(ModelClasses):
            file_count = len(classes_and_files[clasz.value])
            label_text += f"Para a classe {clasz.value}: {file_count} imagens\n"

        tk.Label(
            self._parent,
            font=("", 9),
            text=label_text,
            justify=tk.LEFT
        ).pack()

    def clear(self):
        children = self.winfo_children()

        for widget in children:
            widget.destroy()
