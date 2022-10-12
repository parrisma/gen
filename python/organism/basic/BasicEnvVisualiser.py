import numpy as np
import threading
from typing import Tuple
from python.interface.Visualiser import Visualiser
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from python.visualise.ParamScenario import ParamScenario
from python.visualise.SurfacePlot import SurfacePlot
from python.organism.basic.BasicOrganism import BasicOrganism


class BasicEnvVisualiser(Visualiser):

    def __init__(self):
        self._num_organism: int = None  # NOQA
        self._surface_plot: SurfacePlot = None  # NOQA
        self._env_light_level: float = None  # NOQA
        self._env_drought_level: float = None  # NOQA
        self._yield_secs = 0.25
        return

    @staticmethod
    def __gene_space(rng: Tuple[float, float],
                     env_level: float) -> float:
        """
        The given environment level expressed as a gene value.
        :param env_level: The environment level to be re-scaled
        :return: The re-scaled value as a Gene value
        """
        mn, mx = rng
        return (env_level * (mx - mn)) - mx

    def initialise(self,
                   **kwargs) -> None:
        """
        Initialise the view
        """

        self._env_light_level: float = kwargs['env_light_level']
        self._env_drought_level: float = kwargs['env_light_level']
        self._num_organism: int = kwargs['num_organism']

        x = np.arange(0, 1.01, 0.025)  # Light level as % in range 0.0 to 1.0
        y = np.arange(0, 1.01, 0.025)  # Drought level as % in range 0.0 to 1.0

        # Single value scenarios as we fix the surface to show the optimal fitness function for
        # the configured light/drought levels. The organism will have the highest fitness when its
        # genes express a suitability that matches exactly the prevailing light/drought level.

        ell = self.__gene_space(rng=LightToleranceGene.value_range(), env_level=self._env_light_level)
        light_tol_scenario = ParamScenario(scenario_name="Light Tol",
                                           param_values_by_index=np.array(ell).reshape(1))

        dll = self.__gene_space(rng=DroughtToleranceGene.value_range(), env_level=self._env_drought_level)
        drought_tol_scenario = ParamScenario(scenario_name="Drought Tol",
                                             param_values_by_index=np.array(dll).reshape(1))

        self._surface_plot = SurfacePlot(title="Environmental Fitness",
                                         x_label="% of day in drought",
                                         y_label="% of day in light",
                                         z_label="Fitness",
                                         x=x,
                                         y=y,
                                         func=BasicOrganism.hybrid_fitness_func,
                                         func_params={
                                             BasicOrganism.LIGHT_TOLERANCE: light_tol_scenario,
                                             BasicOrganism.DROUGHT_TOLERANCE: drought_tol_scenario},
                                         points=[(0.0, 0.0, 0.0)] * self._num_organism,
                                         x_ticks=10,
                                         y_ticks=10,
                                         z_ticks=10)
        self._surface_plot.plot()
        return

    def update(self,
               **kwargs) -> None:
        """
        Update the view
        """
        pass

    def terminate(self,
                  **kwargs) -> None:
        """
        Tear down the view and release any resources
        """
        pass

    def show(self,
             **kwargs) -> None:
        """
        Show the current plot.
        """
        if self._surface_plot is not None:
            self._surface_plot.show_updates()
