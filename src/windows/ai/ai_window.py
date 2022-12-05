import tkinter as tk
import tkinter.messagebox as tk_boxes

from typing import Union

from globals import events, aliases, configs

from windows.ai.menus.menu_bar import MenuBar
from windows.ai.components.popup import Popup
from windows.ai.components.main_frame import MainFrame
from windows.ai.components.time_elapsed_displayer import TimeElapsedDisplayer
from windows.ai.components.tensorflow_output_displayer import TensorflowOutputDisplayer

from services.model_service import ModelService
from services.dataset_service import DatasetService

from entities.model_related.model_evaluation_metrics import ModelEvaluationMetrics


class AiWindow(tk.Toplevel):
    """
    Class that represents the window with ai
    related things and operations
    """

    _model_datasets: Union[aliases.Datasets, None] = None
    _model: Union[aliases.Model, None] = None
    _evaluation_result: Union[ModelEvaluationMetrics, None] = None

    def __init__(self):
        super().__init__()

        self.title("IA")
        self.geometry(f"{configs.AI_WINDOW_WIDTH}x{configs.AI_WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.update()

        self._init_components()
        self._handle_events()

    def _init_components(self):
        self.config(menu=MenuBar(self))
        self._main_frame = MainFrame(self)
        self._time_elapsed_label = TimeElapsedDisplayer(self._main_frame)
        self._tensorflow_output_displayer = TensorflowOutputDisplayer(self._main_frame)
        self._main_frame.clear_and_show_message("Nada a ser exibido")

    def _handle_events(self):
        events.read_model_main_directory_button_clicked.subscribe(
            self._on_read_model_main_directory_button_clicked)
        events.load_saved_model_button_clicked.subscribe(
            self._on_load_saved_model_button_clicked)
        events.train_neural_network_button_clicked.subscribe(
            self._on_train_neural_network_button_clicked)
        events.train_normal_classifier_button_clicked.subscribe(
            self._on_train_normal_classifier_button_clicked)
        events.evaluate_neural_network_button_clicked.subscribe(
            self._on_evaluate_neural_network_button_clicked)
        events.plot_confusion_matrix_button_clicked.subscribe(
            self._on_plot_confusion_matrix_button_clicked)

    def _on_read_model_main_directory_button_clicked(self):
        """
        Ask the user to select a directory and validate
        its folder structure looking for train, test and
        validation folders with the model images
        """

        self._main_frame.clear_and_show_message("Lendo diretório...")

        result = DatasetService.read_datasets()

        if result.error is not None:
            tk_boxes.showerror("Falha ao ler diretório", message=result.error)
            self._main_frame.clear_and_show_message("Nada a ser exibido")
            return

        self._model_datasets = result.datasets
        self._main_frame.show_datasets_infos(self._model_datasets)

    def _check_if_should_use_checkpoint(self) -> bool:
        start_from_checkpoint = False

        if ModelService.has_fit_checkpoint():
            message = "Um checkpoint de treinamento foi encontrado.\n" + \
            "Deseja resumir o treinamento do modelo a partir dele?"
            start_from_checkpoint = tk_boxes.askquestion(title="Modelo", message=message) == "yes"

        return start_from_checkpoint

    def _save_model_and_show_info(self):
        if ModelService.save_model(self._model):
            tk_boxes.showinfo(message="Treinamento finalizado com sucesso. O modelo foi salvo para uso posterior")
        else:
            tk_boxes.showinfo(message="Treinamento finalizado com sucesso porém não foi possível salvar o modelo")

    def _on_train_neural_network_button_clicked(self):
        if self._model_datasets is None:
            tk_boxes.showwarning(message="Necessário ler antes um diretório com os arquivos para o treinamento, teste e validação")
            return
        
        start_from_checkpoint = self._check_if_should_use_checkpoint()

        epochs = Popup(self).get_epochs_then_destroy()

        self._main_frame.clear_children()
        self._tensorflow_output_displayer.enable()
        self._time_elapsed_label.enable()

        self._model = ModelService.create_and_train_model(
            self._model_datasets, epochs=epochs, start_from_checkpoint=start_from_checkpoint)

        self._time_elapsed_label.disable()
        self._tensorflow_output_displayer.disable()

        self._save_model_and_show_info()

    def _on_evaluate_neural_network_button_clicked(self):
        if self._model_datasets is None or self._model is None:
            tk_boxes.showwarning(message="Necessário ler antes um diretório com os arquivos para o treinamento e teste ou carregar um modelo")
            return

        self._main_frame.clear_children()
        self._tensorflow_output_displayer.enable()
        self._time_elapsed_label.enable()

        self._evaluation_result = ModelService \
            .evaluate_model_and_get_metrics(self._model, self._model_datasets)

        self._time_elapsed_label.disable()
        self._tensorflow_output_displayer.disable()
        self._main_frame.show_model_evaluation_result(self._evaluation_result)

    def _on_train_normal_classifier_button_clicked(self):
        if self._model_datasets is None:
            tk_boxes.showwarning(message="Necessário ler antes um diretório com os arquivos para o treinamento e teste")
            return

    def _on_load_saved_model_button_clicked(self):
        self._model = ModelService.load_saved_model()

        if self._model is None:
            tk_boxes.showwarning(message="Nenhum modelo salvo foi encontrado")
            return

        tk_boxes.showinfo(message="Modelo encontrado e carregado com sucesso")

    def _on_plot_confusion_matrix_button_clicked(self):
        if self._evaluation_result is not None:
            matrix = self._evaluation_result.confusion_matrix
            ModelService.plot_confusion_matrix(matrix)
        else:
            tk_boxes.showwarning(message="Necessário carregar (ou treinar) e avaliar um modelo antes")
