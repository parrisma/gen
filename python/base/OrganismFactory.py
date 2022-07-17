from abc import ABC, abstractmethod
from typing import List
from python.base.Organism import Organism
from python.base.Genome import Genome


class OrganismFactory(ABC):
    """
    The interface for generating new organisms
    """

    @abstractmethod
    def new(self,
            genome: Genome) -> Organism:
        """
        Create a new organism from the given Chromosomes
        :param genome: The Genome from which to create the organism
        :return: An Organism
        """
        raise NotImplementedError
