from enum import Enum, unique, auto


@unique
class EnvironmentAttributesForTesting(Enum):
    """
    Test attributes
    """
    EMPTY = auto()
