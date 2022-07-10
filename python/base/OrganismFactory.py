from abc import ABC, abstractmethod
from python.base.Organism import Organism


class OrganismFactory(ABC):
    """
    The interface for generating new organisms
    """

    @abstractmethod
    def new(self) -> Organism:
        """
        Create a new organism from the given Chromosomes
        :return: An Organism
        """
        raise NotImplementedError
