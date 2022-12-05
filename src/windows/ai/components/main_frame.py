import tkinter as tk

import seaborn as sn

import matplotlib.pyplot as plt

from globals import aliases

from entities.model_related.expected_subfolders import ExpectedSubfolders
from entities.model_related.model_evaluation_metrics import ModelEvaluationMetrics

from services.dataset_service import DatasetService


subfolders_and_titles = {
    ExpectedSubfolders.TRAIN: "Para o treinamento:",
    ExpectedSubfolders.TEST: "Para o teste:",
    ExpectedSubfolders.VALIDATION: "Para a validação:"
}


class MainFrame(tk.Frame):
    def __init__(self, parent: tk.Toplevel):
        super().__init__(parent)

        self.configure(width=parent.winfo_width())
        self.configure(height=parent.winfo_height())

        self.pack(fill=tk.BOTH)

        self.update()

    def clear_children(self):
        for child in self.winfo_children():
            child.destroy()

    def clear_and_show_message(self, message: str):
        self.clear_children()

        label = tk.Label(self, text=message)
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def _show_file_count_per_class_for(self, dataset: aliases.Dataset):
        """ Display the file count for each model class """

        file_count_per_class = DatasetService.get_file_count_per_class_for(dataset)

        for clasz, file_count in file_count_per_class.items():
            label_text = f"Para a classe {clasz.value}: {file_count} imagens"
            tk.Label(self._datasets_infos_frame, font=("", 9), text=label_text).pack()

    def show_datasets_infos(self, datasets: aliases.Datasets):
        """ Creates widgets on centered frame to display the datasets infos """

        self.clear_children()

        self._datasets_infos_frame = tk.Frame(self)

        tk.Label(self._datasets_infos_frame, text="Sobre o diretório escolhido:").pack()

        for subfolder, title in subfolders_and_titles.items():
            tk.Label(self._datasets_infos_frame, text=title).pack()

            self._show_file_count_per_class_for(datasets[subfolder])

        self._datasets_infos_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def show_model_evaluation_result(self, result: ModelEvaluationMetrics):
        self.clear_children()

        temporary_frame = tk.Frame(self)

        tk.Label(temporary_frame, text="Informações do modelo após availação com arquivos de teste:").pack(pady=2)
        tk.Label(temporary_frame, text=f"Acurácia: {result.accuracy_score}").pack(pady=2)
        tk.Label(temporary_frame, text=f"Precisão: {result.precision_score}").pack(pady=2)
        tk.Label(temporary_frame, text=f"Especificidade: {result.specificity_score}").pack(pady=2)
        tk.Label(temporary_frame, text=f"Sensibilidade: {result.sensitivity_score}").pack(pady=2)
        tk.Label(temporary_frame, text=f"F1 Score: {result.f1_score}").pack(pady=2)

        temporary_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
