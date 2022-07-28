from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict


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
