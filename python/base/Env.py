from abc import ABC, abstractmethod
from python.base.EnvironmentState import EnvironmentState


class Env(ABC):
    """
    The environment in which evolution occurs.
    """

    @abstractmethod
    def create_generation_zero(self):
        """
        Create the initial generation zero population.
        :return: A List of Organisms
        """
        raise NotImplementedError

    @abstractmethod
    def termination_conditions_met(self) -> bool:
        """
        Evaluate the conditions that will indicate when the simulation has ended
        :return: True if the conditions to exit run have been met
        """
        raise NotImplementedError

    @abstractmethod
    def run_population(self) -> None:
        """
        Iterate over the population and call the run method on each
        """
        raise NotImplementedError

    @abstractmethod
    def rank_and_select_survivors(self) -> None:
        """
        Based on the current fitness metrics, establish which of the current population should
        survive into the next generation
        """
        raise NotImplementedError

    @abstractmethod
    def create_next_generation(self) -> None:
        """
        Create the next generation of Organisms
        """
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        """
        Run the evolutionary simulation until termination condition are met
        """
        raise NotImplementedError

    @abstractmethod
    def get_state(self) -> EnvironmentState:
        """
        Get the current state of the Environment
        :return: The current environment state
        """
        raise NotImplementedError
