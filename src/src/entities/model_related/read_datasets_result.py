from typing import Union
from dataclasses import dataclass

from globals import aliases


@dataclass
class ReadDatasetsResult:
    error: Union[str, None] = None
    datasets: Union[aliases.Datasets, None] = None
    folder_path: str =None