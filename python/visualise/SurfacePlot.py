from typing import Union, Callable, Tuple, List
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
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
                 func: Callable[[float, float], float],
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
        :param points: A list of points to overlay onto the contour
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
        self._x_animation_data: np.ndarray = None
        self._y_animation_data: np.ndarray = None
        self._num_animation_points: int = None
        self._rotate_plot: bool = True
        self._rotate_step: int = 1

        self._func: Callable[[float, float], float] = func
        self._x, self._y, self._z = PlotUtil.render_function(x=x, y=y, func=self._func)

        # Plot solution surface
        self._fig = plt.figure(figsize=(7, 7))
        self._ax = self._fig.gca(projection="3d")
        self._ax.view_init(elev=self._elevation,
                           azim=self._azimuth)  # 3D Viewing position
        self._ax.dist = self._distance  # Zoom out, so we can see all the axes and labels.

        x_ticks = PlotUtil.ticks(v=self._x, given_ticks=x_ticks)
        y_ticks = PlotUtil.ticks(v=self._y, given_ticks=y_ticks)
        z_ticks = PlotUtil.ticks(v=self._z, given_ticks=z_ticks)

        PlotUtil.axis_configuration(axes=self._ax,
                                    title=title,
                                    x_label=x_label, y_label=y_label, z_label=z_label,
                                    x_ticks=x_ticks, y_ticks=y_ticks, z_ticks=z_ticks)
        return

    def plot(self,
             show_point: bool = True,
             show_surface_contours: bool = True,
             show_2d_contour: bool = True) -> None:
        """
        Render a surface with contour lines given function
        :param show_point: Set to True to show the animated point
        :param show_surface_contours: Set True to show the contour lines superimposed on teh surface plot
        :param show_2d_contour:  Set True to show the 2d contour plot directly under the surface
        """
        surface = self._ax.plot_surface(self._x, self._y, self._z,
                                        cmap=cm.jet,
                                        linewidth=0,
                                        antialiased=False,
                                        rcount=200,
                                        ccount=200,
                                        alpha=self._transparency)
        self._fig.colorbar(surface, shrink=0.5, aspect=20)

        if show_surface_contours:
            self._ax.contour(self._x, self._y, self._z,
                             levels=20,
                             colors='grey', linestyles="dashed", linewidths=.5,
                             antialiased=False)

        if show_2d_contour:
            self._ax.contourf(self._x, self._y, self._z,
                              levels=20,
                              cmap=cm.binary,
                              alpha=self._transparency,
                              antialiased=False, offset=0)

        if show_point:
            self._plotted_point, = self._ax.plot(self._point[0],  # x
                                                 self._point[1],  # y
                                                 self._point[2],  # z
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
        self._plotted_point.set_3d_properties(z)

        if self._rotate_plot:
            self._azimuth = (self._azimuth + self._rotate_step) % 360
            self._ax.view_init(elev=self._elevation,
                               azim=self._azimuth)  # 3D Viewing position
            return self._fig,
        else:
            return self._point,

    def animate(self,
                x_animation_data: np.ndarray,
                y_animation_data: np.ndarray,
                frame_interval: int = 30,
                show_time: int = 60,
                rotate_plot: bool = True,
                rotate_step: int = 1):
        """
        Animate the plot.
        :param x_animation_data: The x points over which to animate the animated point
        :param y_animation_data: The z points over which to animate the animated point
        :param frame_interval: The interval between frame updates in milli-sec, default = 30 ms
        :param show_time: The number of seconds to show the animation for, default = 60 secs.
        :param rotate_plot: If True rotate the plot during the animation
        :param rotate_step: The numbers of degrees to rotate the plot by for each animation update
        :return:
        """
        if len(x_animation_data) != len(y_animation_data):
            raise ValueError("X and Y animation data points must have same length")

        self._x_animation_data = x_animation_data
        self._y_animation_data = y_animation_data
        self._num_animation_points = len(self._x_animation_data)

        self._rotate_plot = rotate_plot
        self._rotate_step = rotate_step

        _ = FuncAnimation(self._fig,
                          func=self,
                          frames=self._num_animation_points,
                          interval=frame_interval)
        plt.draw()
        plt.pause(show_time)
        return

    def __call__(self, i, *args, **kwargs):
        return self.animation_function(i)
