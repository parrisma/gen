import numpy as np
from python.visualise.PlotAnimationData import PlotAnimationData


class PreCalcPointPlotAnimationDataForTesting(PlotAnimationData):
    """
    Supply pre-calculated data for animated points
    """

    def __init__(self,
                 data: np.ndarray):
        self._data = data
        return

    def get_data_for_frame(self,
                           frame_idx: int) -> np.ndarray:
        return self._data[frame_idx]

    def num_points(self) -> int:
        return np.shape(self._data)[0]

    def point_shape(self):
        return np.shape(self._data[0][0])
