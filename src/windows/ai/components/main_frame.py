import tkinter as tk

from globals import aliases

from entities.model_related.expected_subfolders import ExpectedSubfolders


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

    def _clear_inner_frame(self):
        for child in self._centered_inner_frame.winfo_children():
            child.destroy()

    def _display_classes_and_files_infos(
        self,
        infos: aliases.ClassesAndFiles
    ):
        """ Display the file count for each model class """

        for c, files in infos.items():
            tk.Label(
                self._centered_inner_frame,
                font=("", 9), justify=tk.LEFT,
                text=f"Para a classe {c.value}: {len(files)} imagens"
            ).pack()

    def _display_dataset_infos(
        self,
        dataset: aliases.Dataset
    ):
        """ Display the file count for each model class """

        # for c, files in dataset:
        #     tk.Label(
        #         self._centered_inner_frame,
        #         font=("", 9), justify=tk.LEFT,
        #         text=f"Para a classe {c.value}: {len(files)} imagens"
        #     ).pack()

    def display_model_folders_and_files_infos(
        self,
        infos: aliases.Datasets
    ):
        """
        Creates widgets on screen to display the files infos
        """

        self._clear_inner_frame()

        tk.Label(
            self._centered_inner_frame,
            text="Sobre o diretório escolhido:").pack()

        for subfolder, title in subfolders_and_titles.items():
            tk.Label(self._centered_inner_frame, text=title).pack()
            self._display_dataset_infos(infos[subfolder])

    def display_no_folder_and_files_message(self):
        self._clear_inner_frame()

        tk.Label(
            self._centered_inner_frame,
            text="Nenhum diretório escolhido").pack()
