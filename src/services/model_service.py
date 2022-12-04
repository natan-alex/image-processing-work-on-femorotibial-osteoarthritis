import os
import tensorflow as tf

from typing import Union

from globals import configs, aliases

from entities.model_related.model_classes import ModelClasses
from entities.model_related.expected_subfolders import ExpectedSubfolders


class ModelService:
    _checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=configs.MODEL_FIT_CHECKPOINT_FILE_PATH,
        save_best_only=True, verbose=1)

    @staticmethod
    def load_saved_model() -> Union[aliases.Model, None]:
        try:
            if os.path.isfile(configs.SAVED_MODEL_FILE_PATH):
                return tf.keras.models.load_model(configs.SAVED_MODEL_FILE_PATH)

            return None
        except Exception as e:
            print(f"Exception on ModelService.load_saved_model: {e}")
            return None

    @staticmethod
    def load_model_from_checkpoint() -> Union[aliases.Model, None]:
        try:
            if os.path.isfile(configs.MODEL_FIT_CHECKPOINT_FILE_PATH):
                return tf.keras.models.load_model(configs.MODEL_FIT_CHECKPOINT_FILE_PATH)

            return None
        except Exception as e:
            print(f"Exception on ModelService.load_model_from_checkpoint: {e}")
            return None

    @staticmethod
    def save_model(model: aliases.Model) -> bool:
        try:
            model.save(configs.SAVED_MODEL_FILE_PATH)
            return True
        except Exception as e:
            print(f"Exception on ModelService.save_model: {e}")
            return False

    @staticmethod
    def has_fit_checkpoint():
        try:
            return os.path.isfile(configs.MODEL_FIT_CHECKPOINT_FILE_PATH)
        except Exception as e:
            print(f"Exception on ModelService.has_fit_checkpoint: {e}")
            return False

    @staticmethod
    def _create_model_with_layers() -> aliases.Model:
        input_layer = tf.keras.Input(shape=configs.MODEL_IMAGES_SIZE + (3,))

        inception_model = tf.keras.applications.InceptionV3(
            weights="imagenet", include_top=False, input_tensor=input_layer)

        inception_model.trainable = False

        number_of_classes = len(list(ModelClasses))

        x = tf.keras.layers.Flatten()(inception_model.output)

        x = tf.keras.layers.Dropout(rate=0.2)(x)

        output_layer = tf.keras.layers.Dense(
            number_of_classes, 
            activation=tf.keras.activations.softmax,
            kernel_regularizer=tf.keras.regularizers.l2(0.0001))(x)

        return tf.keras.Model(inputs=input_layer, outputs=output_layer)

    @staticmethod
    def create_and_train_model(
        datasets: aliases.Datasets,
        epochs: int = configs.MODEL_TRAINING_EPOCHS,
        start_from_checkpoint = False
    ) -> Union[aliases.Model, None]:
        try:
            if start_from_checkpoint and ModelService.has_fit_checkpoint():
                model = ModelService.load_model_from_checkpoint()
            else:
                model = ModelService._create_model_with_layers()

            model.compile(
                optimizer=tf.keras.optimizers.Adam(),
                loss=tf.keras.losses.CategoricalCrossentropy(),
                metrics=[tf.keras.metrics.Accuracy(), tf.keras.metrics.Precision()])

            model.fit(
                datasets[ExpectedSubfolders.TRAIN],
                validation_data=datasets[ExpectedSubfolders.VALIDATION],
                epochs=epochs, callbacks=[ModelService._checkpoint_callback])

            return model
        except Exception as e:
            print(f"Exception on ModelService.build_model: {e}")
            return None

    @staticmethod
    def evaluate_model(model: aliases.Model, datasets: aliases.Datasets):
        model.evaluate(datasets[ExpectedSubfolders.TEST], verbose=1)
