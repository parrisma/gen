from typing import Dict
from copy import deepcopy
from exceptions.NoSuchGeneIdInChromosome import NoSuchGeneIdInChromosome
from id.ChromosomeId import ChromosomeId
from id.GeneId import GeneId
from base.Chromosome import Chromosome
from base.Gene import Gene


class BasicChromosome(Chromosome):
    _id: ChromosomeId
    _genes: Dict[str, Gene]

    def __init__(self):
        self._id = ChromosomeId()
        return

    """
    A means to hold the data required to evaluate the relative fitness of organisms
    """

    def get_chromosome_id(self) -> ChromosomeId:
        """
        Get the chromosome unique identifier
        :return: An chromosome UUID
        """
        return deepcopy(self._id)  # ensure id is immutable

    def get_gene(self,
                 gene_id: GeneId) -> Gene:
        """
        Get the gene of the given id
        :return: The gene that matches the given id
        """
        if str(gene_id) not in self._genes.keys():
            raise NoSuchGeneIdInChromosome
        return self._genes[str(gene_id)]

    def get_diversity(self,
                      comparison_chromosome: 'Chromosome') -> float:
        """
        Get the diversity of the Chromosome with respect to the given Chromosome
        :param comparison_chromosome: The Chromosome to calculate diversity with respect to.
        :return: The relative diversity
        """
        raise NotImplementedError
