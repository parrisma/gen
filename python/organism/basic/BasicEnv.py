from typing import Dict, List
from functools import partial
import concurrent.futures
import numpy as np
from python.main.Conf import Conf
from python.base.Env import Env
from python.base.Selector import Selector
from python.base.OrganismFactory import OrganismFactory
from python.base.Organism import Organism
from python.base.Genome import Genome
from python.organism.basic.BasicEnvironmentState import BasicEnvironmentState
from python.organism.basic.BasicSelector import BasicSelector
from python.exceptions.PopulationExtinct import PopulationExtinct


class BasicEnv(Env):
    _num_organisms: int
    _mutation_rate: float
    _crossover_rate: float
    _population: Dict[str, Organism]
    _selector: Selector
    _organism_factory: OrganismFactory
    _state: BasicEnvironmentState

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
        self._num_organisms = conf.config["environment"]["num_generation_zero_organisms"]
        self._crossover_rate = conf.config["environment"]["crossover_rate"]
        self._mutation_rate = conf.config["environment"]["mutation_rate"]
        self._population = {}
        self._metrics = {}
        self._selector = selector
        self._organism_factory = organism_factory
        self._state = BasicEnvironmentState(avg_hours_of_light_per_day=hours_of_light_per_day,
                                            avg_hours_between_rain=hours_since_last_rain,
                                            population=list(self._population.values()))
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
        return len(self._population) == 0

    def run_population(self) -> None:
        """
        Call the run method on each member of the population
        """
        self._metrics.clear()

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(partial(organism.run, self._state)) for organism in self._population.values()]

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
        survivors = BasicSelector(selection_probability=0.2).select_survivors(list(self._population.values()))  # NOQA
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
            new_organism.mutate(step_size=0.001)
            next_generation.append(new_organism)

        for organism in next_generation:
            self._population[organism.get_id()] = organism

        return

    def run(self) -> bool:
        """
        Run the evolutionary simulation until termination condition are met
        :return: False if the evolutionary simulation has met termination conditions.
        """
        self.create_generation_zero()

        while not self.termination_conditions_met():
            self.run_population()

            fitness = [o.fitness() for o in self._population.values()]
            p_min = np.min(fitness)
            p_max = np.max(fitness)
            p_avg = np.average(fitness)
            print(f'min {p_min:0.5f}  max {p_max:0.5f}  average {p_avg:0.5f}')

            self.rank_and_select_survivors()
            self.create_next_generation()

        return False

    def get_state(self) -> BasicEnvironmentState:
        """
        Get the current state of the Environment
        :return: The current environment state
        """
        raise NotImplementedError
