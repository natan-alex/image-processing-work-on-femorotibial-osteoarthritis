import os
import tkinter.filedialog as tk_files

from globals import aliases, configs
from entities.model_related.model_classes import ModelClasses
from entities.model_related.expected_subfolders import ExpectedSubfolders
from entities.model_related.read_dir_result import ReadDirResult


class TrainingModelService:
    file_types = [
        ("Imagens", " ".join(configs.ALLOWED_IMAGE_FILE_TYPES)),
        ("Todos os arquivos", "*.*")
    ]

    subfolders_error_message = """
    A pasta escolhida deve conter as seguintes subpastas:
    {0}
    Essas subpastas ({0}) correspondem a cada uma das etapas de construção do modelo.
    Cada uma dessas subpastas deve conter as seguintes "subsubpastas":
    {1}
    Essas "subsubpastas" ({1}) correspondem a cada uma das possíveis classes de uma imagem.
    Essas "subsubpastas" são as que devem conter de fato as imagens que serão utilizadas pelo modelo
    """.format(
        ", ".join(list(ExpectedSubfolders)),
        ", ".join(list(ModelClasses)))

    @staticmethod
    def read_model_related_folders_and_files() -> ReadDirResult:
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

            if not TrainingModelService._are_folder_subfolders_valid(folder_path):
                return ReadDirResult(error=TrainingModelService.subfolders_error_message)

            return ReadDirResult(
                folder_classes_and_files=TrainingModelService
                ._get_classes_and_corresponding_files_from(folder_path))
        except Exception as e:
            print(f"Exception on MultipleFilesService.read_files_and_corresponding_classes: {e}")
            return ReadDirResult(error=f"Something wrong happened. Error: {e}")

    @staticmethod
    def _are_folder_subfolders_valid(folder_path: str) -> bool:
        """
        Check if the selected directory contains the 
        necessary and expected model files
        """

        if not os.path.isdir(folder_path):
            return False

        folder_content = os.listdir(folder_path)

        for subfolder in list(ExpectedSubfolders):
            if subfolder.value not in folder_content:
                return False

            subfolder_path = os.path.join(folder_path, subfolder.value)
            subfolder_content = os.listdir(subfolder_path)

            for clasz in list(ModelClasses):
                if clasz.value not in subfolder_content:
                    return False

        return True

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

        folder_classes_and_files: aliases.FoldersClassesAndFiles = {}

        for subfolder in list(ExpectedSubfolders):
            folder_classes_and_files[subfolder.value] = {}

            subfolder_path = os.path.join(folder_path, subfolder.value)

            for clasz in list(ModelClasses):
                class_folder_path = os.path.join(subfolder_path, clasz.value)
                class_folder_content = os.listdir(class_folder_path)

                folder_classes_and_files[subfolder.value][clasz.value] = list(filter(
                    TrainingModelService._is_file_an_allowed_image, class_folder_content))

        return folder_classes_and_files
