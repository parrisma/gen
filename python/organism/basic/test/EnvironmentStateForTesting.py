from typing import Dict
from python.base.EnvironmentState import EnvironmentState
from python.organism.basic.test.EnvironmentAttributesForTesting import EnvironmentAttributesForTesting


class EnvironmentStateForTesting(EnvironmentState):
    """
    The current state of the basic environment
    """

    def __init__(self):
        """
        The constructor for test environment attributes
        """
        return

    def get_attributes(self) -> Dict[EnvironmentAttributesForTesting, object]:
        """
        Get the current environment attributes
        :return: A dictionary of environment attributes.
        """
        return {}
