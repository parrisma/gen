from typing import Callable, Dict, Union, List
from python.id.EntityId import EntityId


class InvocationHandler:
    _method_name: str = 'method_name'
    _method_args: str = 'method_args'
    _invocation_id: str = 'invocation_id'

    _invocations: Dict[str, Dict] = {}

    @staticmethod
    def call(o: object,
             command: Dict):
        res = None
        try:
            if InvocationHandler._method_name in command:
                method = o.__getattribute__(command[InvocationHandler._method_name])
                if method is not None and isinstance(method, Callable):
                    args = {}
                    if InvocationHandler._method_args in command:
                        args = command[InvocationHandler._method_args]
                        print(f'calling method {str(method)}')
                        res = method(**args)
                else:
                    raise RuntimeError(
                        f'Method {InvocationHandler._method_name} does not exist or is not callable for {str(o)}')
            else:
                raise RuntimeError(f'Missing {InvocationHandler._method_name} element in command dictionary')
        except Exception as e:
            print(f'Failed to invoke method on object {str(o)} with error {str(e)}')
        return res

    @staticmethod
    def method_and_args_as_dict(method_name: str,
                                args: Union[List, Dict]) -> Dict:
        res: Dict = {InvocationHandler._method_name: method_name,
                     InvocationHandler._invocation_id: EntityId().as_str()}
        if isinstance(args, Dict):
            res[InvocationHandler._method_args] = args
        elif isinstance(args, List):
            res[InvocationHandler._method_args] = {args[i]: args[i + 1] for i in range(0, len(args), 2)}
        else:
            raise RuntimeError(f'args for method must be passed as List or Dict but given {type(args)}')
        InvocationHandler._invocations[res[InvocationHandler._invocation_id]] = res
        return res
