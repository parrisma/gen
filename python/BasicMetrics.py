import uuid
from base.Metrics import Metrics


class BasicMetrics(Metrics):
    _organism_uuid: uuid
    _alive: bool

    def __init__(self,
                 organism_id: uuid):
        self._alive = True
        self._organism = organism_id
        return

    def get_organism_id(self) -> uuid:
        return self._organism

    def is_alive(self) -> bool:
        return self._alive

    def set_alive(self,
                  alive: bool) -> None:
        self._alive = alive
        return
