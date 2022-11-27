import tkinter as tk

from globals import aliases

from entities.model_related.model_classes import ModelClasses
from entities.model_related.expected_subfolders import ExpectedSubfolders


subfolders_and_titles = {
    ExpectedSubfolders.TRAIN: "Para o treinamento:",
    ExpectedSubfolders.TEST: "Para o teste:",
    ExpectedSubfolders.VALIDATION: "Para a validação:"
}


class FilesInfosBox(tk.Frame):
    def __init__(self, parent: tk.Toplevel):
        super().__init__(parent)

        self._parent = parent

        self.configure(width=parent.winfo_width() * 0.3)
        self.configure(height=parent.winfo_height())
        self.update()

    def display_folders_classes_and_files_infos(
        self,
        folders_classes_and_files: aliases.FoldersClassesAndFiles
    ):
        tk.Label(self._parent, text="Sobre o diretório escolhido:").pack(pady=5)

        for subfolder, title in subfolders_and_titles.items():
            tk.Label(self._parent, text=title).pack()
            classes_and_files = folders_classes_and_files[subfolder]
            self._display_file_count_for_each_model_class(classes_and_files)

    def _display_file_count_for_each_model_class(
        self,
        classes_and_files: aliases.ClassesAndFiles
    ):
        text = ""

        for clasz in list(ModelClasses):
            file_count = len(classes_and_files[clasz.value])
            text += f"Para a classe {clasz.value}: {file_count} imagens\n"

        tk.Label(self._parent, font=("", 9), text=text, justify=tk.LEFT).pack()

    def clear(self):
        children = self.winfo_children()

        for widget in children:
            widget.destroy()
