from typing import List
from abc import ABC, abstractmethod
from python.base.Genome import Genome
from python.base.Metrics import Metrics
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
    def fitness(self) -> float:
        """
        Return a number that represents the fitness of the organism.

        Until the organism has run at least once the fitness will be the value for least-fit.

        :return: Organism fitness expressed as a float.
        """
        raise NotImplementedError

    @abstractmethod
    def metrics(self) -> Metrics:
        """
        Return the current metrics for the organism

        Until the organism has run at least once the metrics will be default values

        :return: Organism fitness expressed as a float.
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
               step_size: float) -> None:
        """
        Randomly mutate the genes that comprise the Genome
        :param step_size: The size of the mutation to randomly apply + / -  the current value of the mutated genes
        """
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        """
        Test equality between BasicOrganism and a given object
        :param other: Object to check equality with.
        :return: True if BasicOrganism fields match
        Note: This is not an identity check, so we do not compare the id
        """
        raise NotImplementedError(
            "__eq__ must be implemented by all Organisms")

    @abstractmethod
    def __str__(self):
        """
        Basic Organism as string
        :return: Organism as String
        """
        raise NotImplementedError(
            "__str__ must be implemented by all Organisms")

    @abstractmethod
    def __repr__(self, *args, **kwargs):
        """
        Basic Organism as printable form
        :param args:
        :param kwargs:
        :return: Organism as printable string
        """
        raise NotImplementedError(
            "__repr__ must be implemented by all Organisms")

    def __hash__(self):
        """
        Makes organisms hashable for use in dictionaries
        :return: A unique has of the Organism
        """
        return hash(self.__repr__())
