from typing import Dict
import concurrent.futures
from python.main.Conf import Conf
from python.base.Env import Env
from python.base.Organism import Organism
from python.organism.basic.BasicChromosome import BasicChromosome
from python.organism.basic.BasicOrganism import BasicOrganism
from python.organism.basic.BasicSelector import BasicSelector
from python.organism.basic.BasicOrganismFactory import BasicOrganismFactory


class SimpleEnv(Env):
    _num_gen_zero_organisms: int
    _mutation_rate: float
    _crossover_rate: float
    _population: Dict[str, BasicOrganism]
    _selector: BasicSelector
    _organism_factory: BasicOrganismFactory

    def __init__(self,
                 selector: BasicSelector,
                 organism_factory: BasicOrganismFactory,
                 conf: Conf):
        super(SimpleEnv, self).__init__()
        self._num_gen_zero_organisms = conf.config["environment"]["num_generation_zero_organisms"]
        self._crossover_rate = conf.config["environment"]["crossover_rate"]
        self._mutation_rate = conf.config["environment"]["mutation_rate"]
        self._population = {}
        self._metrics = {}
        self._selector = selector
        self._organism_factory = organism_factory
        return

    def create_generation_zero(self):
        """
        Create the initial generation zero population.
        """
        self._population.clear()
        for _ in range(self._num_gen_zero_organisms):
            o = self._organism_factory.new(chromosomes=BasicChromosome())
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
            results = [executor.submit(organism) for organism in self._population.values()]

            for f in concurrent.futures.as_completed(results):
                o: Organism = f.result()
                print(f'{o.get_id()} Organism has run')
                if not o.is_alive():
                    self._population.pop(o.get_id())
                    print(f'{o.get_id()} Organism has died & been removed from the population')
        return

    def rank_and_select_survivors(self) -> None:
        """
        Based on the organisms' fitness & diversity , establish which of the current population should
        survive into the next generation
        """
        
        # new_population: Dict[str, BasicOrganism] = {}
        # new_population = self._selector.select_survivors(population_fitness=self._fitness,
        #                                                 population_diversity=self._diversity,
        #                                                 population=list(self._population.values()))
        # self._population.clear()
        # self._population = new_population
        return

    def create_next_generation(self) -> None:
        """
        Create the next generation of Organisms
        """

        return

    def run(self) -> bool:
        """
        Run the evolutionary simulation until termination condition are met
        :return: False if the evolutionary simulation has met termination conditions.
        """
        self.create_generation_zero()

        while not self.termination_conditions_met():
            self.run_population()
            self.rank_and_select_survivors()
            self.create_next_generation()

        return False
