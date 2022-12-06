import os
import cv2
import numpy as np
import tensorflow as tf
import seaborn as sn
import xgboost
import matplotlib.pyplot as plt

from sklearn import metrics, model_selection, preprocessing
from sklearn.ensemble import RandomForestClassifier

from typing import Union, Any, Tuple

from globals import configs, aliases

from entities.model_related.model_classes import ModelClasses
from entities.model_related.expected_subfolders import ExpectedSubfolders
from entities.model_related.model_evaluation_metrics import ModelEvaluationMetrics


np.seterr(divide="ignore", invalid="ignore")


import sys
out = sys.stdout


class ModelService:
    @staticmethod
    def _load_saved_model(path: str) -> Union[aliases.Model, None]:
        try:
            if os.path.isfile(path):
                return tf.keras.models.load_model(path)

            return None
        except Exception as e:
            print(f"Exception on ModelService.load_saved_model: {e}")
            return None

    @staticmethod
    def load_saved_neural_network() -> Union[aliases.Model, None]:
        return ModelService._load_saved_model(configs.SAVED_NEURAL_NETWORK_FILE_PATH)

    @staticmethod
    def load_saved_xgboost() -> Union[aliases.Model, None]:
        return ModelService._load_saved_model(configs.SAVED_XGBOOST_FILE_PATH)

    @staticmethod
    def _load_model_from_checkpoint(path: str) -> Union[aliases.Model, None]:
        try:
            if os.path.isfile(path):
                return tf.keras.models.load_model(path)

            return None
        except Exception as e:
            print(f"Exception on ModelService.load_model_from_checkpoint: {e}")
            return None

    @staticmethod
    def load_neural_network_from_checkpoint() -> Union[aliases.Model, None]:
        return ModelService._load_model_from_checkpoint(configs.NEURAL_NETWORK_CHECKPOINT_FILE_PATH)

    @staticmethod
    def _save_model(model: aliases.Model, path: str) -> bool:
        try:
            model.save(path)
            return True
        except Exception as e:
            print(f"Exception on ModelService.save_model: {e}")
            return False

    @staticmethod
    def save_neural_network(model: aliases.Model) -> bool:
        return ModelService._save_model(model, configs.SAVED_NEURAL_NETWORK_FILE_PATH)

    @staticmethod
    def save_xgboost(model: aliases.Model) -> bool:
        return ModelService._save_model(model, configs.SAVED_XGBOOST_FILE_PATH)

    @staticmethod
    def _has_fit_checkpoint(path: str):
        try:
            return os.path.isfile(path)
        except Exception as e:
            print(f"Exception on ModelService.has_fit_checkpoint: {e}")
            return False

    @staticmethod
    def neural_network_has_fit_checkpoint() -> bool:
        return ModelService._has_fit_checkpoint(configs.NEURAL_NETWORK_CHECKPOINT_FILE_PATH)

    @staticmethod
    def _create_neural_network_with_layers() -> Union[aliases.Model, None]:
        """ Add layers on top of inceptionV3 model to generate a new one """

        try:
            input_layer = tf.keras.Input(shape=configs.NEURAL_NETWORK_IMAGES_SIZE + (3,))

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
        except Exception as e:
            print(f"Exception on ModelService.create_and_train_neural_network: {e}")
            return None

    @staticmethod
    def get_images_and_labels_from(
        dataset: aliases.Dataset,
        image_size: Tuple[int, int],
        cv_read_model: Any,
        image_resize_mode: Any = None,
    ):
        images = []
        classes = []

        for path in dataset.file_paths:
            class_name = os.path.basename(os.path.dirname(path))
            classes.append(class_name)

            image = cv2.imread(path, cv_read_model)

            if image_resize_mode is None:
                images.append(cv2.resize(image, image_size))
            else:
                images.append(cv2.resize(image, image_size, image_resize_mode))

        label_encoder = preprocessing.LabelEncoder()
        label_encoder.fit(classes)

        return (np.array(images) / 255, label_encoder.transform(classes))

    @staticmethod
    def create_and_train_xgboost(
        dataset: aliases.Dataset
    ) -> Union[aliases.Model, None]:
        try:
            model = xgboost.XGBRegressor(
                objective="reg:squarederror",
                colsample_bytree=0.3,
                learning_rate=0.05,
                max_depth=5,
                alpha=10,
                n_estimators=10)

            images, labels = ModelService \
                .get_images_and_labels_from(dataset, (150, 150), cv2.IMREAD_GRAYSCALE)

            x_train, _, y_train, _ = model_selection \
                .train_test_split(images, labels, train_size=0.99, random_state=123)

            x_train = x_train.reshape(x_train.shape[0], -1)

            model.fit(x_train, y_train)

            return model
        except Exception as e:
            print(f"Exception on ModelService.create_and_train_xgboost: {e}")
            return None

    @staticmethod
    def create_and_train_neural_network(
        datasets: aliases.Datasets,
        epochs: int = configs.MODEL_TRAINING_EPOCHS,
        start_from_checkpoint = False
    ) -> Union[aliases.Model, None]:
        """
        Create model from checkpoint or from inception model,
        compile it to get metrics and train it with the train dataset
        """

        try:
            checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
                filepath=configs.NEURAL_NETWORK_CHECKPOINT_FILE_PATH,
                save_best_only=True, verbose=1)

            model = None

            if start_from_checkpoint and ModelService.neural_network_has_fit_checkpoint():
                model = ModelService.load_neural_network_from_checkpoint()
            else:
                model = ModelService._create_neural_network_with_layers()

            if model is None:
                return None

            model.compile(
                optimizer=tf.keras.optimizers.Adam(),
                loss=tf.keras.losses.CategoricalCrossentropy(),
                metrics=[tf.keras.metrics.Accuracy(), tf.keras.metrics.Precision()])

            model.fit(
                datasets[ExpectedSubfolders.TRAIN],
                validation_data=datasets[ExpectedSubfolders.VALIDATION],
                epochs=epochs, callbacks=[checkpoint_callback])

            return model
        except Exception as e:
            print(f"Exception on ModelService.create_and_train_neural_network: {e}")
            return None

    @staticmethod
    def create_and_train_random_forest_classifier(dataset: aliases.Dataset):
        model = RandomForestClassifier(
            n_estimators=200,
            min_samples_split=6,
            min_samples_leaf=8,
            max_features="sqrt",
            max_depth=19,
            criterion="entropy")

        images, labels = ModelService \
            .get_images_and_labels_from(dataset, (150, 200), cv2.IMREAD_GRAYSCALE, cv2.INTER_AREA)

        x_train, _, y_train, _ = model_selection \
            .train_test_split(images, labels, train_size=0.99, random_state=123)

        x_train = x_train.reshape(x_train.shape[0], -1)

        model.fit(x_train, y_train)

        return model

    @staticmethod
    def evaluate_model_and_get_metrics(
        model: aliases.Model,
        datasets: aliases.Datasets
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
    def _format_metric_value(array: aliases.NpArray) -> float:
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
            precision_score=ModelService._format_metric_value(precision_per_class),
            accuracy_score=ModelService._format_metric_value(accuracy_per_class),
            specificity_score=ModelService._format_metric_value(specificity_per_class),
            sensitivity_score=ModelService._format_metric_value(sensitivity_per_class),
            f1_score=ModelService._format_metric_value(f1_score_per_class),
        )

    @staticmethod
    def plot_confusion_matrix(matrix: aliases.ConfusionMatrix):
        sn.heatmap(matrix, annot=True)

        plt.ylabel("Classe real")
        plt.xlabel("Classe predita")

        plt.show()
