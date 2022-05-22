import uuid
from base.Organism import Organism
from BasicMetrics import BasicMetrics


class BasicOrganism(Organism):
    _metrics: BasicMetrics
    _id: uuid

    def __init__(self):
        self._id = uuid.uuid4()
        self._metrics = BasicMetrics(self.get_id_as_str())
        print(f'{self._id} Organism is born')
        return

    def __call__(self, *args, **kwargs):
        return self.run()

    def run(self) -> BasicMetrics:
        print(f'{self._id} Organism has run')
        self._metrics.set_alive(False)
        return self._metrics

    def get_id_as_str(self) -> str:
        return self._id.hex

    def __str__(self) -> str:
        return self.get_id_as_str()

    def __repr__(self, *args, **kwargs) -> str:
        return self.__str__()
