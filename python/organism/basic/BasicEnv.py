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
from python.organism.basic.BasicEnvironmentState import BasicEnvironmentState
from python.organism.basic.BasicSelector import BasicSelector
from python.organism.basic.BasicDynamicPointAnimation import BasicDynamicPointAnimation
from python.exceptions.PopulationExtinct import PopulationExtinct
from rltrace.Trace import Trace
from python.visualise.VisualisationAgentProxy import VisualisationAgentProxy
from python.organism.basic.BasicEnvVisualiserProxy import BasicEnvVisualiserProxy


class BasicEnv(Env):

    def __init__(self,
                 trace: Trace,
                 args,
                 selector: Selector,
                 organism_factory: OrganismFactory,
                 conf: Conf):
        """
        Simple environment constructor
        :param trace: The trace logger
        :param args: The parsed command line arguments (argparse)
        :param selector:  The selection (object) strategy to use for new generation selection
        :param organism_factory: The factory that can create new organisms
        :param conf: The JSON config file.
        """
        super(BasicEnv, self).__init__()
        self._trace = trace
        self._num_organisms: int = conf.config["environment"]["num_generation_zero_organisms"]
        self._crossover_rate: float = conf.config["environment"]["crossover_rate"]
        self._mutation_rate: float = conf.config["environment"]["mutation_rate"]
        self._mutation_step: float = conf.config["environment"]["mutation_step"]
        self._selection_probability: float = conf.config["environment"]["selection"]["primary_probability"]
        self._selection_fitness_weight: float = conf.config["environment"]["selection"]["fitness_weight"]
        self._hours_of_light_per_day: float = conf.config["environment"]["scenario"]["hours_of_light_per_day"]
        self._hours_since_last_rain: float = conf.config["environment"]["scenario"]["hours_since_last_rain"]
        self._population: Dict[str, Organism] = {}
        self._metrics: Dict[str, Metrics] = {}
        self._selector: Selector = selector
        self._organism_factory: OrganismFactory = organism_factory
        self._env_light_level: float = self._hours_of_light_per_day / 24.0
        self._env_drought_level: float = self._hours_since_last_rain / 24.0
        self._basic_env_visualiser_proxy = BasicEnvVisualiserProxy(hours_of_light_per_day=self._hours_of_light_per_day,
                                                                   hours_since_last_rain=self._hours_since_last_rain,
                                                                   num_organisms=self._num_organisms)
        self._visualisation_agent_proxy = \
            VisualisationAgentProxy(trace=self._trace,
                                    args=args,
                                    basic_visualiser_env_proxy=self._basic_env_visualiser_proxy)
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

    def create_generation_zero(self):
        """
        Create the initial generation zero population.
        """
        self._population.clear()
        for _ in range(self._num_organisms):
            o = self._organism_factory.new()
            self._population[o.get_id()] = o
            self._trace.log(f'{o.get_id()} Organism is born')

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
        try:
            with concurrent.futures.ProcessPoolExecutor(max_workers=50) as executor:
                # All Organisms must be pickalble before mutli-processing. This is because they are sent to the
                # spawned processes and get_state() also passes a list of organisms
                for o in self._population.values():
                    o.pickle_state_on()
                results = [executor.submit(partial(o.run, self.get_state())) for o in self._population.values()]  # NOQA
                for f in concurrent.futures.as_completed(results):
                    o: Organism = f.result()
                    self._trace.log(f'{o.get_id()} Organism has run')
                    if not o.is_alive():
                        self._population.pop(o.get_id())
                        self._trace.log(f'{o.get_id()} Organism has died & been removed from the population')
                    else:
                        o.pickle_state_off()
                        self._population[o.get_id()] = o
        except Exception as e:
            print(e)

        return

    def rank_and_select_survivors(self) -> None:
        """
        Based on the organisms' fitness & diversity , establish which of the current population should
        survive into the next generation
        """
        selector: BasicSelector = BasicSelector(selection_probability=self._selection_probability,
                                                fitness_weight=self._selection_fitness_weight)
        survivors = selector.select_survivors(list(self._population.values()))  # NOQA
        self._population = dict([(s.get_id(), s) for s in survivors])
        self._trace.log(f'{len(self._population)} survivors remain after rank and selection')
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
                                                       p=self._selector.rank_probabilities(num=len(self._population)),
                                                       replace=False)

            # Create new organism Genome
            genome: Genome = parents[0].crossover(organism=parents[1], mix_rate=self._crossover_rate)
            new_organism: Organism = self._organism_factory.new(genome=genome)
            new_organism.mutate(step_size=self._mutation_step)
            next_generation.append(new_organism)
            self._trace.log(f'new {new_organism.get_id()} from parents {parents[0].get_id()} & {parents[1].get_id()}')

        for organism in next_generation:
            self._population[organism.get_id()] = organism

        return

    def run(self) -> bool:
        """
        Run the evolutionary simulation until termination condition are met
        :return: False if the evolutionary simulation has met termination conditions.
        """
        self._visualisation_agent_proxy.initialise(num_organism=self._num_organisms,
                                                   env_light_level=self._env_light_level,
                                                   env_drought_level=self._env_drought_level)
        self.create_generation_zero()
        dpa = BasicDynamicPointAnimation(env_state=self.get_state)

        idx: int = 0
        while not self.termination_conditions_met():
            self.run_population()

            self._visualisation_agent_proxy.update(frame_index=idx,
                                                   frame_data=dpa.extract_points().tolist())
            fitness = []
            for o in self._population.values():
                fitness.append(o.metrics().get_fitness())
            p_min = np.min(fitness)
            p_max = np.max(fitness)
            p_avg = np.average(fitness)
            self._trace.log(
                f'min {p_min:+0.6f},  max {p_max:+0.6f},  average {p_avg:+0.6f}, num {len(self._population)}')
            self._trace.log(f'{fitness}')

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
