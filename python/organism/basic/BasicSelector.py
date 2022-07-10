from typing import List, Dict
from python.base.Fitness import Fitness
from python.base.Diversity import Diversity
from python.organism.basic.BasicOrganismFactory import BasicOrganism
from python.base.Selector import Selector


class BasicSelector(Selector):
    def select_survivors(self,
                         population_fitness: Dict[str, Fitness],
                         population_diversity: Dict[str, Diversity],
                         population: List[BasicOrganism]) -> Dict[str, BasicOrganism]:
        """
        Select the population survivors given their relative fitness and diversity
        :param population_fitness: A dictionary of the population fitness
        :param population_diversity: A dictionary of the population diversity
        :param population: the population
        :return: A Dictionary of Organisms keyed by organism is of the population members that survived
        """
        raise NotImplementedError
