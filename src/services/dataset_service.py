import os
import numpy as np
import tensorflow as tf
import tkinter.filedialog as tk_files

from dataclasses import dataclass
from typing import Union

from globals import aliases, configs
from entities.model_related.model_classes import ModelClasses
from entities.model_related.expected_subfolders import ExpectedSubfolders
from entities.model_related.read_datasets_result import ReadDatasetsResult


@dataclass
class MainFolderValidationResult:
    is_valid: bool
    error: Union[str, None] = None


class DatasetService:
    @staticmethod
    def _validate_model_main_folder(folder_path: str) -> MainFolderValidationResult:
        """
        Check if the selected directory contains the 
        necessary and expected model files
        """

        if not os.path.isdir(folder_path):
            return MainFolderValidationResult(
                is_valid=False,
                error=f"O caminho  {folder_path}  não leva a uma pasta válida") 

        folder_content = os.listdir(folder_path)

        for subfolder in ExpectedSubfolders:
            if subfolder.value not in folder_content:
                return MainFolderValidationResult(
                    is_valid=False,
                    error=f"A subpasta  {subfolder.value}  não foi encontrada na pasta selecionada") 

            subfolder_path = os.path.join(folder_path, subfolder.value)
            subfolder_content = os.listdir(subfolder_path)

            for clasz in ModelClasses:
                if clasz.value not in subfolder_content:
                    return MainFolderValidationResult(
                        is_valid=False,
                        error=f"A subpasta para a classe  {clasz.value}  não foi encontrada na subpasta  {subfolder.value}")

        return MainFolderValidationResult(is_valid=True)

    @staticmethod
    def _read_dataset_from(path: str) -> aliases.Dataset:
        return tf.keras.utils.image_dataset_from_directory(
            path,
            labels="inferred",
            label_mode="categorical",
            color_mode="rgb",
            image_size=configs.MODEL_IMAGES_SIZE,
            class_names=[c.value for c in ModelClasses]
        )

    @staticmethod
    def _read_datasets_from(path: str) -> aliases.Datasets:
        datasets: aliases.Datasets = {}

        for subfolder in ExpectedSubfolders:
            subfolder_path = os.path.join(path, subfolder.value)
            datasets[subfolder] = DatasetService._read_dataset_from(subfolder_path)

        return datasets

    @staticmethod
    def read_datasets() -> ReadDatasetsResult:
        """
        Ask user for the directory that contains the
        directories with the files for model training,
        testing and validation. Check if the folder
        structure is valid also
        """

        try:
            folder_path = tk_files.askdirectory(
                initialdir="~",
                title="Escolha a pasta que contém os arquivos de treino",
            )

            validation_result = DatasetService._validate_model_main_folder(folder_path)

            if not validation_result.is_valid:
                return ReadDatasetsResult(error=validation_result.error)

            datasets = DatasetService._read_datasets_from(folder_path)

            return ReadDatasetsResult(datasets=datasets)
        except Exception as e:
            print(f"Exception on MultipleFilesService.read_model_folders_and_files: {e}")
            return ReadDatasetsResult(error="Um erro inesperado aconteceu")

    @staticmethod
    def get_file_count_per_class_in(
        dataset: aliases.Dataset
    ) -> aliases.ClassFileCount:
        file_count: aliases.ClassFileCount = {c:0 for c in ModelClasses}

        for _, labels_batch in dataset:
            for labels in labels_batch:
                index = np.where(labels == 1)[0][0]
                clasz = dataset.class_names[index]
                file_count[clasz] += 1

        return file_count
