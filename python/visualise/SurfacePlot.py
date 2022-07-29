from typing import List, Callable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


class SurfacePlot:
    @classmethod
    def plot_surf(cls,
                  title: str,
                  x: np.ndarray,
                  y: np.ndarray,
                  func: Callable[[float, float], float]):
        nx = len(x)
        ny = len(y)

        xx = np.zeros((nx, ny), dtype='d')
        yy = np.zeros((nx, ny), dtype='d')
        zz = np.zeros((nx, ny), dtype='d')

        # populate x,y,z arrays
        for i in range(nx):
            for j in range(ny):
                xx[i, j] = x[i]
                yy[i, j] = y[j]
                zz[i, j] = func(x[i], y[j])

        # convert arrays to vectors
        _x = xx.flatten()
        _y = yy.flatten()
        _z = zz.flatten()

        # Plot solution surface
        fig = plt.figure(figsize=(6, 6))
        ax = Axes3D(fig)
        ax.plot_trisurf(_x, _y, _z, cmap=cm.jet, linewidth=0, antialiased=False)
        ax.set_title(title, fontsize=16, color='k')
        ax.view_init(60, 35)
        fig.tight_layout()
        plt.show()
        return

    @classmethod
    def plot_contour(cls,
                     title: str,
                     x: np.ndarray,
                     y: np.ndarray,
                     func: Callable[[float, float], float]):
        nx = len(x)
        ny = len(y)

        _x, _y = np.meshgrid(x, y)
        _z = np.zeros((nx, ny), dtype='d')

        # populate x,y,z arrays
        for i in range(nx):
            for j in range(ny):
                _z[i, j] = func(x[i], y[j])

        # Plot solution surface
        fig, ax = plt.subplots()
        levels = np.arange(-0.25, 1, .025).tolist()
        cp = ax.contourf(_x, _y, _z, levels, cmap=cm.terrain, antialiased=False)
        fig.colorbar(cp)
        ax.set_title(title, fontsize=16, color='k')
        ax.set_xlim([-1, 1])
        ax.set_xticks(x)
        ax.set_ylim([0, 24])
        ax.set_yticks(y)
        fig.tight_layout()
        plt.show()
        return
