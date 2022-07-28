from typing import List
from abc import ABC, abstractmethod
from python.id.GenomeId import GenomeId
from python.base.Chromosome import Chromosome
from python.base.Gene import Gene


class Genome(ABC):
    """
    The complete collection of Chromosomes that describe an Organism.
    """

    @abstractmethod
    def get_genome_id(self) -> GenomeId:
        """
        Get the genome unique identifier
        :return: A genome globally unique id
        """
        raise NotImplementedError

    @abstractmethod
    def get_chromosome(self,
                       chromosome_type: type) -> Chromosome:
        """
        Get the chromosome of the given type
        :param chromosome_type: The type of the Gene within the Chromosome to get
        :return: The chromosome that matches the given type
        """
        raise NotImplementedError

    @abstractmethod
    def set_chromosome(self,
                       chromosome: Chromosome) -> None:
        """
        Add or update the given Chromosome within the Genome
        :param chromosome: The chromosome to add/update within the Genome
        """
        raise NotImplementedError

    @abstractmethod
    def get_chromosome_types(self) -> List[type]:
        """
        Get all the types for the chromosomes in the Genome
        :return: A list of Chromosome types
        """
        raise NotImplementedError

    @abstractmethod
    def get_diversity(self,
                      comparison_genome: 'Genome') -> float:
        """
        Get the diversity of the Genome with respect to the given Genome
        :param comparison_genome: The Genome to calculate diversity with respect to.
        :return: The relative diversity
        """
        raise NotImplementedError

    @abstractmethod
    def __copy__(self):
        """
        Deep copy the Genome
        """
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        """
        Logical equality
        :param other: The other Genome to test equivalence with
        :return: True if this gene is logically equal to the 'other' given Genome
        """
        raise NotImplementedError

    @classmethod
    def gene_list(cls,
                  genome: 'Genome') -> List[Gene]:
        """
        Extract a list of all Genes in the Genome.
        :param genome: The genome to extract Genes from
        :return: A list of all the genes in the Genome
        """
        genes: List[Gene] = []
        for chromosome_type in genome.get_chromosome_types():
            chromosome = genome.get_chromosome(chromosome_type)
            for gene_type in chromosome.get_gene_types():
                genes.append(chromosome.get_gene(gene_type))
        return genes
