import numpy as np
from typing import Tuple, List
from python.visualise.PointAnimationData import PointAnimationData


class DynamicPointPlot3DAnimationDataForTesting(PointAnimationData):
    """
    Supply on the fly animation data for 3D Points
    """

    def __init__(self,
                 num_points: int,
                 x_range: Tuple[float, float],
                 y_range: Tuple[float, float],
                 step_size: float = 0.05):
        self._num_points: int = num_points
        self._step_size = step_size
        self._ranges: List[Tuple[float, float]] = [x_range, y_range]
        self._points: np.ndarray = np.zeros((self._num_points, 2))
        for i in range(self._num_points):
            self._points[i] = [r[0] + (x * (r[1] - r[0])) for x, r in
                               zip(np.random.rand(self._num_points), self._ranges)]
        return

    def get_data_for_frame(self,
                           frame_idx: int) -> np.ndarray:
        """
        For each point Add random +/- noise of the defined step size and clip to the x, y, z defined ranges.
        :param frame_idx: not used.
        :return: the updated points
        """
        for i in range(self._num_points):
            # Add random +/- noise of the defined step size and clip to the x, y, z defined ranges.
            self._points[i] = [(lambda v, l, u: l if v < l else u if v > u else v)(v, g[0], g[1]) for v, g in
                               zip([x + p for x, p in
                                    zip(((np.random.rand(self._num_points) - 0.5) * self._step_size) * 2.0,
                                        self._points[i])], self._ranges)]
        return self._points

    def num_points(self) -> int:
        return PointAnimationData.INF_POINTS

    def point_shape(self) -> Tuple:
        return (2,)  # NOQA
