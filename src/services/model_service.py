import numpy as np
import tensorflow as tf

from typing import Tuple

from globals import configs, aliases

from entities.model_related.model_classes import ModelClasses
from entities.model_related.expected_subfolders import ExpectedSubfolders


class ModelService:
    @staticmethod
    def build_model(infos: aliases.Datasets):
        try:
            inception_model = tf.keras.applications.InceptionV3(weights="imagenet", include_top=False)

            for layer in inception_model.layers:
                layer.trainable = False

            input_layer = tf.keras.Input(shape=configs.MODEL_IMAGES_SIZE + (3,))

            temp = tf.keras.layers.Conv2D(128, (7, 7), padding="same", activation="relu", strides=(2, 2))(input_layer)

            temp = inception_model(temp)

            temp = tf.keras.layers.Dropout(rate=0.2)(temp)

            output_layer = tf.keras.layers.Dense(
                len(list(ModelClasses)),
                activation="softmax")(temp)

            model = tf.keras.Model(inputs=input_layer, outputs=output_layer)
            model.compile(
                optimizer=tf.keras.optimizers.Adam(),
                loss=tf.keras.losses.CategoricalCrossentropy,
                metrics=[tf.keras.metrics.Accuracy])
            model.fit_generator(
                infos[ExpectedSubfolders.TRAIN],
                epochs=2)
            model.summary()
        except Exception as e:
            print(f"Exception on ModelService.load_model_from_file: {e}")
            return
