from abc import ABC, abstractmethod
from python.base.Metrics import Metrics
from python.id.FitnessId import FitnessId


class Fitness(ABC):
    """
    A means to hold the data required to evaluate the relative fitness of organisms
    """

    @abstractmethod
    def __init__(self,
                 _: Metrics):
        """
        Construct Organism Fitness given Organism Metrics
        :param _: The Metrics to construct fitness from
        """
        raise NotImplementedError

    @abstractmethod
    def get_fitness_id(self) -> FitnessId:
        """
        Get the organism unique identifier to which the metrics relate
        :return: A fitness globally unique id
        """
        raise NotImplementedError

    @abstractmethod
    def get_fitness_value(self) -> float:
        """
        Get Fitness as measured by a number in range 0.0 to 1.0
        :return: Fitness as a float
        """
        raise NotImplementedError
