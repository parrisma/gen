from typing import Protocol


class ParamScenarioFunc(Protocol):
    """
    The signature of the function that returns a parameter value for given scenario index.
    index < 0 : raise ValueError
    index = 0 : Initial Value
    index > 0 : Parameter value for that scenario index.
    """

    def __call__(self, scenario_index: int, **kwargs) -> float: ...
