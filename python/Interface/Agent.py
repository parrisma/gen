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

    def __str__(self) -> str:
        return f'Agent: {self.name()} @ id: {self.uuid()}'

    def __repr__(self) -> str:
        return self.__str__()
