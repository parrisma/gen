import sys
import os
from time import sleep
from typing import Dict
from json import loads, dumps
from kafka import KafkaConsumer, TopicPartition, KafkaProducer
from python.main.BaseArgParser import BaseArgParser
from util.K8Util import K8Util


class KafkaAgent:
    def __init__(self):
        args = self._get_args()
        self._initiator: bool = args.initiator
        self._kafka_kubernetes_service_name: str = args.kafka_kubernetes_service_name
        self._kafka_kubernetes_namespace: str = args.kafka_kubernetes_namespace
        self._kafka_external_port: int = args.kafka_external_port
        self._topic_1: str = args.topic_1
        self._topic_2: str = args.topic_2
        self._kafka_group: str = args.kafka_group

        if self._initiator:
            self._listen_topic = self._topic_1
            self._command_topic = self._topic_2
            self._agent_name = 'Initiator'
        else:
            self._listen_topic = self._topic_2
            self._command_topic = self._topic_1
            self._agent_name = 'Responder'

        self._kafka_broker_connection_string: str = self._get_kafka_broker()

        self._consumer: KafkaConsumer = self._create_consumer_side()
        self._producer: KafkaProducer = self._create_producer_side()

        self._topic_partition: TopicPartition = None  # NOQA

        self._value: int = 0

        return

    def run(self) -> None:
        print(f'Agent {self._agent_name} run started')
        self._connect_to_topic()
        if self._initiator:
            self._send_next_value()
        while True:
            self._consumer.seek_to_end()
            for message in self._consumer:
                print(f'Agent {self._agent_name} received message {message}')
                self._update_value(msg_as_json=message.value)
                self._send_next_value()
                sleep(2)

    def _update_value(self,
                      msg_as_json: Dict) -> None:
        value = msg_as_json['number']
        self._value = value
        print(f'Agent {self._agent_name} updated with value {value}')
        return

    def _send_next_value(self):
        print(f'Agent {self._agent_name} update value {self._value} -> {self._value + 1}')
        self._value += 1
        data = {'number': self._value}
        self._producer.send(self._command_topic, value=data)
        print(f'Agent {self._agent_name} sent  value {self._value} to {self._command_topic}')
        self._producer.flush()
        return

    def _create_producer_side(self) -> KafkaProducer:
        producer = KafkaProducer(bootstrap_servers=[self._kafka_broker_connection_string],
                                 value_serializer=lambda x:
                                 dumps(x).encode('utf-8'))
        print(f'Agent {self._agent_name} Producer created on {self._kafka_broker_connection_string}')
        return producer

    def _create_consumer_side(self) -> KafkaConsumer:
        consumer = KafkaConsumer(bootstrap_servers=[self._kafka_broker_connection_string],
                                 group_id=self._kafka_group,
                                 auto_offset_reset='latest',
                                 value_deserializer=lambda x: loads(x.decode('utf-8')))
        print(f'Agent {self._agent_name} Consumer created on {self._kafka_broker_connection_string}')
        return consumer

    def _connect_to_topic(self) -> None:
        self._topic_partition = TopicPartition(topic=self._listen_topic,
                                               partition=0)
        self._consumer.assign([self._topic_partition])
        print(f'Agent {self._agent_name} listening on {self._listen_topic}')
        return

    def _get_kafka_broker(self) -> str:
        """
        The Kafka broker is reached at the current host on the kubernetes NodePort defined by the
        kubernetes service that exposes Kafka from inside the deployment
        :return: the Kafka Broker host and port as a connection string
        """
        hostname = os.getenv('COMPUTERNAME')
        if len(hostname) == 0:
            raise RuntimeError('Unable to establish the name of the host where this is running')
        node_port_id = K8Util.get_node_port_number(namespace=self._kafka_kubernetes_namespace,
                                                   service_name=self._kafka_kubernetes_service_name,
                                                   port_id=self._kafka_external_port)
        if node_port_id is None:
            raise RuntimeError(f'Unable to establish NodePort defined by {self._kafka_kubernetes_service_name}')
        return f'{hostname}:{node_port_id}'

    @classmethod
    def _get_args(cls):
        """
        Extract and verify command line arguments
        """
        parser = BaseArgParser("Kafka Test Agent").parser()
        parser.add_argument("-i", "--initiator",
                            help="This agent initiates the dialog",
                            default=False,
                            type=bool)
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
        parser.add_argument("-t1", "--topic_1",
                            help="The topic 1",
                            default="KafkaAgentTopic1",
                            type=str)
        parser.add_argument("-t2", "--topic_2",
                            help="The topic 2",
                            default="KafkaAgentTopic2",
                            type=str)
        parser.add_argument("-g", "--kafka_group",
                            help="The Kafka consumer group for the Agents to operate as part of",
                            default="KafkaAgentGroup",
                            type=str)
        return parser.parse_args()


if __name__ == "__main__":
    KafkaAgent().run()
    sys.exit(0)
