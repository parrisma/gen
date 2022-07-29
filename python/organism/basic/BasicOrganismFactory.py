from python.base.OrganismFactory import OrganismFactory
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene
from python.organism.basic.BasicChromosome import BasicChromosome
from python.organism.basic.BasicGenome import BasicGenome
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
        return BasicOrganism(
            BasicGenome([BasicChromosome(drought_gene=DroughtToleranceGene(), light_gene=LightToleranceGene())]))
