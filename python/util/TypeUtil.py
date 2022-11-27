from typing import Tuple, Union
import re


class TypeUtil:
    @classmethod
    def module_and_name(cls,
                        klass: type,
                        contains: Union[Tuple[str], str] = None) -> str:
        """
        Get the full module and class name of the given type
        :param klass: The Class to return the module and name for
        :param contains: Raise ValueError if module and name string do not contain the given string or strings
        :return: A concatenated string of module and class name
        """

        if contains is None:
            contains = tuple()
        if isinstance(contains, str):
            contains = tuple([contains])
        if not isinstance(contains, Tuple):
            raise ValueError('contains param must be a string or tuple of strings')

        res = f'{klass.__module__}.{klass.__name__}'
        for s in contains:
            if not isinstance(s, str):
                raise ValueError('contains param must be a tuple of strings')
            if not re.match(f'.*{s}.*', res):
                raise ValueError(f'{res} does not contain required element {s}')

        return res
