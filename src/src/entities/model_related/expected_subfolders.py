from enum import Enum


class ExpectedSubfolders(str, Enum):
    TRAIN = "train"
    TEST = "test"
    VALIDATION = "val"
