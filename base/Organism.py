import uuid
from abc import ABC, abstractmethod
from base.Metrics import Metrics


class Organism(ABC):
    """
    The interface for the entity 'living' and 'evolving' in the environment.
    """

    @abstractmethod
    def get_id_as_str(self) -> str:
        """
        Return the string equivalent of the UUID of the Organism
        :return: UUID as string
        """
        raise NotImplementedError

    @abstractmethod
    def run(self) -> Metrics:
        """
        Life is divided up into single step quanta,where the environment will give every organism the opportunity
        to take a single life step before iterating ove the population again.
        :return: Metrics collected during the run cycle for the Organism.
        """
        raise NotImplementedError

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """
        Organisms are callable, where callable means to execute the run method
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError
