from typing import Protocol


class FuncOfZInTermsOfXY(Protocol):
    """
    The signature of the function of z in terms of x,y used to plot the surface
    """

    def __call__(self, x: float, y: float, scenario_index: int, **kwargs) -> float: ...
