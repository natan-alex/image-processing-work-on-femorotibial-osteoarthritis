import numpy as np
import tensorflow as tf

from PIL import Image as PilImages
from typing import Dict, List

from entities.model_related.model_classes import ModelClasses
from entities.model_related.expected_subfolders import ExpectedSubfolders


Image = PilImages.Image
Dataset = tf.data.Dataset
Datasets = Dict[ExpectedSubfolders, Dataset]
ClassFileCount = Dict[ModelClasses, int]
ClassesAndFiles = Dict[ModelClasses, List[str]]
FoldersClassesAndFiles = Dict[ExpectedSubfolders, ClassesAndFiles]
Model = tf.keras.Model
ConfusionMatrix = np.ndarray
NpArray = np.ndarray
