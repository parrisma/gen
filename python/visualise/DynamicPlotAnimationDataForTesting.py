import numpy as np
from typing import Tuple
from python.visualise.PointAnimationData import PointAnimationData


class DynamicPointPlotAnimationDataForTesting(PointAnimationData):
    """
    Supply on the fly animation data
    """
    _MIN: int = 0
    _MAX: int = 1

    def __init__(self,
                 x_range=Tuple[float, float],
                 y_range=Tuple[float, float]):
        self._x_range = x_range
        self._y_range = y_range
        self._last_x = None
        self._last_y = None
        return

    def get_data_for_frame(self,
                           frame_idx: int) -> np.ndarray:
        if self._last_x is None:
            self._last_x = self._x_range[self._MIN] + (
                    (self._x_range[self._MAX] - self._x_range[self._MIN]) * np.random.rand())
            self._last_y = self._y_range[self._MIN] + (
                    (self._y_range[self._MAX] - self._y_range[self._MIN]) * np.random.rand())
        else:
            self._last_x += ((np.random.rand() * 2) - 1) * .1
            self._last_x = np.maximum(self._last_x, self._x_range[self._MIN])
            self._last_x = np.minimum(self._last_x, self._x_range[self._MAX])

            self._last_y += ((np.random.rand() * 2) - 1) * .1
            self._last_y = np.maximum(self._last_y, self._y_range[self._MIN])
            self._last_y = np.minimum(self._last_y, self._y_range[self._MAX])

        return np.array([self._last_x, self._last_y]).reshape((1, 2))

    def num_frames(self) -> int:
        return PointAnimationData.INF_POINTS

    def frame_data_shape(self) -> Tuple:
        return (2,)  # NOQA
