from typing import List
import numpy as np

from python.organism.basic.BasicOrganismFactory import BasicOrganism
from python.base.Selector import Selector


class BasicSelector(Selector):
    _selection_probability: float  # Probability of selection of the highest ranking organism
    _fitness_weight: float  # The contribution of fitness to rank
    _diversity_weight: float  # The contribution of diversity to rank

    def __init__(self,
                 selection_probability: float = 0.2,
                 fitness_weight: float = 0.5,
                 diversity_weight: float = 0.5):
        """
        Constructor.
        :param selection_probability: The probability of selection of the highest ranking organism
        :param fitness_weight:  The contribution of fitness to rank
        :param diversity_weight: The contribution of diversity to rank

        Note: fitness_weight + diversity_weight are normalised to sum to 1.0 so are relative to each other
        """
        self._selection_probability = selection_probability

        normalisation_factor: float = fitness_weight + diversity_weight
        self._fitness_weight = fitness_weight / normalisation_factor
        self._diversity_weight = diversity_weight / normalisation_factor
        return

    def select_survivors(self,
                         population: List[BasicOrganism]) -> List[BasicOrganism]:
        """
        Select the population survivors given their relative fitness and diversity

        P1 = (1 - Pc)^0 * Pc
        P2 = (1 - Pc)^1 * Pc
        P3 = (1 - Pc)^2 * Pc
        ...
        Pn-1 = (1 - Pc)^n-2 * Pc
        Pn   = (1 - Pc)^n-1

        :return: A list of members that survived
        """
        n = np.arange(1, 10)
        x = np.array(map(lambda x: x * 2, n))
        raise NotImplementedError
