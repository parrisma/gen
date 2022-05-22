from abc import ABC, abstractmethod


class Env(ABC):
    """
    The environment in which evolution occurs.
    """

    @abstractmethod
    def create_generation_zero(self):
        """
        Create the initial generation zero population.
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
        Call the run method on each member of the population
        """
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        """
        Run the evolutionary simulation until termination condition are met
        """
        raise NotImplementedError
