import cv2
import numpy as np
from typing import Tuple
from PIL import Image


class CorrelationService:
    @staticmethod
    def find_cross_correlation_between(
        image: Image,
        template: Image,
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        try:
            image_as_np_array = np.array(image)
            template_as_np_array = np.array(template)

            correlation = cv2.matchTemplate(
                image_as_np_array,
                template_as_np_array,
                cv2.TM_CCOEFF_NORMED
            )

            template_height, template_width, _ = template_as_np_array.shape
            y, x = np.unravel_index(np.argmax(correlation), correlation.shape)

            return (
                (x, y),
                (x + template_width, y + template_height)
            )
        except Exception as e:
            print(e)
            return None
