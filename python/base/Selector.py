from typing import List
import numpy as np
from abc import ABC, abstractmethod
from python.base.Organism import Organism


class Selector(ABC):
    """
    The interface for rank selecting Organisms from a population.
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

    @abstractmethod
    def rank_probabilities(self,
                           num: int) -> List[float]:
        """
        The list of selection probabilities for rank selection of organisms ordered by fitness
        :param num: The number of organisms in the population
        :return: List of Probabilities
        """
        raise NotImplementedError

    @classmethod
    def _rank_prob(cls,
                   initial_prob: float,
                   position_in_list: int,
                   number_in_list) -> float:
        """
        Calculate the rank probability.
        :param initial_prob: The probability the highest rank is selected
        :param position_in_list: The position in the rank order being calculated for 0 to n - 1
        :param number_in_list: The number of items in the overall list being ranked n
        :return: The selection probability of the nth (position_in_list) item

        P1 = (1 - Pc)^0 * Pc
        P2 = (1 - Pc)^1 * Pc
        P3 = (1 - Pc)^2 * Pc
        ...
        Pn-1 = (1 - Pc)^n-2 * Pc
        Pn   = (1 - Pc)^n-1

        """
        if position_in_list == number_in_list - 1:
            selection_probability = np.power((1 - initial_prob), position_in_list)
        else:
            selection_probability = np.power((1 - initial_prob), position_in_list) * initial_prob
        return selection_probability

    @classmethod
    def rank_selection_probabilities(cls,
                                     initial_prob: float,
                                     num: int) -> List[float]:
        """
        Generate the rank based selection probabilities
        :param initial_prob: The probability the highest rank is selected
        :param num: The number of items in the overall list being ranked
        :return: A list of selection probabilities
        """
        probs = [Selector._rank_prob(initial_prob=initial_prob,
                                     position_in_list=n,
                                     number_in_list=num) for n in range(num)]
        # must sum to 1
        probs[-1] -= 1 - np.sum(probs)
        return probs
