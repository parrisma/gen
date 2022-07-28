from enum import Enum, unique, auto


@unique
class BasicEnvironmentAttributes(Enum):
    """
    The attributes of the basic environment
    """
    AVG_HOURS_OF_LIGHT_PER_DAY = auto()
    AVG_HOURS_BETWEEN_RAIN = auto()
