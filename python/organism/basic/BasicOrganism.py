from typing import List, Dict
import numpy as np
from copy import copy
from python.id.OrganismId import OrganismId
from python.base.Organism import Organism
from python.base.Gene import Gene
from python.base.Chromosome import Chromosome
from python.base.Genome import Genome
from python.base.EnvironmentState import EnvironmentState
from python.base.Metrics import Metrics
from python.organism.basic.BasicMetrics import BasicMetrics
from python.organism.basic.BasicEnvironmentAttributes import BasicEnvironmentAttributes
from python.organism.basic.BasicChromosome import BasicChromosome
from python.organism.basic.BasicGenome import BasicGenome
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene


class BasicOrganism(Organism):
    _id: OrganismId
    _genome: BasicGenome
    _metrics: BasicMetrics
    _light_tolerance: float
    _drought_tolerance: float

    @classmethod
    def __limit(cls,
                v: float,
                lim: float):
        """
        Clip the given value in the clipped -lim to +lim
        :param v: The value to be capped
        :param lim: The limit
        :return: The value clipped in range -lim to +lim
        """
        return np.sign(v) * np.maximum(np.absolute(v), lim)

    def __init__(self,
                 genome: BasicGenome):
        self._id = OrganismId()
        self._genome = genome
        self._metrics = BasicMetrics(alive=True, fitness=Metrics.LEAST_FIT)
        # Express Chromosomes
        chromosome: BasicChromosome = self._genome.get_chromosome(BasicChromosome)  # NOQA
        self._light_tolerance = chromosome.get_gene(LightToleranceGene).value()
        self._drought_tolerance = chromosome.get_gene(DroughtToleranceGene).value()
        return

    def run(self,
            environment_state: EnvironmentState) -> Organism:
        """
        Execute a life cycle of the organism an update the metrics
        :param environment_state: The current state of the environment in which the organism is living.
        :return: A reference to this (self) Organism after it has executed a life cycle.
        """
        bm: Dict[BasicEnvironmentAttributes, object] = environment_state.get_attributes()  # NOQA
        ave_light = BasicOrganism.__limit(bm.get(BasicEnvironmentAttributes.AVG_HOURS_OF_LIGHT_PER_DAY), 24)
        ave_drought = BasicOrganism.__limit(bm.get(BasicEnvironmentAttributes.AVG_HOURS_BETWEEN_RAIN), (24 * 7))

        light_fitness = (1 - np.sign(self._light_tolerance) * np.power(self._light_tolerance, 2)) + (
                np.power(ave_light / 24, 2) * 2 * np.sign(self._light_tolerance))

        self._metrics = BasicMetrics(alive=True, fitness=light_fitness)

        return self

    def is_alive(self) -> bool:
        """
        Establish if the organism is still alive an operable in the environment
        :return: True, if the organism is alive
        """
        return self._metrics.is_alive()

    def get_id(self) -> str:
        return self._id.as_str()

    def get_relative_diversity(self,
                               comparison_organisms: List['Organism']) -> float:
        """
        Get the diversity of the Organism with respect to the given Organism
        :param comparison_organisms: The Organism to calculate diversity with respect to.
        :return: The relative diversity
        """
        rel_div = list()
        for o in comparison_organisms:
            rel_div.append(self._genome.get_diversity(o.get_genome()))  # NOQA

        return (np.asarray(rel_div).sum()) / len(rel_div)

    def get_genome(self) -> Genome:
        """
        Get the chromosomes of the Organism
        :return: A list of chromosomes
        """
        return self._genome

    def crossover(self,
                  mix_rate: float,
                  organism: 'BasicOrganism') -> Genome:
        """
        Based on the mix rate return a list of chromosomes with genes mixed between the Organism and the given
        chromosomes.
        :param mix_rate: The rate of mixing of Genes between the Chromosomes
        :param organism: The organism to cross genes with
        :return: The Genome resulting from the crossover.
        """
        return Organism.crossover_genomes(from_organism=organism, to_organism=self, mix_rate=mix_rate)

    def mutate(self,
               mutation_rate: float) -> Genome:
        """
        Based on a defined <mutation_rate>. introduce random perturbation into the Organisms populations Genes
        :param mutation_rate: The rate at which Genes are affected by random perturbations
        :return: The Genome resulting from the mutation.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.get_id()

    def __repr__(self, *args, **kwargs) -> str:
        return self.__str__()
