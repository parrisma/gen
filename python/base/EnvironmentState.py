from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List
from python.base.Organism import Organism


class EnvironmentState(ABC):
    """
    The current state of the environment
    """

    @abstractmethod
    def get_attributes(self) -> Dict[Enum, object]:
        """
        Get the current environment attributes
        :return: A dictionary of environment attributes.
        """
        raise NotImplementedError

    @abstractmethod
    def get_population(self) -> List[Organism]:
        """
        Get a list of current organisms that form the current population in teh environment
        :return: A dictionary of environment attributes.
        """
        raise NotImplementedError
