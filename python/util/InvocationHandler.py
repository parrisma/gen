import time
from typing import Dict, Union, List, Callable, Any
from python.id.EntityId import EntityId
from python.exceptions.MessageStructureException import MessageStructureException
from python.exceptions.MessageOriginException import MessageOriginException
from kafka import KafkaConsumer, KafkaProducer
from interface.Agent import Agent
import Trace


class InvocationHandler:
    _method_name: str = 'method_name'
    _method_args: str = 'method_args'
    _is_new_request: str = 'is_new_request'
    _invocation_id: str = 'invocation_id'
    response_id: str = 'response_id'

    _invocations: Dict[str, Dict]
    _bool: Dict = {'true': True, 'false': False, '1': True, '0': False}

    def __init__(self,
                 agent: Agent,
                 consumer: KafkaConsumer,
                 producer: KafkaProducer,
                 request_topic: str,
                 trace: Trace,
                 pause_between_polls: int = 250,
                 max_messages_per_poll=100):
        """
        :param agent: The agent that will process the messages
        :param consumer: The Kafka consumer
        :param producer: The Kafka Producer
        :param request_topic: The Kafka Topic to listen for commands on
        :param pause_between_polls: Time in ms to wait between poll for new messages
        :param max_messages_per_poll: The max messages to process at once.
        """
        self._trace: Trace = trace
        self._invocations = {}
        self._agent = agent
        self._consumer = consumer
        self._producer = producer
        self._request_topic = request_topic
        self._pause_between_polls = pause_between_polls
        self._max_messages_per_poll = max_messages_per_poll
        return

    def handle_message(self,
                       command: Dict) -> Any:
        """
        Process a received message (command)
        :return: The result from calling the handler method on the agent
        """
        invocation_id = command.get(InvocationHandler._invocation_id, None)
        if invocation_id is None:
            raise MessageStructureException(f'Message missing required field {InvocationHandler._invocation_id}')

        is_new_request = command.get(InvocationHandler._is_new_request, None)
        if is_new_request is not None:
            if isinstance(is_new_request, str):
                is_new_request = self._bool.get(is_new_request.lower(), None)
        if is_new_request is None:
            raise MessageStructureException(f'Message missing required field {InvocationHandler._is_new_request}')

        if not is_new_request:
            if invocation_id not in self._invocations:
                raise MessageOriginException(f'Message {invocation_id} was not sent by this process')
            else:
                self._invocations.pop(invocation_id)
                self._trace.log(f'Received response for request id {invocation_id}')

        method_name = command.get(InvocationHandler._method_name, None)
        if method_name is None:
            raise MessageStructureException(f'Message missing required field {InvocationHandler._method_name}')
        method = self._agent.__getattribute__(command[InvocationHandler._method_name])
        if method is None:
            raise ValueError(f'Object {str(self._agent)} has no handler method {method_name}')

        args = command.get(InvocationHandler._method_args, None)
        if args is None:
            raise MessageStructureException(f'Message missing required field {InvocationHandler._method_args}')
        if is_new_request:
            args[InvocationHandler.response_id] = invocation_id

        res = None
        try:
            self._trace.log(f'>>Start<< handler method {str(method_name)}')
            res = method(**args)
            self._trace.log(f'<<End>> handler method {str(method_name)}')
        except Exception as e:
            self._trace.log(f'Failed to invoke method on object {str(self._agent)} with error {str(e)}')
        return res

    def _method_and_args_as_dict(self,
                                 method_name: str,
                                 args: Union[List, Dict],
                                 is_new_request: bool,
                                 response_id: str = "") -> Dict:
        """
        Compose a message/command
        :param method_name: The name of the method to invoke on the receiving agent
        :param args: The arguments to pass to the method, Lists are converted to Dict
        :param is_new_request: Is this a new request or a response to a request
        :param response_id: The globally unique Id to sure to correlate for response.
        :return: Fully formed request as a dictionary
        """
        request_id: str
        if is_new_request:
            request_id = EntityId().as_str()
        else:
            if response_id is None or len(response_id) == 0:
                ValueError("Response Id must be a UUID, but None or empty string passed")
            request_id = response_id

        res: Dict = {InvocationHandler._method_name: method_name,
                     InvocationHandler._invocation_id: request_id,
                     InvocationHandler._is_new_request: str(is_new_request)}
        if isinstance(args, Dict):
            res[InvocationHandler._method_args] = args
        elif isinstance(args, List):
            res[InvocationHandler._method_args] = {args[i]: args[i + 1] for i in range(0, len(args), 2)}
        else:
            raise RuntimeError(f'args for method must be passed as List or Dict but given {type(args)}')
        self._invocations[res[InvocationHandler._invocation_id]] = res
        return res

    def _send(self,
              remote_method_handler: Union[Callable, str],
              remote_method_args: Dict,
              is_new_request: bool,
              response_id: str = "") -> None:
        """
        Push given message to given topic
        :param remote_method_handler: The method id to invoke in receiver
        :param remote_method_args: The args to pass to method
        :param is_new_request: Is this a new request or a response to a request
        :param response_id: The globally unique Id to sure to correlate for response.
        """
        if self._producer is None:
            self._trace.log('***WARNING, nothing sent -  as producer was passed as NONE')
            return

        send_type: str = "response"
        if is_new_request:
            send_type = "request"

        if isinstance(remote_method_handler, Callable):
            remote_method_handler_name = getattr(remote_method_handler, '__name__', repr(remote_method_handler))
        elif isinstance(remote_method_handler, str):
            remote_method_handler_name = remote_method_handler
        else:
            raise ValueError(f'remote_method_handler must be Callable or str, but given {type(remote_method_handler)}')

        data = self._method_and_args_as_dict(method_name=remote_method_handler_name,
                                             args=remote_method_args,
                                             is_new_request=is_new_request,
                                             response_id=response_id)
        self._producer.send(self._request_topic, value=data)
        self._trace.log(
            f'Agent {self._agent.name()} sent {send_type} to {self._request_topic} with response id {response_id}')
        self._producer.flush()
        return

    def send_request(self,
                     remote_method_handler: Union[Callable, str],
                     remote_method_args: Dict) -> None:
        """
        Send a new request
        :param remote_method_handler: The remote method to invoke as handler
        :param remote_method_args: The args to pass to remote method
        :return:
        """
        self._send(remote_method_handler=remote_method_handler,
                   remote_method_args=remote_method_args,
                   is_new_request=True,
                   response_id=EntityId().as_str())
        return

    def send_response(self,
                      remote_method_handler: Union[Callable, str],
                      remote_method_args: Dict,
                      response_id: str) -> None:
        """
        Send a reply to a request
        :param remote_method_handler: The remote method to invoke as handle
        :param remote_method_args: The args to pass to remote method
        :param response_id: The globally unique id being responded to
        """
        self._send(remote_method_handler=remote_method_handler,
                   remote_method_args=remote_method_args,
                   is_new_request=False,
                   response_id=response_id)
        return

    def process_messages(self,
                         cycle_pause_time: int = .25,
                         do_every: callable = None) -> None:
        """
        Process in-coming messages
        :param cycle_pause_time: Time to pause between polls to Kafka
        :param do_every: A client method to invoke every time a message is processed.
        """
        self._consumer.seek_to_end()
        for _ in range(100):
            while True:
                update = self._consumer.poll(timeout_ms=self._pause_between_polls,
                                             max_records=self._max_messages_per_poll)
                if update:
                    for messages in update.values():
                        for message in messages:
                            self._trace.log(f'Agent {self._agent.name()} received message {message}')
                            self.handle_message(command=message.value)  # NOQA
                            if do_every:
                                do_every()
                else:
                    time.sleep(cycle_pause_time)
                    if do_every:
                        do_every()
        return
