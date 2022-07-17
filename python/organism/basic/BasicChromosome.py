from typing import Dict, List
from copy import deepcopy
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
        if self.get_gene_types() != comparison_chromosome.get_gene_types():
            raise ChromosomeMissMatch

        diversities: List[float] = []
        gene: Gene
        for gene in self._genes:
            diversities.append(gene.get_diversity(comparison_chromosome.get_gene(gene.type())))

        return np.array(diversities).mean(axis=-1)
