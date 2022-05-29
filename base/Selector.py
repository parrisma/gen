from typing import List, Dict
from abc import ABC, abstractmethod
from base.Fitness import Fitness
from base.Diversity import Diversity
from base.Organism import Organism


class Selector(ABC):
    """
    The interface for selecting Organisms from a population.
    """

    @abstractmethod
    def select_survivers(self,
                         population_fitness: Dict[str, Fitness],
                         population_diversity: Dict[str, Diversity],
                         population: List[Organism]) -> Dict[str, Organism]:
        """
        Select the population survivers given their relative fitness and diversity
        :param population_fitness: A dictionary of the population fitness
        :param population_diversity: A dictionary of the population diversity
        :param population: the population
        :return: A Dictionary of Organisms keyed by organism is of the population members that survived
        """
        raise NotImplementedError
