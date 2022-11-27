from typing import Union
from dataclasses import dataclass

from globals import aliases


@dataclass
class ReadDirResult:
    error: Union[str, None] = None
    folder_classes_and_files: Union[aliases.FoldersClassesAndFiles, None] = None
