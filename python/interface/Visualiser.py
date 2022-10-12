from abc import ABC, abstractmethod


class Visualiser(ABC):

    @abstractmethod
    def initialise(self,
                   **kwargs) -> None:
        """
        Initialise the view
        """
        pass

    @abstractmethod
    def update(self,
               **kwargs) -> None:
        """
        Update the view
        """
        pass

    @abstractmethod
    def terminate(self,
                  **kwargs) -> None:
        """
        Tear down the view and release any resources
        """
        pass

    @abstractmethod
    def show(self,
             **kwargs) -> None:
        """
        Show the current plot.
        """
        pass
