from enum import Enum, unique, auto


@unique
class BasicEnvironmentAttributes(Enum):
    """
    The attributes of the basic environment
    """
    HOURS_OF_LIGHT_PER_DAY = auto()
    HOURS_SINCE_LAST_RAIN = auto()
