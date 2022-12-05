from typing import Union
from dataclasses import dataclass

from globals import aliases


@dataclass
class ReadModelFoldersResult:
    error: Union[str, None] = None
    folders_classes_and_files: Union[aliases.FoldersClassesAndFiles, None] = None
