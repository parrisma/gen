import uuid
from abc import ABC, abstractmethod


class Metrics(ABC):
    """
    The interface for handling metrics returned from the run of an Organism
    """

    @abstractmethod
    def get_organism_id(self) -> uuid:
        """
        Get the organism unique identifier to which the metrics relate
        :return: An Organism UUID
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Evaluate if teh Organism is still alive and able to participate in a call to it's run method.
        :return: True if teh Organism is alive.
        """
        raise NotImplementedError
