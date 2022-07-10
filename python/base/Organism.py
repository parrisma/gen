from typing import List
from abc import ABC, abstractmethod
from python.base.Chromosome import Chromosome
from python.base.Metrics import Metrics
from python.base.Diversity import Diversity
from python.id.OrganismId import OrganismId


class Organism(ABC):
    """
    The interface for the entity 'living' and 'evolving' in the environment.
    """

    @abstractmethod
    def get_id(self) -> OrganismId:
        """
        Return the string equivalent of the UUID of the Organism
        :return: The globally unique Id of the Organism
        """
        raise NotImplementedError

    @abstractmethod
    def run(self) -> Metrics:
        """
        Life is divided up into single step quanta,where the environment will give every organism the opportunity
        to take a single life step before iterating ove the population again.
        :return: Metrics collected during the run cycle for the Organism.
        """
        raise NotImplementedError

    @abstractmethod
    def get_diversity(self,
                      comparison_organism: List['Organism']) -> Diversity:
        """
        Get the diversity of the Organism with respect to the given Organism
        :param comparison_organism: The Organism to calculate diversity with respect to.
        :return: The relative diversity
        """
        raise NotImplementedError

    @abstractmethod
    def get_chromosomes(self) -> List[Chromosome]:
        """
        Get the chromosomes of the Organism
        :return: A list if chromosomes
        """
        raise NotImplementedError

    @abstractmethod
    def crossover(self,
                  mix_rate: float,
                  organism: 'Organism') -> List[Chromosome]:
        """
        Based on the mix rate return a list of chromosomes with genes mixed between the Organism and the given
        chromosomes.
        :param mix_rate: The rate of mixing of Genes between the Chromosomes
        :param organism: The organism to cross with
        :return: The Chromosomes resulting from the crossover.
        """
        raise NotImplementedError

    @abstractmethod
    def mutate(self,
               mutation_rate: float) -> List[Chromosome]:
        """
        Based on a defined <mutation_rate>. introduce random perturbation into the Organisms populations Genes
        :param mutation_rate: The rate at which Genes are affected by random perturbations
        :return: The Chromosomes resulting from the mutation.
        """
        raise NotImplementedError

    @abstractmethod
    def __call__(self, *_, **__) -> Metrics:
        """
        Organisms are callable, where callable means to execute the run method
        :param _:
        :param __:
        :return: Metrics collected during the run cycle for the Organism.
        """
        raise NotImplementedError
