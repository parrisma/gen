from typing import Any
from abc import ABC, abstractmethod


class Visualiser(ABC):

    @abstractmethod
    def initialise(self,
                   **kwargs) -> Any:
        """
        Initialise the view
        """
        pass

    @abstractmethod
    def update(self,
               **kwargs) -> Any:
        """
        Update the view
        """
        pass

    @abstractmethod
    def terminate(self,
                  **kwargs) -> Any:
        """
        Tear down the view and release any resources
        """
        pass

    @abstractmethod
    def show(self,
             **kwargs) -> Any:
        """
        Show the current plot.
        """
        pass
