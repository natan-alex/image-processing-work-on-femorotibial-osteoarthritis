import tkinter as tk

from globals import aliases

from typing import Union

from entities.model_related.expected_subfolders import ExpectedSubfolders

from services.dataset_service import DatasetService

from services.output_service import (
    OutputService, BeforeWriteCallbackParams, AfterWriteCallbackParams
)

from helpers.tensorflow_output_helper import TensorflowOutputHelper


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

        self._output_service = OutputService()

        self._centered_frame = tk.Frame(self)
        self._centered_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._last_inserted_label: Union[tk.Label, None] = None
        self._stdout_redirected = False


    def _clear_centered_frame(self):
        """ Clear the centered inner frame removing its children """

        for child in self._centered_frame.winfo_children():
            child.destroy()


    def _create_label_with_dataset_infos(self, dataset: aliases.Dataset):
        """ Display the file count for each model class """

        file_count_per_class = DatasetService.get_file_count_per_class_for(dataset)

        for clasz, file_count in file_count_per_class.items():
            tk.Label(
                self._centered_frame, font=("", 9),
                text=f"Para a classe {clasz.value}: {file_count} imagens"
            ).pack()

    def show_datasets_infos(self, datasets: aliases.Datasets):
        """ Creates widgets on centered frame to display the datasets infos """

        old_frame = self._centered_frame
        self._centered_frame = tk.Frame(self)

        tk.Label(self._centered_frame, text="Sobre o diretório escolhido:").pack()

        for subfolder, title in subfolders_and_titles.items():
            tk.Label(self._centered_frame, text=title).pack()

            self._create_label_with_dataset_infos(datasets[subfolder])

        old_frame.destroy()
        self._centered_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


    def clear_and_show_message(self, message: str):
        self._clear_centered_frame()

        tk.Label(self._centered_frame, text=message).pack()


    def _before_write_to_stdout_callback(self, params: BeforeWriteCallbackParams) -> str:
        """ 
        Executed before something is writen to the redirected stdout.
        Manipulate the tensorflow output to show it on screen
        """

        if (
            not TensorflowOutputHelper.is_epoch_indicator(params.content_to_write) and
            not TensorflowOutputHelper.is_training_output(params.content_to_write)
        ):
            return ""

        if (
            self._last_inserted_label is not None and
            not TensorflowOutputHelper.is_epoch_indicator(self._last_inserted_label["text"])
        ):
            self._last_inserted_label.destroy()

        return TensorflowOutputHelper.manipulate_to_show(params.content_to_write)

    def _after_write_to_stdout_callback(self, params: AfterWriteCallbackParams):
        """ 
        Executed after something is writen to the redirected stdout.
        Just store the inserted widget to remove it if necessary in next insertion
        """

        self._last_inserted_label = params.inserted_widget

    def start_showing_stdout(self):
        """ Redirect stdout to the centered frame to show tensorflow output """

        if self._stdout_redirected:
            return

        self._output_service.redirect_stdout_to(
            self._centered_frame,
            before_write_callback=self._before_write_to_stdout_callback,
            after_write_callback=self._after_write_to_stdout_callback)

        self._stdout_redirected = True

    def stop_showing_stdout(self):
        """ Stop showing the stdout in centered frame """

        if self._stdout_redirected:
            self._output_service.undo_stdout_redirection()
            self._stdout_redirected = False
