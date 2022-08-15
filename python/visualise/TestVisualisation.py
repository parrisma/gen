import unittest
import numpy as np
import time
from python.organism.basic.test.UtilsForTesting import UtilsForTesting
from python.visualise.SurfacePlot import SurfacePlot
from python.visualise.ContourPlot import ContourPlot
from python.visualise.PreCalcPlotAnimationDataForTesting import PreCalcPointPlotAnimationDataForTesting
from python.visualise.DynamicPlotAnimationDataForTesting import DynamicPointPlotAnimationDataForTesting
from python.visualise.DynamicPlot3DAnimationDataForTesting import DynamicPointPlot3DAnimationDataForTesting
from python.visualise.PlotTestUtil import PlotTestUtil
from python.visualise.ParamScenario import ParamScenario


class TestVisualisation(unittest.TestCase):
    _run: int
    _LIGHT_TOLERANCE = "LightTolerance"
    _DROUGHT_TOLERANCE = "DroughtTolerance"

    def __init__(self, *args, **kwargs):
        super(TestVisualisation, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        return

    def setUp(self) -> None:
        TestVisualisation._run += 1
        print(f'- - - - - - C A S E {TestVisualisation._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        print(f'- - - - - - C A S E {TestVisualisation._run} Passed - - - - - -\n')
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
                kwargs.get(TestVisualisation._LIGHT_TOLERANCE,
                           ParamScenario(param_values_by_index=np.array([0]), scenario_name='default'))(0)

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
                kwargs.get(TestVisualisation._DROUGHT_TOLERANCE,
                           ParamScenario(param_values_by_index=np.array([0]), scenario_name='default'))(0)
        return 1 - np.power(((1 + drought_tolerance) / 2 - environment_drought_level), 2)

    @classmethod
    def hybrid_fitness_func(cls,
                            environment_light_level: float,
                            environment_drought_level: float,
                            scenario_index: int,
                            **kwargs) -> float:

        # Extract optional (defaulted) arguments for the calculation.
        light_tol = \
            kwargs.get(TestVisualisation._LIGHT_TOLERANCE,
                       ParamScenario(param_values_by_index=np.array([0]), scenario_name='default'))(scenario_index)
        drought_tol = \
            kwargs.get(TestVisualisation._DROUGHT_TOLERANCE,
                       ParamScenario(param_values_by_index=np.array([0]), scenario_name='default'))(scenario_index)

        lf = TestVisualisation.light_fitness_func(light_tolerance=light_tol,
                                                  environment_light_level=environment_light_level)
        df = TestVisualisation.drought_fitness_func(drought_tolerance=drought_tol,
                                                    environment_drought_level=environment_drought_level)
        return lf + df

    # @unittest.skip  # By default, these tests are skipped as they are blocking, remove skip to see result.
    @UtilsForTesting.test_case
    def testSurfacePlotStepByStepUpdate(self):

        x = np.arange(0, 1.01, 0.025)
        y = np.arange(0, 1.01, 0.025)

        light_tol_scenario = ParamScenario(scenario_name="Light Tol",
                                           param_values_by_index=np.array(0.3).reshape(1))
        drought_tol_scenario = ParamScenario(scenario_name="Drought Tol",
                                             param_values_by_index=np.array(-.5).reshape(1))

        num_animated_points = 20

        surface_plot = SurfacePlot(title="Environmental Fitness",
                                   x_label="% of day in drought",
                                   y_label="% of day in light",
                                   z_label="Fitness",
                                   x=x,
                                   y=y,
                                   func=TestVisualisation.hybrid_fitness_func,
                                   func_params={
                                       TestVisualisation._LIGHT_TOLERANCE: light_tol_scenario,
                                       TestVisualisation._DROUGHT_TOLERANCE: drought_tol_scenario},
                                   points=[(0.0, 0.0, 0.0)] * num_animated_points,
                                   x_ticks=10,
                                   y_ticks=10,
                                   z_ticks=10)
        surface_plot.plot()
        d3dp = DynamicPointPlot3DAnimationDataForTesting(num_points=num_animated_points,
                                                         x_range=(0, 1),
                                                         y_range=(0, 1),
                                                         func=TestVisualisation.hybrid_fitness_func,
                                                         func_params={
                                                             TestVisualisation._LIGHT_TOLERANCE: light_tol_scenario,
                                                             TestVisualisation._DROUGHT_TOLERANCE: drought_tol_scenario}
                                                         )
        for i in range(100):
            surface_plot.animate_step(frame_index=i,
                                      plot_animation_data=d3dp,
                                      points_only=True)
        return

    @unittest.skip  # By default, these tests are skipped as they are blocking, remove skip to see result.
    @UtilsForTesting.test_case
    def testSurfacePlotAnimatedWithParamScenario(self):

        x = np.arange(0, 1.01, 0.025)
        y = np.arange(0, 1.01, 0.025)

        light_tol_scenario = ParamScenario(scenario_name="Light Tol",
                                           param_values_by_index=np.arange(-1.0, 1.0, 0.01))
        drought_tol_scenario = ParamScenario(scenario_name="Drought Tol",
                                             param_values_by_index=np.arange(-1.0, 1.0, 0.01))

        num_animated_points = 20

        surface_plot = SurfacePlot(title="Environmental Fitness",
                                   x_label="% of day in drought",
                                   y_label="% of day in light",
                                   z_label="Fitness",
                                   x=x,
                                   y=y,
                                   func=TestVisualisation.hybrid_fitness_func,
                                   func_params={
                                       TestVisualisation._LIGHT_TOLERANCE: light_tol_scenario,
                                       TestVisualisation._DROUGHT_TOLERANCE: drought_tol_scenario},
                                   points=[(0.0, 0.0, 0.0)] * num_animated_points,
                                   x_ticks=10,
                                   y_ticks=10,
                                   z_ticks=10)
        surface_plot.plot()
        d3dp = DynamicPointPlot3DAnimationDataForTesting(num_points=num_animated_points,
                                                         x_range=(0, 1),
                                                         y_range=(0, 1))
        surface_plot.animate(d3dp, show_time=180, rotate_plot=False)
        return

    @unittest.skip  # By default, these tests are skipped as they are blocking, remove skip to see result.
    @UtilsForTesting.test_case
    def testSurfacePlotAnimatedSinglePoint(self):
        x = np.arange(0, 1.01, 0.0125)
        y = np.arange(0, 1.01, 0.0125)
        surface_plot = SurfacePlot(title="Environmental Fitness",
                                   x_label="% of day in drought",
                                   y_label="% of day in light",
                                   z_label="Fitness",
                                   x=x,
                                   y=y,
                                   func=TestVisualisation.hybrid_fitness_func,
                                   func_params={},
                                   points=[(0.0, 0.0, 0.0)],
                                   x_ticks=10,
                                   y_ticks=10,
                                   z_ticks=10)
        surface_plot.plot()
        surface_plot.animate(DynamicPointPlotAnimationDataForTesting((-1.0, 1.0), (0.0, 1.0)),
                             show_time=180,
                             rotate_plot=False)
        return

    @unittest.skip  # By default, these tests are skipped as they are blocking, remove skip to see result.
    @UtilsForTesting.test_case
    def testContourPlotAnimatedPoints(self):
        x = np.arange(0, 1.01, 0.0125)
        y = np.arange(0, 1.01, 0.0125)

        light_tol_scenario = ParamScenario(scenario_name="Light Tol",
                                           param_values_by_index=np.arange(-1.0, 1.0, 0.01))
        drought_tol_scenario = ParamScenario(scenario_name="Drought Tol",
                                             param_values_by_index=np.arange(-1.0, 1.0, 0.01))
        num_animated_points = 6

        contour_plot = ContourPlot(title="Environmental Fitness",
                                   x_label="% of day in drought",
                                   y_label="% of day in light",
                                   x=x,
                                   y=y,
                                   func=TestVisualisation.hybrid_fitness_func,
                                   func_params={
                                       TestVisualisation._LIGHT_TOLERANCE: light_tol_scenario,
                                       TestVisualisation._DROUGHT_TOLERANCE: drought_tol_scenario},
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
