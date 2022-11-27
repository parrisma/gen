from copy import copy
from typing import Tuple
from python.exceptions.GeneTypeMismatch import GeneTypeMismatch
from python.base.Gene import Gene
from python.id.GeneId import GeneId


class DepthGene(Gene):
    """
    A Gene that controls the total number of layers in the network (excluding the input and output layers)
    """

    __VALUE_MIN: int = 1
    __VALUE_MAX: int = 10

    def __init__(self,
                 gene_value: int = None,
                 mutation_rate: float = 0.1):

        self._id: GeneId = GeneId()

        if mutation_rate > 1.0 or mutation_rate < 0.0:
            raise ValueError(f'mutation_rate is a probability and must be in range 0.0 to 1.0 - given {mutation_rate}')
        self._mutation_rate: float = mutation_rate

        self._depth: int = DepthGene.__VALUE_MIN
        if gene_value is not None:
            if self.__VALUE_MIN <= gene_value <= self.__VALUE_MAX:
                self._depth = gene_value
            else:
                raise ValueError(
                    f'Network depth  must be in range {self.__VALUE_MIN} to {self.__VALUE_MAX} given {gene_value}')
        return

    def get_gene_id(self) -> GeneId:
        """
        Get the gene unique identifier
        :return: An gene globally unique id
        """
        return self._id

    def get_diversity(self,
                      comparison_gene: 'Gene') -> float:
        """
        Get the diversity of the Gene with respect to the given Gene
        :param comparison_gene: The gene to calculate diversity with respect to.
        :return: The relative diversity
        """
        if not isinstance(self, type(comparison_gene)):
            raise GeneTypeMismatch
        return (self._depth - comparison_gene.value()) ** 2

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
    def value_range(cls) -> Tuple[float, float]:
        """
        Return the value range of the Gene
        """
        return DepthGene.__VALUE_MIN, DepthGene.__VALUE_MAX

    def __copy__(self):
        """
        Deep copy the gene
        """
        return DepthGene(gene_value=copy(self._depth),
                         mutation_rate=copy(self._mutation_rate))

    def __eq__(self,
               other: Gene):
        """
        Logical equality
        :param other: The other Gene to test equivalence with
        :return: True if this gene is logically equal to the 'other' given gene
        """
        if isinstance(other, DepthGene):
            return self._depth == other._depth
        return False
