from enum import Enum


class ExpectedSubfoldersInChosenFolder(str, Enum):
    TRAIN = "train"
    TEST = "test"
    VALIDATION = "val"
