import numpy as np
from typing import Union
from python.visualise.ParamScenarioFunc import ParamScenarioFunc


class ParamScenario:

    def __init__(self,
                 param_values_by_index: np.ndarray):
        """
        Parameter Scenario Constructor
        :param param_values_by_index: The list of parameter values for a given scenario index.
        """
        if param_values_by_index is None:
            raise ValueError("Parameter values is mandatory, None given")
        if not isinstance(param_values_by_index, np.ndarray):
            raise ValueError(
                f'Expected Numpy array for parameter values, but {param_values_by_index.__class__.__name__} given')
        self._size = param_values_by_index.size
        if self._size == 0:
            raise ValueError("Expected non zero length array of parameter values for scenario")

        np.reshape(param_values_by_index, (1, self._size))
        self._param_values_by_index = param_values_by_index

        self._direction = 1

        return

    @property
    def num_scenario_steps(self) -> int:
        return self._param_values_by_index.size

    def __scenario_func(self,
                        scenario_index: int,
                        *args,
                        **kwargs) -> float:
        """
        Return the given parameter value for the scenario index.
        :param scenario_index: The scenario index to return, cycles as we take index mod number of params
        :param kwargs:
        :return: The parameter value for the given scenario index.
        """
        idx = scenario_index % self._size
        if scenario_index > 0:
            if idx == 0:
                self._direction *= -1

        if self._direction == -1:
            idx = np.maximum(self._size - idx - 1, 0)

        return self._param_values_by_index[idx]

    @property
    def scenario_func(self) -> ParamScenarioFunc:
        """
        The scenario function that matches the ParamScenarioFunc protocol.
        :return: A scenario function that matches the ParamScenarioFunc protocol.
        """
        return self.__scenario_func

    @classmethod
    def single_value_scenario(cls,
                              x: Union[int, float]) -> ParamScenarioFunc:
        if not isinstance(x, (int, float)):
            raise ValueError(f'Single value scenario only for single numerics, but given {x.__class__.__name__}')
        return lambda *args, **kwargs: float(x)
