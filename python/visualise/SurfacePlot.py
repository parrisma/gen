from typing import Union, Callable, Tuple, Protocol, Dict, Any
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
from python.visualise.FuncOfZInTermsOfXY import FuncOfZInTermsOfXY
from python.visualise.ParamScenarioFunc import ParamScenarioFunc
from python.visualise.PointAnimationData import PointAnimationData
from python.visualise.PlotUtil import PlotUtil


class SurfacePlot:
    _2PI: float = 2 * np.pi

    def __init__(self,
                 title: str,
                 x_label: str,
                 y_label: str,
                 z_label: str,
                 x: np.ndarray,
                 y: np.ndarray,
                 func: FuncOfZInTermsOfXY,
                 func_params: Dict[str, ParamScenarioFunc],
                 point: Tuple[float, float, float],
                 x_ticks: Union[int, Tuple[float, float, float]] = 10,
                 y_ticks: Union[int, Tuple[float, float, float]] = 10,
                 z_ticks: Union[int, Tuple[float, float, float]] = 10,
                 elevation: float = 30,
                 azimuth: float = 35,
                 distance: float = 9,
                 transparency: float = 0.5):
        """
        Render a surface with contour lines given function
        :param title: The Title of the Graph
        :param x_label: The Label for the x-axis
        :param y_label: The Label for the y-axis
        :param z_label: The Label for the z-axis
        :param x: The values of X to plot for (must have same length as Y)
        :param y: The values of Y to plot for (must have same length as X)
        :param func: The function of x,y to render
        :param func_params: Optional parameters for function as a dictionary, passed as **kwargs to func
        :param point: A points to overlay onto the contour
        :param x_ticks: X Axis ticks, (start, end, step) or the number of steps to auto-scale ticks to function
        :param y_ticks: Y Axis ticks, (start, end, step) or the number of steps to auto-scale ticks to function
        :param z_ticks: Z Axis ticks, (start, end, step) or the number of steps to auto-scale ticks to function
        :param elevation: The 3D viewing elevation, default = 30 degrees
        :param azimuth: The 3D viewing azimuth, default = 35 degrees (0 to 360)
        :param distance: The 3D viewing distance, default = 9, bigger => further away, adjust to fit plot optimally
        :param transparency: surface transparency, 1.0 = Fully Opaque, default = 0.5
        """
        self._x_data: np.ndarray = x
        self._y_data: np.ndarray = y
        self._elevation: float = elevation
        self._azimuth: float = azimuth
        self._transparency: float = transparency
        self._distance: float = distance

        self._point: Tuple[float, float, float] = point
        self._plotted_point = None  # Point to Animate
        self._plot_animation_data = None
        self._num_animation_points: int = None
        self._show_points = False
        self._show_surface_contours = True
        self._show_2d_contour = True

        self._rotate_plot: bool = True
        self._rotate_step: int = 1

        self._colour_map = cm.get_cmap('jet')
        self._animation_point_cmap = cm.get_cmap('bwr')
        self._2d_contour_cmap = cm.get_cmap('binary')

        self._func: FuncOfZInTermsOfXY = func
        self._func_params = {} if x is None else func_params
        for ky, vl in self._func_params.items():
            if not isinstance(vl, Callable):
                raise ValueError(f'Parameter scenarios must be callable matching protocol {ParamScenarioFunc.__name__}')

        self._title = title
        self._x_label = x_label
        self._y_label = y_label
        self._z_label = z_label

        self._cp = None
        self._fig = None
        self._ax = None
        self._surface = None
        self._cbar = None
        self._surface_contours = None
        self._2d_contours = None

        self._xm = None
        self._ym = None
        self._zm = None

        self._xm, self._ym, self._zm = PlotUtil.render_function(x=self._x_data, y=self._y_data,
                                                                func=self._func, func_params=self._func_params)

        self._x_ticks = PlotUtil.ticks(v=self._xm, given_ticks=x_ticks)
        self._y_ticks = PlotUtil.ticks(v=self._ym, given_ticks=y_ticks)
        self._z_ticks = PlotUtil.ticks(v=self._zm, given_ticks=z_ticks)

        return

    def _init_plot(self) -> None:
        """
        Perform all one of plat configuration.
        """
        # Plot solution surface
        self._fig = plt.figure(figsize=(7, 7))
        self._ax = self._fig.gca(projection="3d")
        self._ax.view_init(elev=self._elevation,
                           azim=self._azimuth)  # 3D Viewing position
        self._ax.dist = self._distance  # Zoom out, so we can see all the axes and labels.

        PlotUtil.axis_configuration(axes=self._ax,
                                    title=self._title,
                                    x_label=self._x_label, y_label=self._y_label, z_label=self._z_label,
                                    x_ticks=self._x_ticks, y_ticks=self._y_ticks, z_ticks=self._z_ticks)
        return

    def _updated_and_plot_contours(self,
                                   frame_index: int) -> None:
        """
        Calculate the plot Z values by calling plot function & update the contour plot
        :param frame_index: The index of the frame to update for.
        """
        return

    def _init_points(self,
                     show_points: bool) -> None:
        """
        Initialise the animated points
        :param show_points: Set to True to show the animated point
        """
        if show_points:
            self._plotted_point, = self._ax.plot(self._point[0],  # x
                                                 self._point[1],  # y
                                                 self._point[2],  # z
                                                 marker="o", color="r")
        return

    def _update_and_plot_points(self,
                                show_points: bool,
                                frame_index: int) -> None:
        """
        Update the animated points for teh given frame index
        :param frame_index: The index of the frame to update for
        :param show_points: Set to True to show the animated point
        """
        if show_points:
            data_points_for_frame: np.ndarray = self._plot_animation_data.get_data_for_frame(frame_idx=frame_index)
            x: float = data_points_for_frame[0][0]
            y: float = data_points_for_frame[0][1]
            z: float = self._func(x, y, frame_index, **self._func_params)

            self._plotted_point.set_data(x, y)
            self._plotted_point.set_3d_properties(z)
        return

    def _update_and_plot_surface(self,
                                 frame_index: int) -> None:

        self._xm, self._ym, self._zm = PlotUtil.render_function(x=self._x_data, y=self._y_data,
                                                                scenario_index=frame_index,
                                                                func=self._func, func_params=self._func_params)

        if self._surface is not None:
            self._surface.remove()
        self._surface = self._ax.plot_surface(self._xm, self._ym, self._zm,
                                              cmap=self._colour_map,
                                              linewidth=0,
                                              antialiased=False,
                                              rcount=200,
                                              ccount=200,
                                              alpha=self._transparency)

        # if self._cbar is not None:
        #    self._cbar.remove()
        # self._cbar = self._fig.colorbar(self._surface, shrink=0.5, aspect=20)

        if self._surface_contours is not None:
            for c in self._surface_contours.collections:
                c.remove()
        if self._show_surface_contours:
            self._surface_contours = self._ax.contour(self._xm, self._ym, self._zm,
                                                      levels=20,
                                                      colors='grey', linestyles="dashed", linewidths=.5,
                                                      antialiased=False)

        if self._2d_contours is not None:
            for c in self._2d_contours.collections:
                c.remove()
        if self._show_2d_contour:
            self._2d_contours = self._ax.contourf(self._xm, self._ym, self._zm,
                                                  levels=20,
                                                  cmap=self._2d_contour_cmap,
                                                  alpha=self._transparency,
                                                  antialiased=False,
                                                  offset=self._z_ticks[0])

        return

    def plot(self,
             show_points: bool = True,
             show_surface_contours: bool = True,
             show_2d_contour: bool = True) -> None:
        """
        Render a surface with contour lines given function
        :param show_points: Set to True to show the animated point
        :param show_surface_contours: Set True to show the contour lines superimposed on teh surface plot
        :param show_2d_contour:  Set True to show the 2d contour plot directly under the surface
        """
        self._init_plot()

        self._show_points = show_points
        self._init_points(show_points=show_points)

        self._show_surface_contours = show_surface_contours
        self._show_2d_contour = show_2d_contour

        self._update_and_plot_surface(frame_index=0)

        return

    def animation_function(self,
                           frame_index):
        """
        Animate the plot
        :param frame_index: The number of the frame animation & index into x,y animation data points
        :return:
        """
        self._update_and_plot_points(show_points=self._show_points, frame_index=frame_index)
        self._update_and_plot_surface(frame_index=frame_index)

        # if self._rotate_plot:
        #    self._azimuth = (self._azimuth + self._rotate_step) % 360
        #    self._ax.view_init(elev=self._elevation,
        #                       azim=self._azimuth)  # 3D Viewing position
        #    return self._fig,
        # else:
        #    return self._point,
        return self._point,

    def animate(self,
                plot_animation_data: PointAnimationData,
                frame_interval: int = 30,
                show_time: int = 60,
                rotate_plot: bool = True,
                rotate_step: int = 1):
        """
        Animate the plot.
        :param plot_animation_data: Class to supply animation data on demand frame by frame
        :param frame_interval: The interval between frame updates in milli-sec, default = 30 ms
        :param show_time: The number of seconds to show the animation for, default = 60 secs.
        :param rotate_plot: If True rotate the plot during the animation
        :param rotate_step: The numbers of degrees to rotate the plot by for each animation update
        :return:
        """
        self._plot_animation_data = plot_animation_data
        self._num_animation_points = plot_animation_data.num_points()

        self._rotate_plot = rotate_plot
        self._rotate_step = rotate_step

        p_shape = self._plot_animation_data.point_shape()
        if p_shape[0] != 2:
            raise ValueError(f'Animation expected x,y values, but shape was {str(p_shape)}')

        _ = FuncAnimation(self._fig,
                          func=self,
                          frames=self._num_animation_points,
                          interval=frame_interval)
        plt.draw()
        plt.pause(show_time)
        return

    def __call__(self, i, *args, **kwargs):
        return self.animation_function(i)
