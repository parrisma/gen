from typing import Union, Callable, Tuple, List
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
from python.visualise.PlotUtil import PlotUtil


class ContourPlot:
    _2PI: float = 2 * np.pi

    def __init__(self,
                 title: str,
                 x_label: str,
                 y_label: str,
                 x: np.ndarray,
                 y: np.ndarray,
                 func: Callable[[float, float], float],
                 point: Tuple[float, float],
                 x_ticks: Union[int, Tuple[float, float, float]] = 10,
                 y_ticks: Union[int, Tuple[float, float, float]] = 10,
                 levels: Union[int, Tuple[float, float, float]] = 20):
        """
        Render a surface with contour lines given function
        :param title: The Title of the Graph
        :param x_label: The Label for the x-axis
        :param y_label: The Label for the y-axis
        :param x: The values of X to plot for (must have same length as Y)
        :param y: The values of Y to plot for (must have same length as X)
        :param func: The function of x,y to render
        :param x_ticks: X Axis ticks, (start, end, step) or the number of steps to auto-scale ticks to function
        :param y_ticks: Y Axis ticks, (start, end, step) or the number of steps to auto-scale ticks to function
        :param levels: The contour levels as a simple count (default 20) or as parameters for a stepped range
        """
        self._x_data: np.ndarray = x
        self._y_data: np.ndarray = y

        self._point: Tuple[float, float] = point
        self._plotted_point = None  # Point to Animate
        self._x_animation_data: np.ndarray = None
        self._y_animation_data: np.ndarray = None
        self._num_animation_points: int = None
        self._rotate_plot: bool = True
        self._rotate_step: int = 1

        self._func: Callable[[float, float], float] = func
        self._x, self._y, self._z = PlotUtil.render_function(x=x, y=y, func=self._func)

        # Plot solution surface
        self._fig, self._ax = plt.subplots(figsize=(7, 7))
        if isinstance(levels, int):
            lower = np.min(self._z)
            upper = np.max(self._z)
            interval = np.absolute(upper - lower) / levels
            self._levels = np.arange(lower, upper, interval).tolist()
        else:
            self._levels = np.arange(levels[0], levels[1], levels[2]).tolist()

        x_ticks = PlotUtil.ticks(v=self._x, given_ticks=x_ticks)
        y_ticks = PlotUtil.ticks(v=self._y, given_ticks=y_ticks)

        PlotUtil.axis_configuration(axes=self._ax,
                                    title=title,
                                    x_label=x_label, y_label=y_label,
                                    x_ticks=x_ticks, y_ticks=y_ticks)
        return

    def plot(self,
             show_point: bool = True) -> None:
        """
        Render a surface with contour lines given function
        :param show_point: Set to True to show the animated point
        """
        cp = self._ax.contourf(self._x, self._y, self._z, self._levels, cmap=cm.jet, antialiased=False)
        self._fig.colorbar(cp, aspect=20)

        if show_point:
            self._plotted_point, = self._ax.plot(self._point[0],  # x
                                                 self._point[1],  # y
                                                 marker="o", color="r")
        return

    def animation_function(self,
                           i):
        """
        Animate the plot
        :param i: The number of the frame animation & index into x,y animation data points
        :return:
        """
        if i > self._num_animation_points:
            raise ValueError(f' Animation frame index {i} is greater than number of animation points')

        x: float = self._x_animation_data[i]
        y: float = self._y_animation_data[i]
        z: float = self._func(x, y)
        self._plotted_point.set_data(x, y)
        return self._point,

    def animate(self,
                x_animation_data: np.ndarray,
                y_animation_data: np.ndarray,
                frame_interval: int = 30,
                show_time: int = 60):
        """
        Animate the plot.
        :param x_animation_data: The x points over which to animate the animated point
        :param y_animation_data: The z points over which to animate the animated point
        :param frame_interval: The interval between frame updates in milli-sec, default = 30 ms
        :param show_time: The number of seconds to show the animation for, default = 60 secs.
        :return:
        """
        if len(x_animation_data) != len(y_animation_data):
            raise ValueError("X and Y animation data points must have same length")

        self._x_animation_data = x_animation_data
        self._y_animation_data = y_animation_data
        self._num_animation_points = len(self._x_animation_data)

        _ = FuncAnimation(self._fig,
                          func=self,
                          frames=self._num_animation_points,
                          interval=frame_interval)
        plt.draw()
        plt.pause(show_time)
        return

    def __call__(self, i, *args, **kwargs):
        return self.animation_function(i)
