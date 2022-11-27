from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np
from python.id.GeneId import GeneId


class Gene(ABC):
    """
    A means to influence the expression of given characteristic(s) of an Organism.
    """

    @abstractmethod
    def get_gene_id(self) -> GeneId:
        """
        Get the gene unique identifier
        :return: An gene globally unique id
        """
        raise NotImplementedError

    @abstractmethod
    def get_diversity(self,
                      comparison_gene: 'Gene') -> float:
        """
        Get the diversity of the Gene with respect to the given Gene
        :param comparison_gene: The gene to calculate diversity with respect to.
        :return: The relative diversity
        """
        raise NotImplementedError

    @abstractmethod
    def mutate(self,
               step_size: float) -> None:
        """
        Make a random mutation to the Gene
        :param step_size: The size of the mutation to make +/- from current value
        """
        raise NotImplementedError

    @abstractmethod
    def value(self, **kwargs):
        """
        Return the value of the Gene - the return type is specific to the Gene
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def value_range(cls) -> Tuple[float, float]:
        """
        Return the value range of the Gene
        """
        raise NotImplementedError

    @abstractmethod
    def __copy__(self):
        """
        Deep copy the gene
        """
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        """
        Logical equality
        :param other: The other Gene to test equivalence with
        :return: True if this gene is logically equal to the 'other' given gene
        """
        raise NotImplementedError

    @classmethod
    def mutate_float(cls,
                     current_value: float,
                     mutation_rate: float,
                     step_size: float,
                     v_min: float = 0.0,
                     v_max: float = 1.0) -> float:
        """
        Mutate the current value randomly by + or - the step size
        :param current_value: The value to be mutates
        :param mutation_rate: The probability of a mutation happening as a result of this call
        :param step_size: The step size of the mutation
        :param v_min: Clip the mutated value at this lower bound
        :param v_max: Clip the mutated value at this upper bound
        :return: the value after the mutation
        """
        new_value: float = current_value
        if np.random.rand() <= mutation_rate:
            if np.random.rand() > 0.5:
                new_value += step_size
            else:
                new_value -= step_size

        return np.minimum(v_max, np.maximum(v_min, new_value))

    @classmethod
    def mutate_int(cls,
                   current_value: int,
                   mutation_rate: float,
                   step_size: float,
                   v_min: int,
                   v_max: int) -> int:
        """
        Mutate the current value randomly by + or - the step size
        :param current_value: The value to be mutated
        :param mutation_rate: The probability of a mutation happening as a result of this call
        :param step_size: The step size of the mutation
        :param v_min: Clip the mutated value at this lower bound
        :param v_max: Clip the mutated value at this upper bound
        :return: the value after the mutation
        """
        new_value: int = current_value
        if np.random.rand() <= mutation_rate:
            if np.random.rand() > 0.5:
                new_value += step_size
            else:
                new_value -= step_size

        return int(np.floor(np.minimum(v_max, np.maximum(v_min, new_value))))
