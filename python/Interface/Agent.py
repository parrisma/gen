from abc import ABC, abstractmethod


class Agent(ABC):

    @abstractmethod
    def name(self) -> str:
        """
        The unique name of the agent
        """
        pass

    @abstractmethod
    def uuid(self) -> str:
        """
        The UUID of the agent
        """
        pass
