from typing import List
from abc import ABC, abstractmethod
from python.id.ChromosomeId import ChromosomeId
from python.base.Gene import Gene


class Chromosome(ABC):
    """
    A related collection of Genes
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
                 gene_type: type) -> Gene:
        """
        Get the gene of the given type
        :param gene_type: The type of the Gene within the Chromosome to get
        :return: The gene that matches the given type
        """
        raise NotImplementedError

    @abstractmethod
    def set_gene(self,
                 gene: Gene) -> None:
        """
        Add or update the given gene within the Chromosome
        :param gene: The Gene to add/update within the Chromosome
        """
        raise NotImplementedError

    @abstractmethod
    def get_gene_types(self) -> List[type]:
        """
        Get all the types for the Genes in the Chromosome (as returned by Gene.type())
        :return: A list of Gene types
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

    @abstractmethod
    def __copy__(self):
        """
        Deep copy the Chromosome
        """
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        """
        Logical equality
        :param other: The other Chromosome to test equivalence with
        :return: True if this gene is logically equal to the 'other' given Chromosome
        """
        raise NotImplementedError
