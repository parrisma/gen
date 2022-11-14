import argparse
import os
import pickle
from typing import List, Tuple
from rltrace.Trace import Trace
from kafka import KafkaProducer
from util.K8Util import K8Util
from interface.Agent import Agent
from python.id.EntityId import EntityId
from python.organism.basic.BasicEnvVisualiserProxy import BasicEnvVisualiserProxy


class VisualisationAgentProxy(Agent):

    def __init__(self,
                 trace: Trace,
                 args,
                 basic_visualiser_env_proxy: BasicEnvVisualiserProxy):
        self._trace = trace
        self._agent_name = f'VisualisationServiceProxy'
        self._uuid = EntityId().as_str()

        self._topic = args.topic
        self._kafka_kubernetes_service_name: str = args.kafka_kubernetes_service_name
        self._kafka_kubernetes_namespace: str = args.kafka_kubernetes_namespace
        self._kafka_external_port: int = args.kafka_external_port
        self._kafka_group: str = args.kafka_group
        self._hostname = os.getenv('COMPUTERNAME')
        self._node_port_id = K8Util.get_node_port_number()
        self._producer = KafkaProducer(bootstrap_servers=[f'{self._hostname}:{self._node_port_id}'],
                                       value_serializer=lambda x:
                                       pickle.dumps(x))
        self._basic_visualiser_env_proxy = basic_visualiser_env_proxy
        self._trace.log(f'Visualisation Agent {self} publishing to {self._topic} @ \
                          {self._hostname}:{self._node_port_id}')
        return

    @staticmethod
    def add_args(parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-t", "--topic",
                            help="Kafka topic name to listen for commands on",
                            default=f'visualisation_agent_{EntityId().as_str()}',
                            type=str)
        parser.add_argument("-s", "--kafka_kubernetes_service_name",
                            help="The name of the Kubernetes service",
                            default='kafka-service',
                            type=str)
        parser.add_argument("-n", "--kafka_kubernetes_namespace",
                            help="The kubernetes namespace where all kafka elements exist",
                            default='kafka',
                            type=str)
        parser.add_argument("-p", "--kafka_external_port",
                            help="The port id kafka listens on for external connects",
                            default=19093,
                            type=int)
        parser.add_argument("-g", "--kafka_group",
                            help="The Kafka consumer group for the Agents to operate as part of",
                            default=f'VisualisationGroup',
                            type=str)

    def name(self) -> str:
        """
        The unique name of the agent
        """
        return self._agent_name

    def uuid(self) -> str:
        """
        The UUID of the agent
        """
        return self._uuid

    def initialise(self,
                   **kwargs) -> None:
        """
        Send initialise request to Visualisation service
        """
        _ = self._producer.send(topic=self._topic,
                                value=self._basic_visualiser_env_proxy.initialise(**kwargs))
        self._trace.log(f'Visualisation Agent {self} sent initialise message')
        return

    def update(self,
               **kwargs) -> None:
        """
        Send update request to Visualisation service


        """
        frame_index: int = kwargs.get(BasicEnvVisualiserProxy.FRAME_INDEX, None)
        frame_data: List[Tuple[float, float, float]] = kwargs.get(BasicEnvVisualiserProxy.FRAME_DATA, None)
        if all([frame_data is not None, frame_index is not None, isinstance(frame_data, List),
                isinstance(frame_index, int)]):
            self._producer.send(topic=self._topic,
                                value=self._basic_visualiser_env_proxy.update(frame_index=frame_index,
                                                                              frame_data=frame_data))
            self._trace.log(f'Visualisation Agent {self} sent update message for frame {frame_index}')
        else:
            raise ValueError(f'Expected int:{BasicEnvVisualiserProxy.FRAME_INDEX} and \
                             List:{BasicEnvVisualiserProxy.FRAME_DATA} to be passed')
        return

    def terminate(self,
                  **kwargs) -> None:
        """
        Send terminate request to Visualisation service
        """
        _ = self._producer.send(topic=self._topic,
                                value=self._basic_visualiser_env_proxy.terminate())
        self._trace.log(f'Visualisation Agent {self} sent terminate message')
        return
