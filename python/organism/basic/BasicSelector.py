from typing import List
from copy import copy
import numpy as np
from python.organism.basic.BasicOrganismFactory import BasicOrganism
from python.base.Selector import Selector


class BasicSelector(Selector):
    _selection_probability: float  # Probability of selection of the highest ranking organism

    def __init__(self,
                 selection_probability: float = 0.2):
        """
        Constructor.
        :param selection_probability: The probability of selection of the highest ranking organism

        Note: fitness_weight + diversity_weight are normalised to sum to 1.0 so are relative to each other
        """
        if selection_probability <= 0.0 or selection_probability >= 1.0:
            raise ValueError("Selection probability must be greater than zero and less than or equal to one")
        self._selection_probability = selection_probability

        return

    def select_survivors(self,
                         population: List[BasicOrganism]) -> List[BasicOrganism]:
        """
        Select the population survivors given their relative fitness and diversity

        Note: The last term of the survival probability (1 - Pc)^n-1 is ~ 10 times bigger than the
        previous last term as it not multiplied by the initial prob. This means the last item in the
        list is over selected. So we map this last prob to select a dummy null added to the population

        :return: A list of members that survived

        """
        probs = Selector.rank_selection_probabilities(initial_prob=self._selection_probability,
                                                      num=len(population) + 1)
        sorted_population = copy(population)
        sorted_population = sorted(sorted_population,
                                   key=lambda o: o.metrics().get_fitness() * .55 + o.metrics().get_diversity() * .45,
                                   reverse=True)
        sorted_population.append(None)
        survivors = np.random.choice(a=sorted_population, p=probs, size=len(population), replace=True)
        final_survivors = []
        for s in survivors:
            if s is not None:  # Ignore the dummy entry mapped to last selection probability
                if s not in final_survivors:
                    final_survivors.append(s)
        return final_survivors
