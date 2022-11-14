import argparse
from typing import Dict, List, Tuple
from python.interface.Visualiser import Visualiser
from python.id.EntityId import EntityId


class BasicEnvVisualiserProxy(Visualiser):
    FRAME_INDEX: str = 'frame_index'
    FRAME_DATA: str = 'frame_data'
    ENV_LIGHT_LEVEL: str = 'env_light_level'
    ENV_DROUGHT_LEVEL: str = 'env_drought_level'
    NUM_ORGANISMS: str = 'num_organism'
    METHOD_NAME: str = 'method_name'
    METHOD_ARGS: str = 'method_args'
    IS_NEW_REQUEST: str = 'is_new_request'
    INVOCATION_ID: str = 'invocation_id'

    def __init__(self,
                 hours_of_light_per_day: float,
                 hours_since_last_rain: float,
                 num_organisms: int):
        self._hours_of_light_per_day: float = hours_of_light_per_day
        self._hours_since_last_rain: float = hours_since_last_rain
        self._env_light_level: float = self._hours_of_light_per_day / 24.0
        self._env_drought_level: float = self._hours_since_last_rain / 24.0
        self._num_organisms = num_organisms
        return

    def initialise(self,
                   **kwargs) -> Dict:
        """
        Generate an initialise message
        :return: An Initialise message
        """
        return {self.METHOD_NAME: 'initialise',
                self.INVOCATION_ID: EntityId().as_str(),
                self.IS_NEW_REQUEST: str(True),
                self.METHOD_ARGS: {self.ENV_LIGHT_LEVEL: kwargs.get(self.ENV_LIGHT_LEVEL, self._env_light_level),
                                   self.ENV_DROUGHT_LEVEL: kwargs.get(self.ENV_DROUGHT_LEVEL, self._env_drought_level),
                                   self.NUM_ORGANISMS: kwargs.get(self.NUM_ORGANISMS, self._num_organisms)}}

    def update(self,
               frame_index: int,
               frame_data: List[Tuple[float, float, float]],
               **kwargs) -> Dict:
        """
        Generate an update message
        :param frame_index: The update frame index
        :param frame_data: The update frame data
        :return: An update message as dictionary
        """
        return {self.METHOD_NAME: 'update',
                self.INVOCATION_ID: EntityId().as_str(),
                self.IS_NEW_REQUEST: str(True),
                self.METHOD_ARGS: {self.FRAME_INDEX: frame_index,
                                   self.FRAME_DATA: frame_data}}

    def terminate(self,
                  **kwargs) -> Dict:
        """
        Return: A Termination message
        """
        return {self.METHOD_NAME: 'terminate',
                self.INVOCATION_ID: EntityId().as_str(),
                self.IS_NEW_REQUEST: str(True),
                self.METHOD_ARGS: {}}

    def show(self,
             **kwargs) -> None:
        """
        Show the current view.
        """
        pass
