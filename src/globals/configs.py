# Global app configurations

import os

MAIN_WINDOW_WIDTH = 350
MAIN_WINDOW_HEIGHT = 500

IMAGES_WINDOW_WIDTH = 640
IMAGES_WINDOW_HEIGHT = 480

AI_WINDOW_WIDTH = 550
AI_WINDOW_HEIGHT = 450

ALLOWED_IMAGE_FILE_TYPES = [".jpg", ".jpeg", ".png"]

MODEL_TRAINING_EPOCHS = 2

ROOT_FOLDER_PATH = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

SAVED_MODELS_FOLDER_PATH = os.path.join(ROOT_FOLDER_PATH, "saved_models")

SAVED_XGBOOST_FILE_PATH = os.path.join(SAVED_MODELS_FOLDER_PATH, "saved_xgboost.h5")

SAVED_NEURAL_NETWORK_FILE_PATH = os.path.join(SAVED_MODELS_FOLDER_PATH, "saved_neural_network.h5")
NEURAL_NETWORK_CHECKPOINT_FILE_PATH = os.path.join(SAVED_MODELS_FOLDER_PATH, "neural_network_checkpoint.h5")
NEURAL_NETWORK_IMAGES_SIZE = (299, 299)
