import sys
import argparse
import os
import pickle
from rltrace.Trace import Trace, LogLevel
from rltrace.elastic.ElasticTraceBootStrap import ElasticTraceBootStrap
from kafka import KafkaConsumer, TopicPartition, KafkaProducer
from util.K8Util import K8Util
from util.InvocationHandler import InvocationHandler
from interface.Agent import Agent
from python.id.EntityId import EntityId
from python.interface.Visualiser import Visualiser
from python.organism.basic.BasicEnvVisualiser import BasicEnvVisualiser
from python.visualise.VisualisationAgentProxy import VisualisationAgentProxy


class VisualisationAgent(Agent):
    _verbose: bool
    _config_file: str

    def __init__(self):
        args = self._get_args()

        self._agent_name = f'VisualisationService'
        self._uuid = EntityId().as_str()
        self._log_index = args.log_index
        self._elastic_db_username = args.elastic_db_username
        self._elastic_db_password = args.elastic_db_password
        self._trace = ElasticTraceBootStrap(log_level=LogLevel.debug,
                                            index_name=self._log_index,
                                            elastic_user=self._elastic_db_username,
                                            elastic_password=self._elastic_db_password,
                                            ).trace

        self._topic = args.topic
        self._kafka_kubernetes_service_name: str = args.kafka_kubernetes_service_name
        self._kafka_kubernetes_namespace: str = args.kafka_kubernetes_namespace
        self._kafka_external_port: int = args.kafka_external_port
        self._kafka_group: str = args.kafka_group

        self._kafka_broker_connection_string: str = self._get_kafka_broker()
        self._consumer: KafkaConsumer = self._create_consumer_side()

        self._invocation_handler: InvocationHandler = InvocationHandler(agent=self,
                                                                        consumer=self._consumer,
                                                                        producer=None,  # NOQA
                                                                        request_topic=self._topic,
                                                                        trace=self._trace)

        self._visualiser: Visualiser = BasicEnvVisualiser(trace=self._trace)

        self._terminated: bool = False

        return

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

    @staticmethod
    def _get_args():
        """
        Extract and verify command line arguments
        """
        parser = argparse.ArgumentParser(description='MatPlotLib stand alone process for graph rendering')
        parser.add_argument("-l", "--log_index",
                            help="The name of the elastic DB index to log to",
                            default='visualisation_index',
                            type=str)
        parser.add_argument("-u", "--elastic_db_username",
                            help="The user name for the Elastic DB logging connection",
                            default='elastic',
                            type=str)
        parser.add_argument("-w", "--elastic_db_password",
                            help="The password of the elastic DB logging user",
                            default='changeme',
                            type=str)
        VisualisationAgentProxy.add_args(parser)
        return parser.parse_args()

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

    def _create_consumer_side(self) -> KafkaConsumer:
        consumer = KafkaConsumer(bootstrap_servers=[self._kafka_broker_connection_string],
                                 group_id=self._kafka_group,
                                 auto_offset_reset='latest',
                                 value_deserializer=lambda x: pickle.loads(x))
        self._trace.log(f'Agent {self._agent_name} Consumer created on {self._kafka_broker_connection_string}')
        return consumer

    def _connect_to_topic(self) -> None:
        self._topic_partition = TopicPartition(topic=self._topic,
                                               partition=0)
        self._consumer.assign([self._topic_partition])
        self._trace.log(f'Agent {self._agent_name} listening on {self._topic}')
        return

    def initialise(self, **kwargs) -> None:
        """
        """
        if self._terminated:
            self._trace.log('Cannot initialise as session as already been terminated', level=Trace.LogLevel.warn)
        else:
            self._trace.log('Request to initialise plot received')
            self._visualiser.initialise(**kwargs)
        return

    def update(self, **kwargs) -> None:
        """
        """
        if self._terminated:
            self._trace.log('Cannot update as session as already been terminated', level=Trace.LogLevel.warn)
        else:
            self._trace.log('Request to update plot received')
            self._visualiser.update(**kwargs)
        return

    def terminate(self, **kwargs) -> None:
        """
        """
        if self._terminated:
            self._trace.log('Terminate already requested, this request is ignored', level=Trace.LogLevel.warn)
        else:
            self._trace.log('Request to terminate plot received')
            self._visualiser.terminate(**kwargs)
        return

    def run(self) -> None:
        """
        Initialise the basic plot and wait for updates on Kafka Topic
        """
        self._trace.log(f'Starting Visualisation Agent {self._agent_name} run started')
        self._connect_to_topic()
        self._invocation_handler.process_messages(do_every=self._visualiser.show)
        return


if __name__ == "__main__":
    VisualisationAgent().run()
    sys.exit(0)
