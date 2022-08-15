from typing import Dict, List
from python.base.Organism import Organism
from python.base.EnvironmentState import EnvironmentState
from python.organism.basic.BasicEnvironmentAttributes import BasicEnvironmentAttributes


class BasicEnvironmentState(EnvironmentState):
    """
    The current state of the basic environment
    """
    _avg_hours_of_light_per_day: float
    _avg_hours_between_rain: float
    _population: List[Organism]

    def __init__(self,
                 avg_hours_of_light_per_day: float,
                 avg_hours_between_rain: float,
                 population: List[Organism]):
        """
        The constructor for basic environment attributes
        :param avg_hours_of_light_per_day: The current hours of light per day in environment
        :param avg_hours_between_rain: The current hours since last rain in environment
        :param population: The current population of organisms
        """
        self._population = population
        self._avg_hours_between_rain = avg_hours_between_rain
        self._avg_hours_of_light_per_day = avg_hours_of_light_per_day
        return

    def get_attributes(self) -> Dict[BasicEnvironmentAttributes, object]:
        """
        Get the current environment attributes
        :return: A dictionary of environment attributes.
        """
        return {BasicEnvironmentAttributes.AVG_HOURS_BETWEEN_RAIN: self._avg_hours_between_rain,
                BasicEnvironmentAttributes.AVG_HOURS_OF_LIGHT_PER_DAY: self._avg_hours_of_light_per_day,
                BasicEnvironmentAttributes.POPULATION: self._population}
