from typing import List
from abc import ABC, abstractmethod
from base.Fitness import Fitness
from base.Diversity import Diversity
from base.Chromosome import Chromosome


class Env(ABC):
    """
    The environment in which evolution occurs.
    """

    @abstractmethod
    def create_generation_zero(self):
        """
        Create the initial generation zero population.
        :return: A List of Organisms
        """
        raise NotImplementedError

    @abstractmethod
    def termination_conditions_met(self) -> bool:
        """
        Evaluate the conditions that will indicate when the simulation has ended
        :return: True if the conditions to exit run have been met
        """
        raise NotImplementedError

    @abstractmethod
    def run_population(self) -> None:
        """
        Iterate over the population and call the run method on each
        """
        raise NotImplementedError

    @abstractmethod
    def evaluate_fitness(self) -> Fitness:
        """
        Evaluate the fitness of the current population.
        """
        raise NotImplementedError

    @abstractmethod
    def evaluate_diversity(self) -> Diversity:
        """
        Evaluate the diversity of the current population with respect to itself.
        """
        raise NotImplementedError

    @abstractmethod
    def select_next_generation(self) -> None:
        """
        Based on the current fitness metrics, establish which of the current population should
        survive into the next generation
        """
        raise NotImplementedError

    @abstractmethod
    def crossover(self) -> List[List[Chromosome]]:
        """
        Based on a defined <crossover_rate>, cross genes between the pair of given Organisms designated as
        'mating'
        """
        raise NotImplementedError

    @abstractmethod
    def mutate(self,
               next_generation_chromosomes: List[List[Chromosome]]) -> List[List[Chromosome]]:
        """
        Based on a defined <mutation_rate>. introduce random perturbation into the Organisms populations Genes
        """
        raise NotImplementedError

    @abstractmethod
    def create_next_generation(self,
                               next_generation_chromosomes: List[List[Chromosome]]) -> None:
        """
        Create the next generation of Organisms
        """
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        """
        Run the evolutionary simulation until termination condition are met
        """
        raise NotImplementedError
