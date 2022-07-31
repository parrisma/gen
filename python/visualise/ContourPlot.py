import sys
from typing import Union, Callable, Tuple, List
import matplotlib.lines
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
from python.visualise.PlotUtil import PlotUtil
from python.visualise.PlotAnimationData import PlotAnimationData


class ContourPlot:
    _2PI: float = 2 * np.pi

    def __init__(self,
                 title: str,
                 x_label: str,
                 y_label: str,
                 x: np.ndarray,
                 y: np.ndarray,
                 func: Callable[[float, float], float],
                 points: List[Tuple[float, float]],
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
        :param points: The initial coordinates of the points that will be animated
        :param x_ticks: X Axis ticks, (start, end, step) or the number of steps to auto-scale ticks to function
        :param y_ticks: Y Axis ticks, (start, end, step) or the number of steps to auto-scale ticks to function
        :param levels: The contour levels as a simple count (default 20) or as parameters for a stepped range
        """
        self._x_data: np.ndarray = x
        self._y_data: np.ndarray = y

        self._points: List[Tuple[float, float]] = points
        self._plotted_points: List[matplotlib.lines.Line2D] = []  # Points to Animate
        self._plot_animation_data: PlotAnimationData = None
        self._num_animation_points: int = None
        self._animation_point_cmap = matplotlib.cm.get_cmap('brg')
        self._z_min = sys.float_info.max
        self._z_max = sys.float_info.min

        self._func: Callable[[float, float], float] = func
        self._x, self._y, self._z = PlotUtil.render_function(x=x, y=y, func=self._func)

        # Plot solution contour
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
            for point in self._points:
                plotted_pnt, = self._ax.plot(point[0],  # x
                                             point[1],  # y
                                             marker="o", color="r")
                self._plotted_points.append(plotted_pnt)
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

        data_points_for_frame: np.ndarray = self._plot_animation_data.get_data_for_frame(frame_idx=i)

        idx: int = 0
        for plotted_pnt in self._plotted_points:
            x: float = data_points_for_frame[idx][0]
            y: float = data_points_for_frame[idx][1]
            z: float = self._func(x, y)
            self._z_min = np.minimum(self._z_min, z)
            self._z_max = np.maximum(self._z_max, z)
            z = (z - self._z_min) / (self._z_max - self._z_min)

            plotted_pnt.set_data(x, y)
            plotted_pnt.set_color(self._animation_point_cmap(z))
            idx += 1
        return self._points,

    def animate(self,
                plot_animation_data: PlotAnimationData,
                frame_interval: int = 30,
                show_time: int = 60):
        """
        Animate the plot.
        :param plot_animation_data: Class to supply animation data on demand frame by frame
        :param frame_interval: The interval between frame updates in milli-sec, default = 30 ms
        :param show_time: The number of seconds to show the animation for, default = 60 secs.
        :return:
        """
        self._plot_animation_data = plot_animation_data
        self._num_animation_points = plot_animation_data.num_points()

        # check shape is a 2d point

        _ = FuncAnimation(self._fig,
                          func=self,
                          frames=self._plot_animation_data.num_points(),
                          interval=frame_interval)
        plt.draw()
        plt.pause(show_time)
        return

    def __call__(self, i, *args, **kwargs):
        return self.animation_function(i)
