from typing import List, Union, Dict
from copy import copy
from abc import ABC, abstractmethod
import numpy as np
from python.id.GenomeId import GenomeId
from python.base.Chromosome import Chromosome
from python.base.Gene import Gene
from python.exceptions.NoSuchGeneInGenome import NoSuchGeneInGenome


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

    @classmethod
    def replace_gene(cls,
                     genome: 'Genome',
                     gene: Gene) -> None:
        """
        Replace the given Gene in the given Genome
        :param genome: The genome to replace the Gene in
        :param gene: The gene to overwrite the corresponding Gene in the Genome
        :raise NoSuchGeneInGenome: If the given gene does not exist in the Genome
        """
        replaced: bool = False
        for chromosome_type in genome.get_chromosome_types():
            chromosome = genome.get_chromosome(chromosome_type)
            for gene_type in chromosome.get_gene_types():
                if isinstance(gene, gene_type):
                    chromosome.set_gene(gene=gene)
                    replaced = True
                    break

        if not replaced:
            raise NoSuchGeneInGenome(f'Gene {gene.__class__} not present in Genome {genome.get_genome_id()}')
        return

    @classmethod
    def cross_genomes(cls,
                      mix_percent: float,
                      to_genome: 'Genome',
                      from_genome: 'Genome') -> 'Genome':
        """
        Swap mix_percent of randomly selected genes from_genome to_genome
        :param mix_percent: The percentage of genomes to randomly select to swap into target genome
        :param to_genome: The genome to swap genes into
        :param from_genome: The genome to select genes from
        :return: The Genome resulting from the crossover.
        """
        if mix_percent > 1.0 or mix_percent < 0.0:
            raise ValueError(f'mix_percent is a % and must be in range 0.0 to 1.0 - given {mix_percent}')

        target_genome = copy(to_genome)
        source_genes = Genome.gene_list(from_genome)
        target_genes = Genome.gene_list(target_genome)
        lcg = int(len(source_genes) * mix_percent)
        if lcg > 0:
            mix_genes = np.random.choice(source_genes, size=lcg, replace=False)
            for mix_gene in mix_genes:
                for target_gene in target_genes:
                    if isinstance(target_gene, type(mix_gene)):
                        Genome.replace_gene(genome=target_genome, gene=mix_gene)

        return target_genome

    @classmethod
    def mutate(cls,
               genome_to_mutate: 'Genome',
               step_size: Union[float, Dict[type, float]]) -> 'Genome':
        """
        Based on a defined <mutation_rate>. introduce random perturbation into the Organisms populations Genes
        :param genome_to_mutate: The genome to be mutated.
        :param step_size: An absolute step size as float to be applied to all gene types ot
        :return: The Genome resulting from the mutation.
        """
        mutated_genome = copy(genome_to_mutate)
        genes = Genome.gene_list(mutated_genome)
        for gene in genes:
            if isinstance(step_size, dict):
                if type(gene) in step_size.keys():
                    gene.mutate(step_size=step_size.get(type(gene)))
                else:
                    raise ValueError(f'No step size supplied for gene type {str(type(gene))}')
            else:
                gene.mutate(step_size=float(step_size))  # NOQA

        return mutated_genome
