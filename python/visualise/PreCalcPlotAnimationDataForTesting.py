import numpy as np
from typing import Tuple
from python.visualise.PointAnimationData import PointAnimationData


class PreCalcPointPlotAnimationDataForTesting(PointAnimationData):
    """
    Supply pre-calculated data for animated points
    """

    def __init__(self,
                 data: np.ndarray):
        """
        Constructor, just store the pre-calculated data that will be returned as frame data.
        :param data: The data points to store and return as frame data
        """
        self._data = data
        return

    def get_data_for_frame(self,
                           frame_idx: int) -> np.ndarray:
        return self._data[frame_idx % self.num_frames()]

    def num_frames(self) -> int:
        return np.shape(self._data)[0]

    def frame_data_shape(self) -> Tuple:
        return np.shape(self._data[0][0])
