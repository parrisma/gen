import unittest
import numpy as np
from python.organism.basic.test.UtilsForTesting import UtilsForTesting
from python.visualise.SurfacePlot import SurfacePlot


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

    @classmethod
    def func(cls,
             x_val: float,
             y_val: float) -> float:
        return np.power(x_val, 2) + np.power(y_val, 2)

    @unittest.skip  # By default, these tests are skipped as they are blocking, remove skip to see result.
    @UtilsForTesting.test_case
    def testSurfacePlot(self):
        x = np.arange(-1.0, 1.0, 0.1)
        y = np.arange(-1.0, 1.0, 0.1)
        SurfacePlot.plot("Test Plot", x=x, y=y, func=TestSurfacePlot.func)

    @classmethod
    def fitness_func(cls,
                     x_val: float,
                     y_val: float) -> float:
        return np.power(np.absolute(-1 + x_val) / 2.0, 2) + (x_val * np.power((y_val / 24), 2))

    @UtilsForTesting.test_case
    def testSurfacePlotFitnessFunc(self):
        x = np.arange(-1.0, 1.1, 0.1)
        y = np.arange(0, 24.0 + (24 / 20), (24 / 20))
        SurfacePlot.plot_contour("Test Plot", x=x, y=y, func=TestSurfacePlot.fitness_func)
