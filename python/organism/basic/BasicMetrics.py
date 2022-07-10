import uuid
from python.base.Metrics import Metrics
from python.id.MetricsId import MetricsId


class BasicMetrics(Metrics):
    _metrics_id: MetricsId
    _alive: bool

    def __init__(self,
                 organism_id: uuid):
        self._alive = True
        self.metrics_id = MetricsId()
        return

    def get_metrics_id(self) -> MetricsId:
        return self._metrics_id

    def is_alive(self) -> bool:
        return self._alive

    def set_alive(self,
                  alive: bool) -> None:
        self._alive = alive
        return
