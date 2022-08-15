from typing import List, Dict, Union
from copy import copy
from python.id.OrganismId import OrganismId
from python.base.Organism import Organism
from python.base.Genome import Genome
from python.base.Metrics import Metrics
from python.base.EnvironmentState import EnvironmentState
from python.organism.basic.BasicMetrics import BasicMetrics


class OrganismForTesting(Organism):
    """
    Test Organism with hard-wired metrics for testing.
    """
    _id: OrganismId
    _fitness: float
    _diversity: float
    _metrics: BasicMetrics

    def __init__(self,
                 fitness: float,
                 diversity: float):
        self._id = OrganismId()
        self._fitness = fitness
        self._diversity = diversity
        self._metrics = BasicMetrics(alive=True, fitness=self._fitness, diversity=diversity)
        return

    def run(self,
            environment_state: EnvironmentState) -> Organism:
        """
        Execute a life cycle of the organism an update the metrics
        :param environment_state: The current state of the environment in which the organism is living.
        :return: A reference to this (self) Organism after it has executed a life cycle.
        """
        # Nothing to do as metrics are fixed at construct time to allow for predictable testing
        # so just construct a new metrics based on fixed values.
        self._metrics = BasicMetrics(alive=True, fitness=self._fitness, diversity=self._diversity)
        return self

    def is_alive(self) -> bool:
        """
        Establish if the organism is still alive an operable in the environment
        :return: True, if the organism is alive
        """
        return self._metrics.is_alive()

    def fitness(self) -> float:
        """
        Return a number that represents the fitness of the organism.

        Until the organism has run at least once the fitness will be the value for least-fit.

        :return: Organism fitness expressed as a float.
        """
        return self._metrics.get_fitness()

    def metrics(self) -> Metrics:
        """
        Return the current metrics for the organism

        Until the organism has run at least once the metrics will be default values

        :return: Organism fitness expressed as a float.
        """
        return copy(self._metrics)

    def get_id(self) -> str:
        return self._id.as_str()

    def get_relative_diversity(self,
                               comparison_organisms: List['OrganismForTesting']) -> float:
        """
        Get the diversity of the Organism with respect to the given Organism
        :param comparison_organisms: The Organism to calculate diversity with respect to.
        :return: The relative diversity
        """
        raise NotImplementedError(f'Method not supported for testing by {self.__class__.__name__}')

    def get_genome(self) -> Genome:
        """
        Get the chromosomes of the Organism
        :return: A list of chromosomes
        """
        raise NotImplementedError(f'Method not supported for testing by {self.__class__.__name__}')

    def crossover(self,
                  mix_rate: float,
                  organism: 'OrganismForTesting') -> Genome:
        """
        Based on the mix rate return a list of chromosomes with genes mixed between the Organism and the given
        chromosomes.
        :param mix_rate: The rate of mixing of Genes between the Chromosomes
        :param organism: The organism to cross genes with
        :return: The Genome resulting from the crossover.
        """
        raise NotImplementedError(f'Method not supported for testing by {self.__class__.__name__}')

    def mutate(self,
               step_size: Union[float, Dict[type, float]]) -> Genome:
        """
        Based on a defined <mutation_rate>. introduce random perturbation into the Organisms populations Genes
        :param step_size: An absolute step size as float to be applied to all gene types ot
        :return: The Genome resulting from the mutation.
        """
        raise NotImplementedError(f'Method not supported for testing by {self.__class__.__name__}')

    def __str__(self) -> str:
        return self.get_id()

    def __repr__(self, *args, **kwargs) -> str:
        return self.__str__()

    def __eq__(self, other):
        """
        Test equality between BasicOrganism and a given object
        :param other: Object to check equality with.
        :return: True if BasicOrganism fields match
        Note: This is not an identity check, so we do not compare the id
        """
        if isinstance(other, OrganismForTesting):
            if self._id == other._id:
                return True
        return False
