import numpy as np
import tensorflow as tf
from copy import copy
from typing import Tuple, List, Dict
from python.exceptions.GeneTypeMismatch import GeneTypeMismatch
from python.util.Distribution import Distribution
from python.util.TypeUtil import TypeUtil
from python.base.Gene import Gene
from python.id.GeneId import GeneId


class LayerTypeGene(Gene):
    """
    A Gene that controls the type of the layer to be added.
    """

    _LAYER_TYPES: Dict[str, int] = {
        TypeUtil.module_and_name(tf.keras.layers.Dense): 0,
        TypeUtil.module_and_name(tf.keras.layers.Dropout): 1,
        TypeUtil.module_and_name(tf.keras.layers.Conv1D): 2,
        TypeUtil.module_and_name(tf.keras.layers.Conv2D): 3,
    }
    __VALUE_MIN: int = 0
    __VALUE_MAX: int = len(_LAYER_TYPES)

    def __init__(self,
                 gene_value: Dict[str, np.ndarray] = None,
                 mutation_rate: float = 0.1):

        self._id: GeneId = GeneId()

        if mutation_rate > 1.0 or mutation_rate < 0.0:
            raise ValueError(f'mutation_rate is a probability and must be in range 0.0 to 1.0 - given {mutation_rate}')
        self._mutation_rate: float = mutation_rate

        if gene_value is None:
            gene_value: Dict[type, np.ndarray] = {}

        if not isinstance(gene_value, Dict):
            raise ValueError(
                f'gene_value must be a Dict with key of Keras layer type and numpy array of selection probabilities')

        self._layer_probs: List[np.array] = [None] * self.num_layer_types()
        for layer_type, idx in self._LAYER_TYPES.items():
            selection_probs: np.ndarray = gene_value.get(str(layer_type),
                                                         Distribution.random_distribution(self.__VALUE_MAX))
            if len(selection_probs) != self.num_layer_types():
                raise ValueError(f'Selection probabilities must be same length as the number of layers')
            if np.absolute(np.sum(selection_probs) - 1.0) > 1e-6:
                raise ValueError(f'Selection probabilities must sum to 1.0')

            self._layer_probs[idx] = selection_probs
        return

    @classmethod
    def num_layer_types(cls) -> int:
        return len(cls._LAYER_TYPES)

    @classmethod
    def layer_types(cls) -> List[str]:
        return [str(lt) for lt in cls._LAYER_TYPES.keys()]

    def get_gene_id(self) -> GeneId:
        """
        Get the gene unique identifier
        :return: An gene globally unique id
        """
        return self._id

    def get_diversity(self,
                      comparison_gene: 'LayerTypeGene') -> float:
        """
        Get the diversity of the Gene with respect to the given Gene
        :param comparison_gene: The gene to calculate diversity with respect to.
        :return: The relative diversity
        """
        if not isinstance(self, type(comparison_gene)):
            raise GeneTypeMismatch
        if not self.num_layer_types() != comparison_gene.num_layer_types():
            raise GeneTypeMismatch(f'Number of layers do not match')

        diff = np.zeros(self.num_layer_types())
        for lt, idx in self._LAYER_TYPES.items():
            comp_idx = comparison_gene._LAYER_TYPES.get(lt, None)
            if comp_idx is None:
                raise GeneTypeMismatch(f'Comparison Gene does not contain layer {lt}')
            diff += self._layer_probs[idx] - comparison_gene._layer_probs[comp_idx]
        return np.sum(diff) / self.num_layer_types()

    def mutate(self,
               step_size: float) -> None:
        """
        Make a random mutation to the Gene of step_size
        :param step_size: The size of the mutation to make +/- from current value
        """
        self._depth = Gene.mutate_int(current_value=self._depth,
                                      mutation_rate=self._mutation_rate,
                                      step_size=step_size,
                                      v_min=-1.0,
                                      v_max=+1.0)
        return

    def value(self):
        """
        Return the value of the Gene - the return type is specific to the Gene
        """
        return int(self._depth)

    @classmethod
    def value_range(cls) -> Tuple[int, int]:
        """
        Return the value range of the Gene
        """
        return LayerTypeGene.__VALUE_MIN, LayerTypeGene.__VALUE_MAX

    def __copy__(self):
        """
        Deep copy the gene
        """
        return LayerTypeGene(gene_value=copy(self._depth),
                             mutation_rate=copy(self._mutation_rate))

    def __eq__(self,
               other: Gene):
        """
        Logical equality
        :param other: The other Gene to test equivalence with
        :return: True if this gene is logically equal to the 'other' given gene
        """
        if isinstance(other, LayerTypeGene):
            return self._depth == other._depth
        return False
