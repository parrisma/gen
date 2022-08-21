from typing import Dict, List, Tuple
from functools import partial
import concurrent.futures
import time
import numpy as np
from python.main.Conf import Conf
from python.base.Env import Env
from python.base.Selector import Selector
from python.base.OrganismFactory import OrganismFactory
from python.base.Organism import Organism
from python.base.Genome import Genome
from python.base.Metrics import Metrics
from python.base.Gene import Gene
from python.organism.basic.BasicEnvironmentState import BasicEnvironmentState
from python.organism.basic.BasicSelector import BasicSelector
from python.organism.basic.BasicOrganism import BasicOrganism
from python.organism.basic.DynamicPointAnimation import DynamicPointAnimation
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from python.exceptions.PopulationExtinct import PopulationExtinct
from python.visualise.ParamScenario import ParamScenario
from python.visualise.SurfacePlot import SurfacePlot


class BasicEnv(Env):

    def __init__(self,
                 hours_of_light_per_day: float,
                 hours_since_last_rain: float,
                 selector: Selector,
                 organism_factory: OrganismFactory,
                 conf: Conf):
        """
        Simple environment constructor
        :param selector:  The selection (object) strategy to use for new generation selection
        :param organism_factory: The factory that can create new organisms
        :param conf: The JSON config file.
        """
        super(BasicEnv, self).__init__()
        self._num_organisms: int = conf.config["environment"]["num_generation_zero_organisms"]
        self._crossover_rate: float = conf.config["environment"]["crossover_rate"]
        self._mutation_rate: float = conf.config["environment"]["mutation_rate"]
        self._mutation_step: float = conf.config["environment"]["mutation_step"]
        self._population: Dict[str, Organism] = {}
        self._metrics: Dict[str, Metrics] = {}
        self._selector: Selector = selector
        self._organism_factory: OrganismFactory = organism_factory
        self._env_light_level: float = hours_of_light_per_day / 24.0
        self._env_drought_level: float = hours_since_last_rain / 24.0
        self._surface_plot = None
        return

    @classmethod
    def __as_pct(cls,
                 v: float,
                 lim: float):
        """
        Return the given value as a % where lim = 100%
        :param v: The value to be converted to %
        :param lim: The limit that represents 100%
        :return: The value as %
        """
        return np.maximum(0, np.minimum(np.absolute(v), lim)) / lim

    def __gene_space(self,
                     rng: Tuple[float, float],
                     env_level: float) -> float:
        """
        The given environment level expressed as a gene value.
        :param env_level: The environment level to be re-scaled
        :return: The re-scaled value as a Gene value
        """
        mn, mx = rng
        return (env_level * (mx - mn)) - mx

    def init_visualisation(self):

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
                                         points=[(0.0, 0.0, 0.0)] * self._num_organisms,
                                         x_ticks=10,
                                         y_ticks=10,
                                         z_ticks=10)
        self._surface_plot.plot()
        return

    def create_generation_zero(self):
        """
        Create the initial generation zero population.
        """
        self._population.clear()
        for _ in range(self._num_organisms):
            o = self._organism_factory.new()
            self._population[o.get_id()] = o
            print(f'{o.get_id()} Organism is born')

        return

    def termination_conditions_met(self) -> bool:
        """
        Evaluate the conditions that indicate the simulation has ended
        :return: True if the conditions to exit run have been met
        """
        return len(self._population) < 2

    def run_population(self) -> None:
        """
        Call the run method on each member of the population
        """
        self._metrics.clear()

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(partial(organism.run, self.get_state())) for organism in
                       self._population.values()]

            for f in concurrent.futures.as_completed(results):
                o: Organism = f.result()
                print(f'{o.get_id()} Organism has run')
                if not o.is_alive():
                    self._population.pop(o.get_id())
                    print(f'{o.get_id()} Organism has died & been removed from the population')
                else:
                    self._population[o.get_id()] = o
        return

    def rank_and_select_survivors(self) -> None:
        """
        Based on the organisms' fitness & diversity , establish which of the current population should
        survive into the next generation
        """
        survivors = BasicSelector(selection_probability=0.1).select_survivors(list(self._population.values()))  # NOQA
        self._population = dict([(s.get_id(), s) for s in survivors])
        return

    def create_next_generation(self) -> None:
        """
        Create the next generation of Organisms, by adding new organisms by random selection of 'parent' pairs
        from the residual population.
        """
        if len(self._population) < 2:
            raise PopulationExtinct('Less than 2 organisms remain, next generation not possible')

        next_generation: List[Organism] = list()

        while (len(self._population) + len(next_generation)) < self._num_organisms:
            # Select parents
            parents: List[Organism] = np.random.choice(a=np.array(list(self._population.values())),
                                                       size=2,
                                                       replace=False)

            # Create new organism Genome
            genome: Genome = parents[0].crossover(organism=parents[1], mix_rate=self._crossover_rate)
            new_organism: Organism = self._organism_factory.new(genome=genome)
            new_organism.mutate(step_size=self._mutation_step)
            next_generation.append(new_organism)

        for organism in next_generation:
            self._population[organism.get_id()] = organism

        return

    def run(self) -> bool:
        """
        Run the evolutionary simulation until termination condition are met
        :return: False if the evolutionary simulation has met termination conditions.
        """
        self.init_visualisation()
        self.create_generation_zero()
        dpa = DynamicPointAnimation(env_state=self.get_state)

        idx: int = 0
        while not self.termination_conditions_met():
            self.run_population()

            self._surface_plot.animate_step(frame_index=idx,
                                            plot_animation_data=dpa,
                                            points_only=True)
            fitness = [o.fitness() for o in self._population.values()]
            print(f'{fitness}')
            p_min = np.min(fitness)
            p_max = np.max(fitness)
            p_avg = np.average(fitness)
            print(f'min {p_min:0.5f},  max {p_max:0.5f},  average {p_avg:0.5f}, num {len(self._population)}')

            self.rank_and_select_survivors()
            self.create_next_generation()
            time.sleep(0)  # yield

        return False

    def get_state(self) -> BasicEnvironmentState:
        """
        Get the current state of the Environment
        :return: The current environment state
        """
        return BasicEnvironmentState(avg_hours_of_light_per_day=self._env_light_level,
                                     avg_hours_between_rain=self._env_drought_level,
                                     population=list(self._population.values()))
