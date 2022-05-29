from abc import ABC, abstractmethod
from id.DiversityId import DiversityId


class Diversity(ABC):
    """
    A means to hold the data required to evaluate the relative diversity of organisms
    """

    @abstractmethod
    def __init__(self):
        """
        Construct Organism Diversity given Organism Metrics
        """
        raise NotImplementedError

    @abstractmethod
    def get_diversity_id(self) -> DiversityId:
        """
        Get the organism unique identifier to which the diversity relates
        :return: An Diversity Id
        """
        raise NotImplementedError

    @abstractmethod
    def get_diversity_value(self) -> float:
        """
        Get diversity as measured by a number in range 0.0 to 1.0
        :return: Diversity as a float
        """
        raise NotImplementedError
