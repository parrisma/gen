from python.base.Chromosome import Chromosome


class NotAChromosome(Exception):
    _offending_type: type

    def __init__(self, offending_type: type):
        """
        Raised when a type is used as if it were a Chromosome when it is not
        :param offending_type: The type that was used is if it were a Chromosome
        """
        self._offending_type = offending_type
        actual: str = str(self._offending_type)
        expected = str(type(Chromosome))
        message: str = f'f{actual} is not an instance of {expected}'
        super().__init__(message)
