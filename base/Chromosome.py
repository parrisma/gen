from typing import List
from abc import ABC, abstractmethod
from id.ChromosomeId import ChromosomeId
from id.GeneId import GeneId
from base.Gene import Gene


class Chromosome(ABC):
    """
    A means to hold the data required to evaluate the relative fitness of organisms
    """

    @abstractmethod
    def get_chromosome_id(self) -> ChromosomeId:
        """
        Get the chromosome unique identifier
        :return: An chromosome globally unique id
        """
        raise NotImplementedError

    @abstractmethod
    def get_gene(self,
                 gene_id: GeneId) -> Gene:
        """
        Get the gene of the given id
        :return: The gene that matches the given id
        """
        raise NotImplementedError

    @abstractmethod
    def get_gene_ids(self) -> List[GeneId]:
        """
        Get all the id's for the Genes in the Chromosome
        :return: A list of GeneId's
        """
        raise NotImplementedError

    @abstractmethod
    def get_diversity(self,
                      comparison_chromosome: 'Chromosome') -> float:
        """
        Get the diversity of the Chromosome with respect to the given Chromosome
        :param comparison_chromosome: The Chromosome to calculate diversity with respect to.
        :return: The relative diversity
        """
        raise NotImplementedError
