import os
import sys
from typing import Dict
import pickle
from kafka import KafkaProducer
from util.K8Util import K8Util
from python.id.EntityId import EntityId


class TestVisualisationProducer:

    def __init__(self):
        self._hostname = os.getenv('COMPUTERNAME')
        self._node_port_id = K8Util.get_node_port_number()
        self._producer = KafkaProducer(bootstrap_servers=[f'{self._hostname}:{self._node_port_id}'],
                                       value_serializer=lambda x:
                                       pickle.dumps(x))
        self._method_name: str = 'method_name'
        self._method_args: str = 'method_args'
        self._is_new_request: str = 'is_new_request'
        self._invocation_id: str = 'invocation_id'
        self._env_light_level_key: str = 'env_light_level'
        self._env_drought_level_key: str = 'env_light_level'
        self._num_organism_key: str = 'num_organism'

        self._hours_of_light_per_day: float = 12
        self._hours_since_last_rain: float = 2
        self._env_light_level: float = self._hours_of_light_per_day / 24.0
        self._env_drought_level: float = self._hours_since_last_rain / 24.0

    def send_updates(self) -> None:
        initalise_request: Dict = {self._method_name: 'initialise',
                                   self._invocation_id: EntityId().as_str(),
                                   self._is_new_request: str(True),
                                   self._method_args: {self._env_light_level_key: self._env_light_level,
                                                       self._env_drought_level_key: self._hours_since_last_rain,
                                                       self._num_organism_key: 10}}
        future = self._producer.send('visualisation_agent_744488', value=initalise_request)
        try:
            record_metadata = future.get(timeout=10)
            print(record_metadata.topic)
            print(record_metadata.partition)
            print(record_metadata.offset)
        except Exception as exp:
            print(f'{exp}')
        self._producer.flush()


if __name__ == "__main__":
    TestVisualisationProducer().send_updates()
    sys.exit(0)
