import cv2
import numpy as np
from typing import Tuple, Union
from aliases import Image


class CorrelationService:
    @staticmethod
    def _find_correlation_point(image: np.ndarray, template: np.ndarray):
        try:
            correlation = cv2.matchTemplate(
                image, template, cv2.TM_CCOEFF_NORMED
            )

            argmax = np.argmax(correlation)
            y, x = np.unravel_index(argmax, correlation.shape)

            return (x, y)
        except Exception as e:
            print(f"Exception on CorrelationService.find_correlation_point: {e}")
            return None

    @staticmethod
    def find_cross_correlation_between(
        image: Image,
        template: Image,
    ) -> Union[Tuple[int, int], Tuple[int, int], None]:
        try:
            image_array = np.array(image)
            template_array = np.array(template)

            point = CorrelationService. \
                _find_correlation_point(image_array, template_array)

            if point is None:
                return None

            template_height = template_array.shape[0]
            template_width = template_array.shape[1]

            return (
                (point[0], point[1]),
                (point[0] + template_width, point[1] + template_height)
            )
        except Exception as e:
            print(f"Exception on CorrelationService.find_cross_correlation_between: {e}")
            return None
