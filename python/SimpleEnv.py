from typing import Dict, List
import concurrent.futures
import numpy as np
from Conf import Conf
from python.base.Env import Env
from python.base.Fitness import Fitness
from python.base.Diversity import Diversity
from python.base.Chromosome import Chromosome
from python.organism.basic.BasicMetrics import BasicMetrics
from python.organism.basic.BasicOrganism import BasicOrganism
from python.organism.basic.BasicSelector import BasicSelector
from python.organism.basic.BasicOrganismFactory import BasicOrganismFactory


class SimpleEnv(Env):
    _num_gen_zero_organisms: int
    _mutation_rate: float
    _crossover_rate: float
    _population: Dict[str, BasicOrganism]
    _metrics: Dict[str, BasicMetrics]
    _fitness: Dict[str, Fitness]
    _diversity: Dict[str, Diversity]
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
            o = self._organism_factory.new()
            self._population[o.get_id()] = o
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
                res: BasicMetrics = f.result()
                if not res.is_alive():
                    self._population.pop(res.get_metrics_id())
                else:
                    self._metrics[res.get_metrics_id()] = res
        return

    def evaluate_fitness(self) -> None:
        """
        Evaluate the fitness of the current population.
        """
        self._fitness.clear()
        for metric in self._metrics.values():
            fitness = Fitness(metric)
            self._fitness[fitness.get_fitness_id()] = fitness
        return

    def evaluate_diversity(self) -> None:
        """
        Evaluate the diversity of the current population with respect to itself.
        """
        self._diversity.clear()

        organism: BasicOrganism
        for organism in self._population:
            self._diversity[organism.get_id()] = organism.get_diversity(list(self._population.values()))

        raise NotImplementedError

    def rank_and_select_survivors(self) -> None:
        """
        Based on the organisms' fitness & diversity , establish which of the current population should
        survive into the next generation
        """
        new_population: Dict[str, BasicOrganism] = {}
        new_population = self._selector.select_survivors(population_fitness=self._fitness,
                                                         population_diversity=self._diversity,
                                                         population=list(self._population.values()))
        self._population.clear()
        self._population = new_population
        return

    def crossover(self) -> List[List[Chromosome]]:
        """
        Based on a defined <crossover_rate>, cross genes between the pair of given Organisms designated as
        'mating'
        :return: The List of Chromosomes from which to form the next generation
        """
        crossover_chromosomes: List[List[Chromosome]] = []
        random_index = np.random.choice(range((len(self._population) % 2) * 2), size=1, replace=False)
        organism_id = list(self._population.keys())
        a: BasicOrganism
        b: BasicOrganism
        for a_idx, b_idx in random_index:
            a = self._population[organism_id[a_idx]]
            b = self._population[organism_id[b_idx]]
            if np.random.rand() > self._crossover_rate:
                crossover_chromosomes.append(a.crossover(mix_rate=self._crossover_rate,
                                                         organism=b))
            return crossover_chromosomes

    def mutate(self,
               next_generation_chromosomes: List[List[Chromosome]]) -> List[List[Chromosome]]:
        """
        Based on a defined <mutation_rate>. introduce random perturbation into the Organisms populations Genes
        :param next_generation_chromosomes: The candidate chromosomes of the next generation to under-go mutation
        :return: The List of Chromosomes from which to form the next generation
        """
        chromosomes: List[Chromosome]
        for chromosomes in next_generation_chromosomes:
            chromosome: Chromosome
            for chromosome in chromosomes:
                if np.random.rand() > self._crossover_rate:
                    gene_id_to_mutate = np.random.choice(chromosome.get_gene_types())
                    chromosome.get_gene(gene_id_to_mutate).mutate()

        return next_generation_chromosomes

    def create_next_generation(self,
                               next_generation_chromosomes: List[List[Chromosome]]) -> None:
        """
        Create the next generation of Organisms
        :param next_generation_chromosomes: The candidate chromosomes of the next generation
        """
        chromosomes: List[Chromosome]
        for chromosomes in next_generation_chromosomes:
            o = self._organism_factory.new()
            self._population[o.get_id()] = o
        return

    def run(self) -> bool:
        """
        Run the evolutionary simulation until termination condition are met
        :return: False if the evolutionary simulation has met termination conditions.
        """
        self.create_generation_zero()

        while not self.termination_conditions_met():
            self.run_population()
            self.evaluate_fitness()
            self.rank_and_select_survivors()
            self.create_next_generation(self.mutate(self.crossover()))

        return False
