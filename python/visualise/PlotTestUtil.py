import numpy as np
from typing import Tuple


class PlotTestUtil:
    """
    Simple utilities for plot testing
    """

    @classmethod
    def generate_random_animation_data(cls,
                                       num_samples: int,
                                       points_per_sample: int,
                                       datums_per_point: int):
        data = np.zeros((num_samples, points_per_sample, datums_per_point))
        data_shape = np.shape(data)
        for i in range(data_shape[0]):
            for j in range(data_shape[1]):
                if i == 0:
                    idx = 0
                    for r in np.random.random(data_shape[2]):
                        data[i][j][idx] = r
                        idx += 1
                else:
                    s = 1
                    if np.random.rand() > 0.5:
                        s = -1
                    idx = 0
                    for r in np.random.random(data_shape[data_shape[2]]):
                        data[i][j][idx] = (data[i - 1][j][idx] + (r * .07 * s)) % 1
                        idx += 1
        return data

    @classmethod
    def generate_xy_range_animation_data(cls,
                                         x_range: Tuple[float, float, float],
                                         y_range: Tuple[float, float, float]):

        xr = np.arange(x_range[0], x_range[1], x_range[2])
        yr = np.arange(y_range[0], y_range[1], y_range[2])
        num_samples = len(xr)
        if len(yr) != num_samples:
            raise ValueError(f'X & Y ranges must specify same number of points, but given x{num_samples} y{len(yr)}')

        data = np.zeros((num_samples, 1, 2))
        for i in range(num_samples):
            data[i][0][0] = xr[i]
            data[i][0][1] = yr[i]
        return data
