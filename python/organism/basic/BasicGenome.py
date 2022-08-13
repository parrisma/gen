from typing import Dict, List
from copy import copy
import numpy as np
from python.exceptions.NoSuchChromosomeInGenome import NoSuchChromosomeInGenome
from python.exceptions.NotAChromosome import NotAChromosome
from python.exceptions.GenomeMissMatch import GenomeMissMatch
from python.id.GenomeId import GenomeId
from python.base.Genome import Genome
from python.base.Chromosome import Chromosome
from python.organism.basic.BasicChromosome import BasicChromosome


class BasicGenome(Genome):
    """
    The Genome of a Basic Organism
    """

    _id: GenomeId
    _chromosomes: Dict[type, Chromosome]

    def __init__(self,
                 chromosomes: List[BasicChromosome] = None,
                 ):
        self._id = GenomeId()

        if chromosomes is None:
            chromosomes = [BasicChromosome()]

        self._chromosomes = dict()
        for chromosome in chromosomes:
            self._chromosomes[type(chromosome)] = chromosome
        return

    def get_genome_id(self) -> GenomeId:
        """
        Get the Genome unique identifier
        :return: An Genome UUID
        """
        return copy(self._id)  # ensure id is immutable

    def get_chromosome(self,
                       chromosome_type: type) -> Chromosome:
        """
        Get the chromosome of the given type
        :param chromosome_type: The type of Gene to get
        :return: The chromosome that matches the given type
        """
        if not isinstance(chromosome_type, type):
            raise ValueError(f'get_chromosome expects a type of chromosome to be passed')
        if chromosome_type not in self._chromosomes.keys():
            raise NoSuchChromosomeInGenome
        return self._chromosomes[chromosome_type]

    def set_chromosome(self,
                       chromosome: Chromosome) -> None:
        """
        Add or update the given chromosome within the Genome
        :param chromosome: The chromosome to add/update within the Genome
        """
        if not isinstance(chromosome, Chromosome):
            raise NotAChromosome(type(chromosome))
        self._chromosomes[type(chromosome)] = chromosome

    def get_chromosome_types(self) -> List[type]:
        """
        Get all the types for the Chromosome in the Genome
        :return: A list of Chromosome types
        """
        return list(self._chromosomes.keys())

    def get_diversity(self,
                      comparison_genome: 'BasicGenome') -> float:
        """
        Get the diversity of the Genome with respect to the given Genome
        :param comparison_genome: The Genome to calculate diversity with respect to.
        :return: The relative diversity
        """
        chromosomes_self = sorted(list(map(str, self.get_chromosome_types())))
        chromosomes_compare = sorted(list(map(str, comparison_genome.get_chromosome_types())))
        if chromosomes_self != chromosomes_compare:
            raise GenomeMissMatch

        diversities: List[float] = []
        chromosome: Chromosome
        for chromosome in self._chromosomes.values():
            diversities.append(chromosome.get_diversity(comparison_genome.get_chromosome(type(chromosome))))

        return np.array(diversities).mean(axis=-1)

    def __copy__(self):
        """
        Deep copy the Genome
        """
        copy_chromosomes: List[Chromosome] = []
        for chromosome in self._chromosomes.values():
            copy_chromosomes.append(copy(chromosome))
        return BasicGenome(copy_chromosomes)  # NOQA

    def __eq__(self, other):
        """
        Logical equality
        :param other: The other Genome to test equivalence with
        :return: True if this gene is logically equal to the 'other' given Genome
        """
        eq: bool = True
        if isinstance(other, BasicGenome):
            for chromosome_type in self.get_chromosome_types():
                if chromosome_type in other.get_chromosome_types():
                    if self.get_chromosome(chromosome_type) == other.get_chromosome(chromosome_type):
                        pass
                    else:
                        eq = False
                        break
                else:
                    eq = False
                    break
        else:
            eq = False
        return eq
