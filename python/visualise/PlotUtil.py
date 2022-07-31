from typing import Tuple, Callable, Union
import numpy as np


class PlotUtil:
    @classmethod
    def render_function(cls,
                        x: np.ndarray,
                        y: np.ndarray,
                        func: Callable[[float, float], float],
                        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Render the given function over x, y values in a form that can be contour or surface plotted
        :param x: The values of X to plot for (must have same length as Y)
        :param y: The values of Y to plot for (must have same length as X)
        :param func: The function of x,y to render
        :return x,y,z values in form for plotting a contour or surface
        """
        nx = len(x)
        ny = len(y)

        # Calculate z using given function.
        _z = np.zeros((nx, ny), dtype='d')
        for i in range(nx):
            for j in range(ny):
                _z[i, j] = func(x[i], y[j])

        # Establish x, y for plotting.
        _x, _y = np.meshgrid(x, y)
        return _x, _y, _z

    @classmethod
    def axis_configuration(cls,
                           axes,
                           title: str,
                           x_label: str,
                           y_label: str,
                           z_label: str = None,
                           x_ticks: Tuple[float, float, float] = None,
                           y_ticks: Tuple[float, float, float] = None,
                           z_ticks: Tuple[float, float, float] = None,
                           title_text_size: int = 16,
                           axis_text_size: int = 14) -> None:
        """
        Configure titles and axis ticks and labels.
        :param axes: The Matplot Lib axis to configure
        :param title: The Title of the Graph
        :param x_label: The Label for the x-axis
        :param y_label: The Label for the y-axis
        :param z_label: The Label for the z-axis - optional
        :param x_ticks: X Axis ticks, (start, end, step) - optional
        :param y_ticks: Y Axis ticks, (start, end, step) - optional
        :param z_ticks: Z Axis ticks, (start, end, step) - optional
        :param title_text_size: Size in points of plot title - default = 16pts
        :param axis_text_size: Size in points of axes labels - default = 14pts
        """
        axes.set_title(title, fontsize=title_text_size, color='k')
        axes.set_xlabel(x_label, fontsize=axis_text_size, color='k')
        axes.set_ylabel(y_label, fontsize=axis_text_size, color='k')
        if z_label is not None:
            axes.set_zlabel(z_label, fontsize=axis_text_size, color='k')

        # Configue & label axes
        if x_ticks is not None:
            axes.set_xlim([x_ticks[0], x_ticks[1]])  # NOQA
            axes.set_xticks(np.arange(x_ticks[0], x_ticks[1], x_ticks[2]).tolist())
        if y_ticks is not None:
            axes.set_ylim([y_ticks[0], y_ticks[1]])  # NOQA
            axes.set_yticks(np.arange(y_ticks[0], y_ticks[1], y_ticks[2]).tolist())
        if z_ticks is not None:
            axes.set_zlim([z_ticks[0], z_ticks[1]])  # NOQA
            axes.set_zticks(np.arange(z_ticks[0], z_ticks[1], z_ticks[2]).tolist())

        return

    @classmethod
    def ticks(cls,
              v: np.ndarray,
              given_ticks: Union[int, Tuple[float, float, float]]) -> Tuple[float, float, float]:
        """
        Create a tick range for a Matplotlib Axis
        :param v: The values to be plotted on the axis
        :param given_ticks: The ticks range to use or the number of ticks
        :return: If given_ticks is
            1. A Tuple, then just return given_ticks
            2. An Integer, a range of floor(min(v)) to ceil(max(v) with interval: max - min / given_ticks
            3. None, a range of floor(min(v)) to ceil(max(v) with interval: max - min / 10.0
        :raise ValueError: if given ticks is not Tuple, Integer or None
        """
        if given_ticks is None:
            given_ticks = 10

        if isinstance(given_ticks, Tuple):
            res = given_ticks
        elif isinstance(given_ticks, int):
            v_min = np.floor(np.min(v) * 10) / 10  # rounded down to 1 DP
            v_max = np.ceil(np.max(v) * 10) / 10  # rounded up to 1 DP
            res = (v_min, v_max, (v_max - v_min) / given_ticks)
        else:
            raise ValueError(
                f'Given ticks must be Tuple[float, float, float], int or None, but given {given_ticks.__class__.__name__}')
        return res
