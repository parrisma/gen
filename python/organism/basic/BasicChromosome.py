from typing import Dict, List
from copy import copy, deepcopy
import numpy as np
from python.exceptions.NoSuchGeneTypeInChromosome import NoSuchGeneTypeInChromosome
from python.exceptions.ChromosomeMissMatch import ChromosomeMissMatch
from python.exceptions.NotAGene import NotAGene
from python.id.ChromosomeId import ChromosomeId
from python.base.Chromosome import Chromosome
from python.base.Gene import Gene
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene


class BasicChromosome(Chromosome):
    """
    The Chromosome of a Basic Organism
    """

    _id: ChromosomeId
    _genes: Dict[type, Gene]

    def __init__(self,
                 drought_gene: DroughtToleranceGene = None,
                 light_gene: LightToleranceGene = None):
        self._id = ChromosomeId()

        if drought_gene is None:
            drought_gene = DroughtToleranceGene()

        if light_gene is None:
            light_gene = LightToleranceGene()

        self._genes = dict()
        self._genes[type(drought_gene)] = drought_gene
        self._genes[type(light_gene)] = light_gene
        return

    def get_chromosome_id(self) -> ChromosomeId:
        """
        Get the chromosome unique identifier
        :return: An chromosome UUID
        """
        return deepcopy(self._id)  # ensure id is immutable

    def get_gene(self,
                 gene_type: type) -> Gene:
        """
        Get the gene of the given type (as returned by Gene.type())
        :param gene_type: The type of Gene to get
        :return: The gene that matches the given type
        """
        if not isinstance(gene_type, type):
            raise ValueError(f'get_gene expects a type of gene to be passed')
        if gene_type not in self._genes.keys():
            raise NoSuchGeneTypeInChromosome
        return self._genes[gene_type]

    def set_gene(self,
                 gene: Gene) -> None:
        """
        Add or update the given gene within the Chromosome
        :param gene: The Gene to add/update within the Chromosome
        """
        if not isinstance(gene, Gene):
            raise NotAGene(type(gene))
        self._genes[type(gene)] = gene

    def get_gene_types(self) -> List[type]:
        """
        Get all the types for the Genes in the Chromosome (as returned by Gene.type())
        :return: A list of Gene types
        """
        return list(self._genes.keys())

    def get_diversity(self,
                      comparison_chromosome: 'Chromosome') -> float:
        """
        Get the diversity of the Chromosome with respect to the given Chromosome
        :param comparison_chromosome: The Chromosome to calculate diversity with respect to.
        :return: The relative diversity
        """
        genes_self = sorted(list(map(str, self.get_gene_types())))
        genes_compare = sorted(list(map(str, comparison_chromosome.get_gene_types())))
        if genes_self != genes_compare:
            raise ChromosomeMissMatch

        diversities: List[float] = []
        gene: Gene
        for gene in self._genes.values():
            diversities.append(gene.get_diversity(comparison_chromosome.get_gene(type(gene))))

        return np.array(diversities).mean(axis=-1)

    def __copy__(self):
        """
        Deep copy the Chromosome
        """
        return BasicChromosome(light_gene=copy(self.get_gene(LightToleranceGene)),  # NOQA
                               drought_gene=copy(self.get_gene(DroughtToleranceGene)))  # NOQA

    def __eq__(self,
               other: Chromosome):
        """
        Logical equality
        :param other: The other Chromosome to test equivalence with
        :return: True if this gene is logically equal to the 'other' given Chromosome
        """
        if isinstance(other, BasicChromosome):
            return self.get_gene(DroughtToleranceGene) == other.get_gene(DroughtToleranceGene) and \
                   self.get_gene(LightToleranceGene) == other.get_gene(LightToleranceGene)
        return False
