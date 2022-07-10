from abc import ABC, abstractmethod
from python.id.GeneId import GeneId


class Gene(ABC):
    """
    A means to hold the data required to evaluate the relative fitness of organisms
    """

    @abstractmethod
    def get_gene_id(self) -> GeneId:
        """
        Get the gene unique identifier
        :return: An gene globally unique id
        """
        raise NotImplementedError

    @abstractmethod
    def get_diversity(self,
                      comparison_gene: 'Gene') -> float:
        """
        Get the diversity of the Gene with respect to the given Gene
        :param comparison_gene: The gene to calculate diversity with respect to.
        :return: The relative diversity
        """
        raise NotImplementedError

    @abstractmethod
    def mutate(self) -> None:
        """
        Make a random mutation to the Gene
        """
        raise NotImplementedError

    @abstractmethod
    def value(self):
        """
        Return the value of the Gene - the return type is specific to the Gene
        """
        raise NotImplementedError

    @abstractmethod
    def type(self) -> str:
        """
        Return the type of the Gene
        """
        raise NotImplementedError
