import sys
from typing import Union, Callable, Tuple, List, Dict
import matplotlib.lines
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
from python.visualise.FuncOfZInTermsOfXY import FuncOfZInTermsOfXY
from python.visualise.ParamScenarioFunc import ParamScenarioFunc
from python.visualise.PlotUtil import PlotUtil
from python.visualise.PointAnimationData import PointAnimationData


class ContourPlot:

    def __init__(self,
                 title: str,
                 x_label: str,
                 y_label: str,
                 x: np.ndarray,
                 y: np.ndarray,
                 func: FuncOfZInTermsOfXY,
                 func_params: Dict[str, ParamScenarioFunc],
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
        :param func_params: Optional parameters for function as a dictionary, passed as **kwargs to func
        :param points: The initial coordinates of the points that will be animated
        :param x_ticks: X Axis ticks, (start, end, step) or the number of steps to auto-scale ticks to function
        :param y_ticks: Y Axis ticks, (start, end, step) or the number of steps to auto-scale ticks to function
        :param levels: The contour levels as a simple count (default 20) or as parameters for a stepped range
        """
        self._x_data: np.ndarray = x
        self._y_data: np.ndarray = y

        self._points: List[Tuple[float, float]] = points
        self._plotted_points: List[matplotlib.lines.Line2D] = []  # Points to Animate
        self._show_points = False
        self._plot_animation_data: PointAnimationData = None  # NOQA
        self._num_animation_points: int = None  # NOQA
        self._colour_map = matplotlib.cm.get_cmap('jet')
        self._animation_point_cmap = matplotlib.cm.get_cmap('bwr')
        self._z_min = sys.float_info.max
        self._z_max = sys.float_info.min
        self._use_func_for_z = True

        self._func: FuncOfZInTermsOfXY = func

        self._func_params = {} if x is None else func_params
        for ky, vl in self._func_params.items():
            if not isinstance(vl, Callable):
                raise ValueError(f'Parameter scenarios must be callable matching protocol {ParamScenarioFunc.__name__}')

        self._title = title
        self._x_label = x_label
        self._y_label = y_label

        self._xm = None
        self._ym = None
        self._zm = None

        # Plot solution contour
        self._cp = None
        self._fig = None
        self._ax = None
        self._cbar = None

        # Define contour levels.
        self._levels = levels
        self._xm, self._ym, self._zm = PlotUtil.render_function(x=self._x_data, y=self._y_data,
                                                                scenario_index=0,
                                                                func=self._func, func_params=self._func_params)

        self._levels = self._set_levels(levels=levels,
                                        z_min=np.min(self._zm),
                                        z_max=np.max(self._zm))

        # Establish correct x, y ticks for each axis.
        self._x_ticks = PlotUtil.ticks(v=self._x_data, given_ticks=x_ticks)
        self._y_ticks = PlotUtil.ticks(v=self._y_data, given_ticks=y_ticks)

        return

    def _set_levels(self,
                    levels: Union[int, Tuple[float, float, float]],
                    z_min: float,
                    z_max: float,
                    min_levels: int = 10) -> List[float]:
        """
        Set the contour level
        :param levels: The contour levels as a simple count (default 20) or as parameters for a stepped range
        :param z_max: The maximum value of Z, and thus the contour range
        :param z_min: The minimum value of Z, and thus the contour range
        :param min_levels: The minimum number of allowable levels, default is 10
        :raises ValueError: if the defined levels not a positive int or a valid range, low,high,step
        :return: A list of the contour level steps, where there are at least min_levels levels defined.
        """

        resulting_levels: List[float] = None  # NOQA
        if isinstance(levels, int):
            if levels >= min_levels:
                interval = np.absolute(z_max - z_min) / self._levels
                resulting_levels = np.arange(z_min, z_max, interval).tolist()  # NOQA
        else:
            if isinstance(levels, Tuple):
                if len(levels) == 3:
                    if levels[0] > levels[1] and levels[1] - levels[0] > levels[2]:
                        resulting_levels = np.arange(self._levels[0], self._levels[1], self._levels[2]).tolist()  # NOQA
                        if len(resulting_levels) < min_levels:
                            resulting_levels = None  # NOQA

        if resulting_levels is None:
            raise ValueError("Contour levels must be specific as a single number n > 10 or range (start, stop, step")

        return resulting_levels

    def _init_plot(self) -> None:
        """
        Perform all one of plat configuration.
        """
        self._fig, self._ax = plt.subplots(figsize=(7, 7))

        PlotUtil.axis_configuration(axes=self._ax,
                                    title=self._title,
                                    x_label=self._x_label, y_label=self._y_label,
                                    x_ticks=self._x_ticks, y_ticks=self._y_ticks)

        return

    def _update_and_plot_contour(self,
                                 frame_index: int) -> None:
        """
        Calculate the plot Z values by calling plot function & update the contour plot
        :param frame_index: The index of the frame to update for.
        """
        self._xm, self._ym, self._zm = PlotUtil.render_function(x=self._x_data, y=self._y_data,
                                                                scenario_index=frame_index,
                                                                func=self._func, func_params=self._func_params)
        if self._cp is not None:
            for c in self._cp.collections:
                c.remove()
        self._cp = self._ax.contourf(self._xm, self._ym, self._zm,
                                     self._levels,
                                     cmap=self._colour_map, antialiased=False)
        if self._cbar is not None:
            self._cbar.remove()
        self._cbar = self._fig.colorbar(self._cp, aspect=20)

        return

    def _init_points(self,
                     show_points: bool) -> None:
        """
        Initialise the animated points
        :param show_points: Set to True to show the animated point
        """
        self._plotted_points = []
        if show_points:
            for point in self._points:
                plotted_pnt, = self._ax.plot(point[0],  # x
                                             point[1],  # y
                                             marker="o", color="r")
                self._plotted_points.append(plotted_pnt)
        return

    def _update_and_plot_points(self,
                                show_points: bool,
                                frame_index: int) -> None:
        """
        Update the animated points for the given frame index
        :param frame_index: The index of the frame to update for
        :param show_points: Set to True to show the animated point
        """
        if show_points:
            data_points_for_frame: np.ndarray = self._plot_animation_data.get_data_for_frame(frame_idx=frame_index)

            idx: int = 0
            for plotted_pnt in self._plotted_points:
                x: float = data_points_for_frame[idx][0]
                y: float = data_points_for_frame[idx][1]
                z: float = self._func(x, y, frame_index, **self._func_params)
                self._z_min = np.minimum(self._z_min, z)
                self._z_max = np.maximum(self._z_max, z)
                z = (z - self._z_min) / (self._z_max - self._z_min)

                plotted_pnt.set_data(x, y)
                plotted_pnt.set_color(self._animation_point_cmap(z))
                idx += 1
        return

    def plot(self,
             show_points: bool = True) -> None:
        """
        Render a surface with contour lines given function
        :param show_points: Set to True to show the animated point
        """
        self._init_plot()
        self._update_and_plot_contour(frame_index=0)
        self._show_points = show_points
        self._init_points(show_points=self._show_points)
        return

    def animation_function(self,
                           i) -> Tuple:
        """
        Animate the plot
        :param i: The number of the frame animation
        :return:
        """
        self._update_and_plot_contour(frame_index=i)
        self._update_and_plot_points(show_points=self._show_points, frame_index=i)
        return self._points,

    def animate(self,
                plot_animation_data: PointAnimationData,
                num_animation_frames: int,
                use_func_for_z: bool = True,
                frame_interval: int = 30,
                show_time: int = 60) -> None:
        """
        Animate the plot
        :param plot_animation_data: Class to supply animation data on demand frame by frame
        :param num_animation_frames: The number of discrete animation frames.
        :param use_func_for_z: If True use the supplied function to calculate z from x,y
        :param frame_interval: The interval between frame updates in milli-sec, default = 30 ms
        :param show_time: The number of seconds to show the animation for, default = 60 secs.
        """
        self._plot_animation_data = plot_animation_data
        self._num_animation_points = plot_animation_data.num_frames()

        # check shape is a 2d point
        self._use_func_for_z = use_func_for_z
        p_shape = self._plot_animation_data.frame_data_shape()
        if self._use_func_for_z and p_shape[0] != 2:
            raise ValueError(f'Animation expected x,y values, but shape was {str(p_shape)}')
        elif not self._use_func_for_z and p_shape[0] != 3:
            raise ValueError(f'Animation expected x,y,z values, but shape was {str(p_shape)}')

        _ = FuncAnimation(self._fig,
                          func=self,
                          frames=num_animation_frames,
                          interval=frame_interval)
        plt.draw()
        plt.pause(show_time)
        return

    def __call__(self,
                 frame_index: int,
                 *args, **kwargs):
        """
        Class is callable, where when called it invokes its animation.
        :param frame_index: The frame_index to pass to the animate function.
        :param args:
        :param kwargs:
        :return: The return result of the animate function
        """
        return self.animation_function(frame_index)
