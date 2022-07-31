import unittest
import numpy as np
from python.organism.basic.test.UtilsForTesting import UtilsForTesting
from python.visualise.SurfacePlot import SurfacePlot
from python.visualise.ContourPlot import ContourPlot
from python.visualise.PreCalcPlotAnimationDataForTesting import PreCalcPointPlotAnimationDataForTesting


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

    @unittest.skip  # By default, these tests are skipped as they are blocking, remove skip to see result.
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
        surface_plot.animate(x_animation_data=np.arange(-1.0, 1.0, 0.02),
                             y_animation_data=np.arange(0.0, 1.0, 0.01))
        return

    # @unittest.skip  # By default, these tests are skipped as they are blocking, remove skip to see result.
    @UtilsForTesting.test_case
    def testContourPlotFitnessFunc(self):
        x = np.arange(-1.0, 1.0 + .1, 0.05)
        y = np.arange(0, 1.0 + .05, 0.025)
        contour_plot = ContourPlot(title="Fitness function for light tolerance",
                                   x_label="Light Tolerance",
                                   y_label="% of day in the Light",
                                   x=x,
                                   y=y,
                                   func=TestSurfacePlot.light_fitness_func,
                                   points=[(0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)],
                                   x_ticks=(-1.0, 1.0, 0.25),
                                   y_ticks=(0, 1, .1),
                                   levels=50)
        contour_plot.plot()

        data = np.zeros((100, 6, 2))
        for i in range(100):
            for j in range(6):
                if i == 0:
                    data[i][j][0], data[i][j][1] = np.random.random(2)
                else:
                    s = 1
                    if np.random.rand() > 0.5:
                        s = -1
                    data[i][j][0] = (data[i - 1][j][0] + (np.random.rand() * .07 * s)) % 1
                    data[i][j][1] = (data[i - 1][j][1] + (np.random.rand() * .07 * s)) % 1

        contour_plot.animate(PreCalcPointPlotAnimationDataForTesting(data=data))
