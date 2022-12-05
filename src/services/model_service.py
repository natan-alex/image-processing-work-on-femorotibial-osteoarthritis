import os
import numpy as np
import tensorflow as tf
import seaborn as sn
import matplotlib.pyplot as plt

from sklearn import metrics

from typing import Union

from globals import configs, aliases

from entities.model_related.model_classes import ModelClasses
from entities.model_related.expected_subfolders import ExpectedSubfolders
from entities.model_related.model_evaluation_metrics import ModelEvaluationMetrics


np.seterr(divide="ignore", invalid="ignore")


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
        """ Add layers on top of inceptionV3 model to generate a new one """

        input_layer = tf.keras.Input(shape=configs.MODEL_IMAGES_SIZE + (3,))

        inception_model = tf.keras.applications.InceptionV3(
            weights="imagenet", include_top=False, input_tensor=input_layer)

        inception_model.trainable = False

        number_of_classes = len(list(ModelClasses))

        x = tf.keras.layers.Flatten()(inception_model.output)

        x = tf.keras.layers.Dropout(rate=0.2)(x)

        output_layer = tf.keras.layers.Dense(
            number_of_classes, 
            activation=tf.keras.activations.softmax)(x)

        return tf.keras.Model(inputs=input_layer, outputs=output_layer)

    @staticmethod
    def create_and_train_model(
        datasets: aliases.Datasets,
        epochs: int = configs.MODEL_TRAINING_EPOCHS,
        start_from_checkpoint = False
    ) -> Union[aliases.Model, None]:
        """
        Create model from checkpoint or from inception model,
        compile it to get metrics and train it with the train dataset
        """

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
            print(f"Exception on ModelService.create_and_train_model: {e}")
            return None

    @staticmethod
    def evaluate_model_and_get_metrics(
        model: aliases.Model, datasets: aliases.Datasets
    ) -> ModelEvaluationMetrics:
        """
        Evaluate the model using the test dataset
        Predict the classes for the test images, get the
        maximum values on predictions to know the most "strong"
        class and group everything to calculate the metrics
        """

        test_dataset = datasets[ExpectedSubfolders.TEST]

        y_prediction = model.predict(test_dataset)

        predicted_classes = np.argmax(y_prediction, axis=1)

        classes = np.concatenate([y for _, y in test_dataset], axis=0)

        classes = np.argmax(classes, axis=1)

        return ModelService._calculate_and_get_metrics(predicted_classes, classes)

    @staticmethod
    def _manipulate_to_show(array: aliases.NpArray) -> float:
        """ Manipulate the score_per_class metric removing the invalid things, get mean and round it """

        replaced = np.nan_to_num(array)
        mean = float(np.mean(replaced))
        return round(mean, 3)

    @staticmethod
    def _calculate_and_get_metrics(
        predicted_classes: aliases.NpArray,
        classes: aliases.NpArray
    ) -> ModelEvaluationMetrics:
        """ Generate confusion matrix and get scores """

        matrix = metrics.confusion_matrix(predicted_classes, classes)

        fp = matrix.sum(axis=0) - np.diag(matrix)  
        fn = matrix.sum(axis=1) - np.diag(matrix)
        tp = np.diag(matrix)
        tn = matrix.sum() - (fp + fn + tp)

        precision_per_class = tp / (tp + fp)
        accuracy_per_class = (tp + tn) / (tp + tn + fp + fn)
        f1_score_per_class = (2 * tp) / (2 * tp + fp + fn)
        specificity_per_class = tn / (tn + fp)
        sensitivity_per_class = tp / (tp + fn)

        return ModelEvaluationMetrics(
            confusion_matrix=matrix,
            precision_score=ModelService._manipulate_to_show(precision_per_class),
            accuracy_score=ModelService._manipulate_to_show(accuracy_per_class),
            specificity_score=ModelService._manipulate_to_show(specificity_per_class),
            sensitivity_score=ModelService._manipulate_to_show(sensitivity_per_class),
            f1_score=ModelService._manipulate_to_show(f1_score_per_class),
        )

    @staticmethod
    def plot_confusion_matrix(matrix: aliases.ConfusionMatrix):
        sn.heatmap(matrix, annot=True)

        plt.ylabel("Classe real")
        plt.xlabel("Classe predita")

        plt.show()
