from typing import List
from abc import ABC, abstractmethod
from copy import copy

import numpy as np

from python.base.Genome import Genome
from python.base.EnvironmentState import EnvironmentState
from python.id.OrganismId import OrganismId


class Organism(ABC):
    """
    The interface for the entity 'living' and 'evolving' in the environment
    """

    @abstractmethod
    def get_id(self) -> OrganismId:
        """
        Return the string equivalent of the UUID of the Organism
        :return: The globally unique Id of the Organism
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Establish if the organism is still alive an operable in the environment
        :return: True, if the organism is alive
        """
        raise NotImplementedError

    @abstractmethod
    def run(self,
            environment_state: 'EnvironmentState') -> 'Organism':
        """
        Life is divided up into single step quanta,where the environment will give every organism the opportunity
        to take a single life step before iterating ove the population again
        :param environment_state: The current state of the environment at the point the Organism is run
        :return: reference to our self .
        """
        raise NotImplementedError

    @abstractmethod
    def get_relative_diversity(self,
                               comparison_organism: List['Organism']) -> float:
        """
        Get the diversity of the Organism with respect to the given Organism
        :param comparison_organism: The Organism to calculate diversity with respect to.
        :return: The relative diversity in the range 0.0 to 1.0
        """
        raise NotImplementedError

    @abstractmethod
    def get_genome(self) -> Genome:
        """
        Get the Genome of the Organism
        :return: The Organisms Genome
        """
        raise NotImplementedError

    @abstractmethod
    def crossover(self,
                  mix_rate: float,
                  organism: 'Organism') -> Genome:
        """
        Based on the mix rate return a Genome with genes mixed between the Organism and the given
        Organism
        :param mix_rate: The rate of mixing of Genes between the Chromosomes
        :param organism: The organism to cross with
        :return: The Chromosomes resulting from the crossover.
        """
        raise NotImplementedError

    @abstractmethod
    def mutate(self,
               step_size: float) -> Genome:
        """
        Randomly mutate the genes that comprise the Genome
        :param step_size: The size of the mutation to randomly apply + / -  the current value of the mutated genes
        :return: The Genome resulting from the mutation.
        """
        raise NotImplementedError

    @classmethod
    def crossover_genomes(cls,
                          mix_rate: float,
                          to_organism: 'Organism',
                          from_organism: 'Organism') -> Genome:
        """
        Based on the mix rate return a list of chromosomes with genes mixed from -> to Organism
        :param mix_rate: The rate of mixing of Genes between the Chromosomes
        :param to_organism: The organism to cross genes to
        :param from_organism: The organism to cross genes from
        :return: The Genome resulting from the crossover.
        """
        if mix_rate > 1.0 or mix_rate < 0.0:
            raise ValueError(f'mix_rate is a probability and must be in range 0.0 to 1.0 - given {mix_rate}')

        cross_genome = copy(from_organism.get_genome())
        current_genes = Genome.gene_list(to_organism.get_genome())
        lcg = len(current_genes)
        current_genes.extend([None] * lcg)  # NOQA - dummy entries selected by residual probabilty
        prob_func: List[float] = ([mix_rate / lcg] * lcg)
        prob_func.extend([(1.0 - mix_rate) / lcg] * lcg)
        mix_genes = np.random.choice(current_genes, p=prob_func, size=lcg, replace=False)
        cross_genes = Genome.gene_list(cross_genome)
        for mix_gene in mix_genes:
            if mix_gene is not None:
                for cross_gene in cross_genes:
                    if isinstance(cross_gene, type(mix_gene)):
                        cross_gene = copy(mix_gene)  # Assign by reference will update gene in cross_genome

        return cross_genome
