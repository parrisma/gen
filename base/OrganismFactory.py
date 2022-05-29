from typing import List
from abc import ABC, abstractmethod
from base.Chromosome import Chromosome
from base.Organism import Organism


class OrganismFactory(ABC):
    """
    The interface for generating new organisms
    """

    @abstractmethod
    def new(self,
            chromosomes: List[Chromosome]) -> Organism:
        """
        Create a new organism from teh given Chromosomes
        :param chromosomes: The Chromosomes to create the new organism with.
        :return: An Organism
        """
        raise NotImplementedError
