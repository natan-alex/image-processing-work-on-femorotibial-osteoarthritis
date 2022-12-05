import os
import tkinter.filedialog as tk_files
from dataclasses import dataclass
from typing import Union

from globals import aliases, configs
from entities.model_related.model_classes import ModelClasses
from entities.model_related.expected_subfolders import ExpectedSubfolders
from entities.model_related.read_model_folders_result import ReadModelFoldersResult


@dataclass
class MainFolderValidationResult:
    is_valid: bool
    error: Union[str, None] = None


class FoldersAndFilesService:
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
    def _is_file_an_allowed_image(file_name: str) -> bool:
        """
        Check if the file extension is one 
        of the allowed ones
        """

        _, file_extension = os.path.splitext(file_name)
        return file_extension in configs.ALLOWED_IMAGE_FILE_TYPES

    @staticmethod
    def _get_classes_and_corresponding_files_from(
        folder_path: str
    ) -> aliases.FoldersClassesAndFiles:
        """
        Read the selected directory content and
        the contents of the expected directories
        """

        result: aliases.FoldersClassesAndFiles = {}

        for subfolder in ExpectedSubfolders:
            subfolder_path = os.path.join(folder_path, subfolder.value)
            result[subfolder] = {}

            for clasz in ModelClasses:
                class_folder_path = os.path.join(subfolder_path, clasz.value)
                class_folder_content = os.listdir(class_folder_path)

                result[subfolder][clasz] = list(
                    filter(FoldersAndFilesService._is_file_an_allowed_image, class_folder_content))

        return result

    @staticmethod
    def read_model_folders_and_files() -> ReadModelFoldersResult:
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

            validation_result = FoldersAndFilesService._validate_model_main_folder(folder_path)

            if not validation_result.is_valid:
                return ReadModelFoldersResult(error=validation_result.error)

            read_result = FoldersAndFilesService._get_classes_and_corresponding_files_from(folder_path)

            return ReadModelFoldersResult(folders_classes_and_files=read_result)
        except Exception as e:
            print(f"Exception on MultipleFilesService.read_model_folders_and_files: {e}")
            return ReadModelFoldersResult(error="Um erro inesperado aconteceu")
