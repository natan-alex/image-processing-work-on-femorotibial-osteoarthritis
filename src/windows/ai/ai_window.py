import tkinter as tk
import tkinter.messagebox as tk_boxes

from typing import Union
from entities.model_related.expected_subfolders import ExpectedSubfolders

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

    _datasets: Union[aliases.Datasets, None] = None

    _neural_network: Union[aliases.Model, None] = None
    _xgboost_model: Union[aliases.Model, None] = None
    _shallow_classifier_model: Union[aliases.Model, None] = None

    _neural_network_evaluation_metrics: Union[ModelEvaluationMetrics, None] = None
    _xgboost_evaluation_metrics: Union[ModelEvaluationMetrics, None] = None
    _shallow_classifier_evaluation_metrics: Union[ModelEvaluationMetrics, None] = None

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
        self._time_elapsed_displayer = TimeElapsedDisplayer()
        self._tensorflow_output_displayer = TensorflowOutputDisplayer(self._main_frame)
        self._main_frame.clear_and_show_message("Nada a ser exibido")

    def _handle_events(self):
        events.read_model_main_directory_button_clicked.subscribe(
            self._on_read_model_main_directory_button_clicked)
        events.load_neural_network_button_clicked.subscribe(
            self._on_load_neural_network_button_clicked)
        events.train_neural_network_button_clicked.subscribe(
            self._on_train_neural_network_button_clicked)
        events.train_shallow_classifier_button_clicked.subscribe(
            self._on_train_shallow_classifier_button_clicked)
        events.train_xgboost_classifier_button_clicked.subscribe(
            self._on_train_xgboost_classifier_button_clicked)
        events.evaluate_neural_network_button_clicked.subscribe(
            self._on_evaluate_neural_network_button_clicked)
        events.evaluate_xgboost_button_clicked.subscribe(
            self._on_evaluate_xgboost_button_clicked)
        events.evaluate_shallow_classifier_button_clicked.subscribe(
            self._on_evaluate_shallow_classifier_button_clicked)
        events.plot_confusion_matrix_for_neural_network_button_clicked.subscribe(
            self._on_plot_confusion_matrix_for_nn_button_clicked)
        events.plot_confusion_matrix_for_xgboost_button_clicked.subscribe(
            self._on_plot_confusion_matrix_for_xgboost_button_clicked)
        events.plot_confusion_matrix_for_shallow_classifier_button_clicked.subscribe(
            self._on_plot_confusion_matrix_for_shallow_classifier_button_clicked)

    def _on_read_model_main_directory_button_clicked(self):
        """
        Ask the user to select a directory and validate
        its folder structure looking for train, test and
        validation folders with the model images.
        After all show the file count per class infos
        """

        self._main_frame.clear_and_show_message("Lendo diretório...")

        result = DatasetService.read_datasets()

        if result.error is not None:
            tk_boxes.showerror("Falha ao ler diretório", message=result.error)
            self._main_frame.clear_and_show_message("Nada a ser exibido")
            return

        self._datasets = result.datasets
        self._main_frame.show_datasets_infos(self._datasets)

    def _check_if_should_use_checkpoint(self) -> bool:
        start_from_checkpoint = False

        if ModelService.neural_network_has_fit_checkpoint():
            message = "Um checkpoint de treinamento foi encontrado.\n" + \
            "Deseja resumir o treinamento do modelo a partir dele?"
            start_from_checkpoint = tk_boxes.askquestion(title="Modelo", message=message) == "yes"

        return start_from_checkpoint

    def _save_neural_network_and_show_info(self):
        if ModelService.save_neural_network(self._neural_network):
            tk_boxes.showinfo(message="Treinamento finalizado com sucesso. O modelo foi salvo para uso posterior")
        else:
            tk_boxes.showinfo(message="Treinamento finalizado com sucesso porém não foi possível salvar o modelo")

    def _on_train_neural_network_button_clicked(self):
        """
        Clear screen to show elapsed time and redirect tensorflow output.
        Ask user if start from previous checkpoint (if exists) and for the number
        of epochs to train the model
        """

        if self._datasets is None:
            tk_boxes.showwarning(message="Necessário ler antes um diretório com os arquivos para o treinamento, teste e validação")
            return
        
        start_from_checkpoint = self._check_if_should_use_checkpoint()

        epochs = Popup(self).get_epochs_then_destroy()

        self._main_frame.clear_children()
        self._tensorflow_output_displayer.enable()
        self._time_elapsed_displayer.start()

        self._neural_network = ModelService.create_and_train_neural_network(
            self._datasets, epochs=epochs, start_from_checkpoint=start_from_checkpoint)

        self._time_elapsed_displayer.stop()
        self._tensorflow_output_displayer.disable()

        self._save_neural_network_and_show_info()

    def _on_train_xgboost_classifier_button_clicked(self):
        if self._datasets is None:
            tk_boxes.showwarning(message="Necessário ler antes um diretório com os arquivos para o treinamento e teste")
            return

        self._main_frame.clear_and_show_message("Treinando classificador xgboost...")
        self._time_elapsed_displayer.start()

        self._xgboost_model = ModelService \
            .create_and_train_xgboost(self._datasets[ExpectedSubfolders.TRAIN])

        self._time_elapsed_displayer.stop()
        self._main_frame.clear_children()

        tk_boxes.showinfo(message="Treinamento finalizado com sucesso")

    def _on_train_shallow_classifier_button_clicked(self):
        if self._datasets is None:
            tk_boxes.showwarning(message="Necessário ler antes um diretório com os arquivos para o treinamento e teste")
            return

        self._main_frame.clear_and_show_message("Treinando classificador raso Random Forest...")
        self._time_elapsed_displayer.start()

        self._shallow_classifier_model = ModelService \
            .create_and_train_random_forest_classifier(self._datasets[ExpectedSubfolders.TRAIN])

        self._time_elapsed_displayer.stop()
        self._main_frame.clear_children()

        tk_boxes.showinfo(message="Treinamento finalizado com sucesso")

    def _on_load_neural_network_button_clicked(self):
        """ Load neural network from file system """

        self._neural_network = ModelService.load_saved_neural_network()

        if self._neural_network is None:
            tk_boxes.showwarning(message="Nenhum modelo salvo foi encontrado")
            return

        tk_boxes.showinfo(message="Modelo encontrado e carregado com sucesso")

    def _on_plot_confusion_matrix_for_nn_button_clicked(self):
        """ Plot the confusion matrix """

        if self._neural_network_evaluation_metrics is not None:
            matrix = self._neural_network_evaluation_metrics.confusion_matrix
            ModelService.plot_confusion_matrix(matrix)
        else:
            tk_boxes.showwarning(message="Necessário carregar (ou treinar) e avaliar a rede neural antes")

    def _on_plot_confusion_matrix_for_xgboost_button_clicked(self):
        if self._xgboost_evaluation_metrics is not None:
            matrix = self._xgboost_evaluation_metrics.confusion_matrix
            ModelService.plot_confusion_matrix(matrix)
        else:
            tk_boxes.showwarning(message="Necessário treinar e avaliar o modelo xgboost antes")

    def _on_plot_confusion_matrix_for_shallow_classifier_button_clicked(self):
        if self._shallow_classifier_evaluation_metrics is not None:
            matrix = self._shallow_classifier_evaluation_metrics.confusion_matrix
            ModelService.plot_confusion_matrix(matrix)
        else:
            tk_boxes.showwarning(message="Necessário treinar e avaliar o classificador raso antes")

    def _on_evaluate_neural_network_button_clicked(self):
        """
        Evaluate classifier with test files and
        show metrics and elapsed time
        """

        if self._datasets is None or self._neural_network is None:
            tk_boxes.showwarning(message="Necessário ler antes um diretório com os arquivos para o treinamento e teste ou carregar um modelo")
            return

        self._main_frame.clear_children()
        self._tensorflow_output_displayer.enable()
        self._time_elapsed_displayer.start()

        self._neural_network_evaluation_metrics = ModelService \
            .evaluate_model_and_get_metrics(self._neural_network, self._datasets)

        self._time_elapsed_displayer.stop()
        self._tensorflow_output_displayer.disable()
        self._main_frame.show_model_evaluation_result(self._neural_network_evaluation_metrics)

    def _on_evaluate_xgboost_button_clicked(self):
        if self._datasets is None or self._xgboost_model is None:
            tk_boxes.showwarning(message="Necessário ler antes um diretório com os arquivos para o treinamento e teste e treinar o classificador xgboost")
            return

        self._main_frame.clear_and_show_message("Avaliando classificador xgboost...")
        self._time_elapsed_displayer.start()

        self._neural_network_evaluation_metrics = ModelService \
            .evaluate_model_and_get_metrics(self._xgboost_model, self._datasets)

        self._time_elapsed_displayer.stop()
        self._main_frame.show_model_evaluation_result(self._neural_network_evaluation_metrics)

    def _on_evaluate_shallow_classifier_button_clicked(self):
        if self._datasets is None or self._shallow_classifier_model is None:
            tk_boxes.showwarning(message="Necessário ler antes um diretório com os arquivos para o treinamento e teste")
            return

        self._main_frame.clear_and_show_message("Avaliando classificador raso Random Forest...")
        self._time_elapsed_displayer.start()

        self._shallow_classifier_evaluation_metrics = ModelService \
            .evaluate_model_and_get_metrics(self._shallow_classifier_model, self._datasets)

        self._time_elapsed_displayer.stop()
        self._main_frame.show_model_evaluation_result(self._shallow_classifier_evaluation_metrics)
