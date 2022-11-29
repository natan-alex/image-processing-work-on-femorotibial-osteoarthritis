import tkinter as tk

from globals import aliases

from entities.model_related.model_classes import ModelClasses
from entities.model_related.expected_subfolders import ExpectedSubfolders


subfolders_and_titles = {
    ExpectedSubfolders.TRAIN: "Para o treinamento:",
    ExpectedSubfolders.TEST: "Para o teste:",
    ExpectedSubfolders.VALIDATION: "Para a validação:"
}


class FilesInfosFrame(tk.Frame):
    """
    Class for displaying the selected directory 
    infos with the amount of files for each folder
    and model class
    """

    def __init__(self, parent: tk.Toplevel):
        super().__init__(parent)

        self.configure(width=parent.winfo_width() * 0.4)
        self.configure(height=parent.winfo_height())
        self.update()

        self._inner_frame = tk.Frame(self)
        self._inner_frame.place(relx=0.55, rely=0.5, anchor=tk.CENTER)

    def display_folders_classes_and_files_infos(
        self,
        folders_classes_and_files: aliases.FoldersClassesAndFiles
    ):
        """
        Creates widgets on screen to display the files infos
        """

        tk.Label(self._inner_frame, text="Sobre o diretório escolhido:").pack()

        for subfolder, title in subfolders_and_titles.items():
            tk.Label(self._inner_frame, text=title).pack()
            classes_and_files = folders_classes_and_files[subfolder]
            self._display_file_count_for_each_model_class(classes_and_files)

    def _display_file_count_for_each_model_class(
        self,
        classes_and_files: aliases.ClassesAndFiles
    ):
        """ Display the file count for each model class """

        text = ""

        for clasz in list(ModelClasses):
            file_count = len(classes_and_files[clasz.value])
            text += f"Para a classe {clasz.value}: {file_count} imagens\n"

        tk.Label(self._inner_frame, font=("", 9), text=text, justify=tk.LEFT).pack()
