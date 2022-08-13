import sys
from abc import ABC, abstractmethod
from python.id.MetricsId import MetricsId


class Metrics(ABC):
    """
    The interface for handling metrics returned from the run of an Organism
    """
    LEAST_FIT: float = sys.float_info.min
    MOST_FIT: float = sys.float_info.max

    @abstractmethod
    def get_metrics_id(self) -> MetricsId:
        """
        Get the metrics unique identifier to which the metrics relate
        :return: A globally unique metrics id
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Evaluate if the Organism is still alive and able to participate in a call to it's run method.
        :return: True if the Organism is alive.
        """
        raise NotImplementedError

    @abstractmethod
    def get_fitness(self) -> float:
        """
        Get the current fitness value
        :return: Fitness expressed as a float
        """
        raise NotImplementedError

    @abstractmethod
    def __copy__(self):
        """
        Create a copy of the metrics.
        :return: A copy of the current metrics
        """
        raise NotImplementedError(
            "__copy__ must be implemented by all Metrics")

    @abstractmethod
    def __eq__(self, other):
        """
        Logical equality
        :param other: The other object to test equivalence with
        :return: True if this gene is logically equal to the 'other' given object
        """
        raise NotImplementedError(
            "__copy__ must be implemented by all Metrics")
