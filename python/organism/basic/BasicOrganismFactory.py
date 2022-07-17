from typing import List
from python.base.OrganismFactory import OrganismFactory
from python.base.Chromosome import Chromosome
from python.organism.basic.BasicOrganism import BasicOrganism


class BasicOrganismFactory(OrganismFactory):
    """
    Create basic Organisms
    """

    def new(self,
            chromosomes: List[Chromosome]) -> BasicOrganism:
        """
        Create a new organism from the given Chromosomes
        :param chromosomes: The Chromosomes from which to create the organism
        :return: An Organism
        """
        return BasicOrganism(chromosomes)
