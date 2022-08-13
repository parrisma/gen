from abc import ABC, abstractmethod
import sys
from typing import Tuple
import numpy as np


class PointAnimationData(ABC):
    """
    A class that supplies frame by frame data to Matplotlib animation
    """

    INF_POINTS: int = sys.maxsize

    @abstractmethod
    def get_data_for_frame(self,
                           frame_idx: int) -> np.ndarray:
        """
        Get the data for a given animation frame
        :return: A numpy array of the expected shape for the given animation
        """
        raise NotImplementedError

    @abstractmethod
    def num_frames(self) -> int:
        """
        The number of animation data frames available
        :return: The number of points or INF_POINTS is the class is supplying a live stream of data
        """
        raise NotImplementedError

    @abstractmethod
    def frame_data_shape(self) -> Tuple:
        """
        The numpy shape of a single frame of data
        :return: The numpy shape of a single frame of data
        """
        raise NotImplementedError
