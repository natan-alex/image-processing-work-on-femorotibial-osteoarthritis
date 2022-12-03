# Global app configurations

import os

MAIN_WINDOW_WIDTH = 350
MAIN_WINDOW_HEIGHT = 500

IMAGES_WINDOW_WIDTH = 640
IMAGES_WINDOW_HEIGHT = 480

AI_WINDOW_WIDTH = 550
AI_WINDOW_HEIGHT = 450

ALLOWED_IMAGE_FILE_TYPES = [".jpg", ".jpeg", ".png"]

MODEL_IMAGES_SIZE = (299, 299)

ROOT_FOLDER_PATH = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

SAVED_MODEL_FILE_PATH = os.path.join(ROOT_FOLDER_PATH, "saved_model", "saved_model.h5")
