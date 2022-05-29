from base.OrganismFactory import OrganismFactory
from typing import List
from base.Chromosome import Chromosome
from BasicOrganism import BasicOrganism


class BasicOrganismFactory(OrganismFactory):
    """
    Create basic Organisms
    """

    def new(self,
            chromosomes: List[Chromosome]) -> BasicOrganism:
        """
        Create a new basic organism from the given Chromosomes
        :param chromosomes: The Chromosomes to create the new organism with.
        :return: An Organism
        """
        return BasicOrganism(chromosomes=chromosomes)
