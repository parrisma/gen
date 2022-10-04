from time import sleep
from typing import Dict, Union, List, Callable
from python.id.EntityId import EntityId
from python.exceptions.MessageStructureException import MessageStructureException
from python.exceptions.MessageOriginException import MessageOriginException
from kafka import KafkaConsumer, TopicPartition, KafkaProducer
from Interface.Agent import Agent


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
                 request_topic: str):
        self._invocations = {}
        self._agent = agent
        self._consumer = consumer
        self._producer = producer
        self._request_topic = request_topic
        return

    def handle_message(self,
                       agent: Agent,
                       command: Dict):

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
                print(f'Received response for request id {invocation_id}')

        method_name = command.get(InvocationHandler._method_name, None)
        if method_name is None:
            raise MessageStructureException(f'Message missing required field {InvocationHandler._method_name}')
        method = agent.__getattribute__(command[InvocationHandler._method_name])
        if method is None:
            raise ValueError(f'Object {str(agent)} has no handler method {method_name}')

        args = command.get(InvocationHandler._method_args, None)
        if args is None:
            raise MessageStructureException(f'Message missing required field {InvocationHandler._method_args}')
        if is_new_request:
            args[InvocationHandler.response_id] = invocation_id

        res = None
        try:
            print(f'>>Start<< handler method {str(method_name)}')
            res = method(**args)
            print(f'<<End>> handler method {str(method_name)}')
        except Exception as e:
            print(f'Failed to invoke method on object {str(agent)} with error {str(e)}')
        return res

    def _method_and_args_as_dict(self,
                                 method_name: str,
                                 args: Union[List, Dict],
                                 is_new_request: bool,
                                 response_id: str = "") -> Dict:
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
        print(
            f'Agent {self._agent.name()} sent {send_type} to {self._request_topic} with response id {response_id}')
        self._producer.flush()
        return

    def send_request(self,
                     remote_method_handler: Union[Callable, str],
                     remote_method_args: Dict) -> None:
        self._send(remote_method_handler=remote_method_handler,
                   remote_method_args=remote_method_args,
                   is_new_request=True,
                   response_id=EntityId().as_str())
        return

    def send_response(self,
                      remote_method_handler: Union[Callable, str],
                      remote_method_args: Dict,
                      response_id: str) -> None:
        self._send(remote_method_handler=remote_method_handler,
                   remote_method_args=remote_method_args,
                   is_new_request=False,
                   response_id=response_id)
        return

    def process_messages(self,
                         cycle_pause_time: int = 1) -> None:
        self._consumer.seek_to_end()
        for _ in range(100):
            for message in self._consumer:
                print(f'Agent {self._agent.name()} received message {message}')
                self.handle_message(agent=self._agent, command=message.value)  # NOQA
                sleep(cycle_pause_time)
        return
