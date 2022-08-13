from abc import ABC, abstractmethod
from python.base.Organism import Organism
from python.base.Genome import Genome


class OrganismFactory(ABC):
    """
    The interface for generating new organisms
    """

    @abstractmethod
    def new(self,
            genome: Genome = None) -> Organism:
        """
        Create a new organism from the given Chromosomes
        :param genome: The Genome to use to create the organism, if None a randomised Genome is used.
        :return: An Organism
        """
        raise NotImplementedError
