from typing import List
from python.organism.basic.BasicOrganismFactory import BasicOrganism
from python.base.Selector import Selector


class BasicSelector(Selector):
    def select_survivors(self,
                         population: List[BasicOrganism]) -> List[BasicOrganism]:
        """
        Select the population survivors given their relative fitness and diversity
        :return: A list of members that survived
        """
        raise NotImplementedError
