from python.base.Metrics import Metrics
from python.id.MetricsId import MetricsId


class BasicMetrics(Metrics):
    _metrics_id: MetricsId
    _fitness: float
    _alive: bool

    def __init__(self,
                 alive: bool,
                 fitness: float):
        """
        Basic Metrics constructor
        :param alive: The value of alive as boolean
        :param fitness: The value of fitness as float
        """
        self._alive = alive
        self._fitness = fitness
        self._metrics_id = MetricsId()
        return

    def get_metrics_id(self) -> MetricsId:
        """
        Get the globally unique id of these metrics.
        :return: Metrics uuid
        """
        return self._metrics_id

    def is_alive(self) -> bool:
        """
        Is the organism still alive
        :return: True if teh Organism is alive, else False
        """
        return self._alive

    def get_fitness(self) -> float:
        """
        Get the current fitness value
        :return: Fitness expressed as a float
        """
        return self._fitness
