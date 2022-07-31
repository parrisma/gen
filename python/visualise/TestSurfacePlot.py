import unittest
import numpy as np
from python.organism.basic.test.UtilsForTesting import UtilsForTesting
from python.visualise.SurfacePlot import SurfacePlot
from python.visualise.ContourPlot import ContourPlot
from python.visualise.PreCalcPlotAnimationDataForTesting import PreCalcPointPlotAnimationDataForTesting
from python.visualise.DynamicPlotAnimationDataForTesting import DynamicPointPlotAnimationDataForTesting
from python.visualise.PlotTestUtil import PlotTestUtil


class TestSurfacePlot(unittest.TestCase):
    _run: int

    def __init__(self, *args, **kwargs):
        super(TestSurfacePlot, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        return

    def setUp(self) -> None:
        TestSurfacePlot._run += 1
        print(f'- - - - - - C A S E {TestSurfacePlot._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        print(f'- - - - - - C A S E {TestSurfacePlot._run} Passed - - - - - -\n')
        return

    def test1(self):
        print("Done test 1")
        return

    @classmethod
    def light_fitness_func(cls,
                           x_val: float,
                           y_val: float) -> float:
        return np.power(np.absolute(-1 + x_val) / 2.0, 2) + (x_val * np.power((y_val), 2))

    # @unittest.skip  # By default, these tests are skipped as they are blocking, remove skip to see result.
    @UtilsForTesting.test_case
    def testSurfacePlotFitnessFunc(self):
        x = np.arange(-1.0, 1.0 + .1, 0.05)
        y = np.arange(0, 1.0 + .05, 0.025)
        surface_plot = SurfacePlot(title="Fitness function for light tolerance",
                                   x_label="Light Tolerance",
                                   y_label="% of day in the Light",
                                   z_label="Fitness",
                                   x=x,
                                   y=y,
                                   func=TestSurfacePlot.light_fitness_func,
                                   point=(0.0, 0.0, 0.0),
                                   x_ticks=10,
                                   y_ticks=10,
                                   z_ticks=10)
        surface_plot.plot()
        if True:
            surface_plot.animate(DynamicPointPlotAnimationDataForTesting((-1.0, 1.0), (0.0, 1.0)))
        else:
            data = PlotTestUtil.generate_xy_range_animation_data(x_range=(-1.0, 1.0, 0.02),
                                                                 y_range=(0.0, 1.0, 0.01))
            surface_plot.animate(PreCalcPointPlotAnimationDataForTesting(data=data))
        return

    @unittest.skip  # By default, these tests are skipped as they are blocking, remove skip to see result.
    @UtilsForTesting.test_case
    def testContourPlotFitnessFunc(self):
        x = np.arange(-1.0, 1.0 + .1, 0.05)
        y = np.arange(0, 1.0 + .05, 0.025)
        num_animated_points = 6
        contour_plot = ContourPlot(title="Fitness function for light tolerance",
                                   x_label="Light Tolerance",
                                   y_label="% of day in the Light",
                                   x=x,
                                   y=y,
                                   func=TestSurfacePlot.light_fitness_func,
                                   points=[(0.0, 0.0)] * num_animated_points,
                                   x_ticks=(-1.0, 1.0, 0.25),
                                   y_ticks=(0, 1, .1),
                                   levels=50)
        contour_plot.plot()
        data = PlotTestUtil.generate_random_animation_data(100, num_animated_points, 2)
        contour_plot.animate(PreCalcPointPlotAnimationDataForTesting(data=data))
