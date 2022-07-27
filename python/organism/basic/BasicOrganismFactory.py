from python.base.OrganismFactory import OrganismFactory
from python.organism.basic.BasicOrganism import BasicOrganism


class BasicOrganismFactory(OrganismFactory):
    """
    Create basic Organisms
    """

    def new(self) -> BasicOrganism:
        """
        Create a new organism from the given Chromosomes
        :return: An Organism
        """
        return BasicOrganism()
