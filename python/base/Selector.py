from typing import List
from abc import ABC, abstractmethod
from python.base.Organism import Organism


class Selector(ABC):
    """
    The interface for selecting Organisms from a population.
    """

    @abstractmethod
    def select_survivors(self,
                         population: List[Organism]) -> List[Organism]:
        """
        Select the population survivors
        :param population: the current population
        :return: A List of the members that survived
        """
        raise NotImplementedError
