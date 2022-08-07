import unittest
import numpy as np
from python.organism.basic.test.UtilsForTesting import UtilsForTesting
from python.visualise.SurfacePlot import SurfacePlot
from python.visualise.ContourPlot import ContourPlot
from python.visualise.PreCalcPlotAnimationDataForTesting import PreCalcPointPlotAnimationDataForTesting
from python.visualise.DynamicPlotAnimationDataForTesting import DynamicPointPlotAnimationDataForTesting
from python.visualise.PlotTestUtil import PlotTestUtil
from python.visualise.ParamScenario import ParamScenario


class TestSurfacePlot(unittest.TestCase):
    _run: int
    _LIGHT_TOLERANCE = "LightTolerance"
    _DROUGHT_TOLERANCE = "DroughtTolerance"

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
                           environment_light_level: float,
                           light_tolerance: float = None,
                           **kwargs) -> float:
        """
        Calculate fitness as a function of light tolerance and light level
        :param light_tolerance: The genetic driven light tolerance -1.0 to 1.0
        :param environment_light_level: The environment light level 0.0 to 1.0
        :return: The fitness of the organism given its light tolerance and the ambient light levels
        """
        if light_tolerance is None:
            light_tolerance = \
                kwargs.get(TestSurfacePlot._LIGHT_TOLERANCE, ParamScenario.single_value_scenario(0))(0)

        return 1 - np.sin(np.absolute((environment_light_level - ((1 + light_tolerance) / 2))) * (np.pi / 2))

    @classmethod
    def drought_fitness_func(cls,
                             environment_drought_level: float,
                             drought_tolerance: float = None,
                             **kwargs) -> float:
        """
        Calculate fitness as a function of drought tolerance and light level
        :param drought_tolerance: The genetic driven drought tolerance -1.0 to 1.0
        :param environment_drought_level: The environment drought level 0.0 to 1.0
        :return: The fitness of the organism given its drought tolerance and the drought level
        """
        if drought_tolerance is None:
            drought_tolerance = \
                kwargs.get(TestSurfacePlot._DROUGHT_TOLERANCE, ParamScenario.single_value_scenario(0))(0)
        return 1 - np.power(((1 + drought_tolerance) / 2 - environment_drought_level), 2)

    @classmethod
    def hybrid_fitness_func(cls,
                            environment_light_level: float,
                            environment_drought_level: float,
                            scenario_index: int,
                            **kwargs) -> float:

        # Extract optional (defaulted) arguments for the calculation.
        light_tol = \
            kwargs.get(TestSurfacePlot._LIGHT_TOLERANCE, ParamScenario.single_value_scenario(0))(scenario_index)
        drought_tol = \
            kwargs.get(TestSurfacePlot._DROUGHT_TOLERANCE, ParamScenario.single_value_scenario(0))(scenario_index)

        lf = TestSurfacePlot.light_fitness_func(light_tolerance=light_tol,
                                                environment_light_level=environment_light_level)
        df = TestSurfacePlot.drought_fitness_func(drought_tolerance=drought_tol,
                                                  environment_drought_level=environment_drought_level)
        return lf + df

    # @unittest.skip  # By default, these tests are skipped as they are blocking, remove skip to see result.
    @UtilsForTesting.test_case
    def testSurfacePlotFitnessFunc1(self):
        x = np.arange(0, 1.0, 0.025)
        y = np.arange(0, 1.0, 0.025)
        light_tol_scenario = ParamScenario(param_values_by_index=np.arange(-1.0, 1.0, 0.01))
        drought_tol_scenario = ParamScenario(param_values_by_index=np.arange(-1.0, 1.0, 0.01))
        surface_plot = SurfacePlot(title="Environmental Fitness",
                                   x_label="% of day in drought",
                                   y_label="% of day in light",
                                   z_label="Fitness",
                                   x=x,
                                   y=y,
                                   func=TestSurfacePlot.hybrid_fitness_func,
                                   func_params={
                                       TestSurfacePlot._LIGHT_TOLERANCE: light_tol_scenario.scenario_func,
                                       TestSurfacePlot._DROUGHT_TOLERANCE: drought_tol_scenario.scenario_func},
                                   point=(0.0, 0.0, 0.0),
                                   x_ticks=10,
                                   y_ticks=10,
                                   z_ticks=10)
        surface_plot.plot()
        if True:
            surface_plot.animate(DynamicPointPlotAnimationDataForTesting((-1.0, 1.0), (0.0, 1.0)), show_time=180)

    @unittest.skip  # By default, these tests are skipped as they are blocking, remove skip to see result.
    @UtilsForTesting.test_case
    def testSurfacePlotFitnessFunc(self):
        x = np.arange(0, 1.01, 0.0125)
        y = np.arange(0, 1.01, 0.0125)
        surface_plot = SurfacePlot(title="Environmental Fitness",
                                   x_label="% of day in drought",
                                   y_label="% of day in light",
                                   z_label="Fitness",
                                   x=x,
                                   y=y,
                                   func=TestSurfacePlot.hybrid_fitness_func,
                                   func_params={},
                                   point=(0.0, 0.0, 0.0),
                                   x_ticks=10,
                                   y_ticks=10,
                                   z_ticks=10)
        surface_plot.plot()
        if True:
            surface_plot.animate(DynamicPointPlotAnimationDataForTesting((-1.0, 1.0), (0.0, 1.0)), show_time=180)
        else:
            data = PlotTestUtil.generate_xy_range_animation_data(x_range=(-1.0, 1.0, 0.02),
                                                                 y_range=(0.0, 1.0, 0.01))
            surface_plot.animate(PreCalcPointPlotAnimationDataForTesting(data=data))
        return

    @unittest.skip  # By default, these tests are skipped as they are blocking, remove skip to see result.
    @UtilsForTesting.test_case
    def testContourPlotFitnessFunc(self):
        x = np.arange(0, 1.01, 0.0125)
        y = np.arange(0, 1.01, 0.0125)
        light_tol_scenario = ParamScenario(param_values_by_index=np.arange(-1.0, 1.0, 0.01))
        drought_tol_scenario = ParamScenario(param_values_by_index=np.arange(-1.0, 1.0, 0.01))
        num_animated_points = 6
        contour_plot = ContourPlot(title="Environmental Fitness",
                                   x_label="% of day in drought",
                                   y_label="% of day in light",
                                   x=x,
                                   y=y,
                                   func=TestSurfacePlot.hybrid_fitness_func,
                                   func_params={
                                       TestSurfacePlot._LIGHT_TOLERANCE: light_tol_scenario.scenario_func,
                                       TestSurfacePlot._DROUGHT_TOLERANCE: drought_tol_scenario.scenario_func},
                                   points=[(0.0, 0.0)] * num_animated_points,
                                   x_ticks=(0, 1.0, 0.1),
                                   y_ticks=(0, 1.0, 0.1),
                                   levels=100)
        contour_plot.plot()
        data = PlotTestUtil.generate_random_animation_data(100, num_animated_points, 2)
        contour_plot.animate(PreCalcPointPlotAnimationDataForTesting(data=data),
                             num_animation_frames=np.maximum(light_tol_scenario.num_scenario_steps,
                                                             drought_tol_scenario.num_scenario_steps),
                             show_time=180)
        return

#    func_params = {
#                      TestSurfacePlot._LIGHT_TOLERANCE: ParamScenario.single_value_scenario(.5),
#                      TestSurfacePlot._DROUGHT_TOLERANCE: ParamScenario.single_value_scenario(-.5)},
# light_tol_scenario = ParamScenario(param_values_by_index=np.array([0.5]))
# drought_tol_scenario = ParamScenario(param_values_by_index=np.array([-0.5]))
