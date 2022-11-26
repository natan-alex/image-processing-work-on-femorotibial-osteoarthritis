from PIL import Image as PilImages
from typing import Dict, List


Image = PilImages.Image
ClassesAndFiles = Dict[str, List[str]]
FoldersClassesAndFiles = Dict[str, ClassesAndFiles]
