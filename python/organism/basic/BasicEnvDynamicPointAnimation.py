import numpy as np
from typing import Tuple, List
from python.visualise.PointAnimationData import PointAnimationData


class BasicEnvDynamicPointAnimation(PointAnimationData):
    """
    Supply on the fly animation data for 3D Points.
    """

    def __init__(self,
                 frame_data: List[Tuple]):
        self._frame_data = frame_data
        return

    def get_data_for_frame(self,
                           frame_idx: int) -> np.ndarray:
        """
        For each point Add random +/- noise of the defined step size and clip to the x, y, z defined ranges
        :param frame_idx: not used.
        :return: the updated points
        """
        points: np.ndarray = np.zeros((len(self._frame_data), 3))
        point: Tuple[float, float, float]
        for i, point in enumerate(self._frame_data):
            points[i][0], points[i][1], points[i][2] = point
        return points

    def num_frames(self) -> int:
        """
        The max number of data frames that will be returned.
        :return: MAX_INT as this is dynamic / on the fly there is no defined end frame.
        """
        return PointAnimationData.INF_POINTS

    def frame_data_shape(self) -> Tuple:
        """
        The data frame is the x,y coordinate to be re-calculated, so shape is 2,
        :return: Tuple(3) as frame is simple two float values for light gene, drought gene, fitness (x,y,z)
        """
        return (3,)  # NOQA
