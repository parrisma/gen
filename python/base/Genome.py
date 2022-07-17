from typing import List
from abc import ABC, abstractmethod
from python.id.GenomeId import GenomeId
from python.base.Chromosome import Chromosome


class Genome(ABC):
    """
    A the complete collection of Chromosomes that describe an Organism.
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
    def get_chromosome_types(self) -> List[str]:
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
