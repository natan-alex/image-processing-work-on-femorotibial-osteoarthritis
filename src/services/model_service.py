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
            input_layer = tf.keras.Input(shape=configs.MODEL_IMAGES_SIZE + (3,))

            inception_model = tf.keras.applications.InceptionV3(
                weights="imagenet", include_top=False, input_tensor=input_layer)

            for layer in inception_model.layers:
                layer.trainable = False

            x = tf.keras.layers.Flatten()(inception_model.output)

            x = tf.keras.layers.Dropout(rate=0.2)(x)

            output_layer = tf.keras.layers.Dense(
                len(list(ModelClasses)),
                activation=tf.keras.activations.softmax)(x)

            model = tf.keras.Model(inputs=[input_layer], outputs=[output_layer])

            model.compile(
                optimizer=tf.keras.optimizers.Adam(),
                loss=tf.keras.losses.CategoricalCrossentropy(),
                metrics=[tf.keras.metrics.Accuracy()])

            model.fit_generator(
                infos[ExpectedSubfolders.TRAIN],
                epochs=2)

            model.summary()
        except Exception as e:
            print(f"Exception on ModelService.load_model_from_file: {e}")
            return
