from abc import ABC, abstractmethod
import sys
import numpy as np


class PlotAnimationData(ABC):
    """
    A class that supplies frame by frame data to Matplotlib animation
    """

    INF_POINTS: int = sys.maxsize

    @abstractmethod
    def get_data_for_frame(self,
                           frame_idx: int) -> np.ndarray:
        """
        Get the data for a given animation frame
        :return: A numpy array of the expected shape for teh given animation
        """
        raise NotImplementedError

    @abstractmethod
    def num_points(self) -> int:
        """
        The number of animation data points available
        :return: The number of points or INF_POINTS is the class is supplying a live stream of data
        """
        raise NotImplementedError

    @abstractmethod
    def point_shape(self):
        """
        The numpy shape of a single point
        :return: The numpy shape of a single point
        """
        raise NotImplementedError
