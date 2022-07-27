from typing import Dict, List
from python.base.Organism import Organism
from python.base.EnvironmentState import EnvironmentState
from python.organism.basic.BasicEnvironmentAttributes import BasicEnvironmentAttributes


class BasicEnvironmentState(EnvironmentState):
    """
    The current state of the basic environment
    """
    _hours_of_light_per_day: float
    _hours_since_last_rain: float
    _population: List[Organism]

    def __init__(self,
                 hours_of_light_per_day: float,
                 hours_since_last_rain: float,
                 population: List[Organism]):
        """
        The constructor for basic environment attributes
        :param hours_of_light_per_day: The current hours of light per day in environment
        :param hours_since_last_rain: The current hours since last rain in environment
        :param population: The current population of organisms
        """
        self._population = population
        self._hours_since_last_rain = hours_since_last_rain
        self._hours_of_light_per_day = hours_of_light_per_day
        return

    def get_attributes(self) -> Dict[BasicEnvironmentAttributes, object]:
        """
        Get the current environment attributes
        :return: A dictionary of environment attributes.
        """
        return {BasicEnvironmentAttributes.HOURS_SINCE_LAST_RAIN: self._hours_since_last_rain,
                BasicEnvironmentAttributes.HOURS_OF_LIGHT_PER_DAY: self._hours_of_light_per_day
                }

    def get_population(self) -> List[Organism]:
        """
        Get a list of current organisms that form the current population in teh environment
        :return: A dictionary of environment attributes.
        """
        return self._population
