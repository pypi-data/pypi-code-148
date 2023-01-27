from typing import List

import cv2
import numpy as np
from numpy import ndarray

from aipose.model import Keypoints
from aipose.plot import plot


class FrameManager:
    def __init__(self):
        pass

    def on_frame(self, frame: ndarray) -> ndarray:
        return frame


class FramePlot(FrameManager):
    def __init__(self, model):
        self.model = model

    def on_frame(self, frame: ndarray) -> ndarray:
        prediction, image_tensor = self.model(frame)
        frame = self._plot(prediction, image_tensor)
        return frame

    def _plot(self, prediction: List[Keypoints], image_tensor: ndarray) -> ndarray:
        frame = plot(
            image_tensor,
            np.array([value.get_raw_keypoint() for value in prediction]),
            plot_image=False,
            return_img=True,
        )
        return frame


def process_webcam(frame_manaer: FrameManager):
    capture = cv2.VideoCapture(0)

    while capture.isOpened():
        import torch

        torch.cuda.empty_cache()

        ret, frame = capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame_manaer.on_frame(frame)

        cv2.imshow("webCam", frame)
        if cv2.waitKey(1) == ord("s"):
            break

    capture.release()
    cv2.destroyAllWindows()
