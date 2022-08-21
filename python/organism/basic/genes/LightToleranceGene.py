import numpy as np
from typing import Tuple
from python.exceptions.GeneTypeMismatch import GeneTypeMismatch
from python.base.Gene import Gene
from python.id.GeneId import GeneId


class LightToleranceGene(Gene):
    """
    A Gene that controls the tolerance of an organism to bright or dark conditions
    """

    __VALUE_MIN: float = -1.0
    __VALUE_MAX: float = +1.0

    def __init__(self,
                 gene_value: float = None,
                 mutation_rate: float = 0.2):

        self._id: GeneId = GeneId()

        if mutation_rate > 1.0 or mutation_rate < 0.0:
            raise ValueError(f'mutation_rate is a probability and must be in range 0.0 to 1.0 - given {mutation_rate}')
        self._mutation_rate: float = mutation_rate

        # Range is -1 likes dark to +1 likes light
        #
        self._light_tolerance: float = 0
        if gene_value is None:
            self._light_tolerance = (np.random.rand() - 0.5) * 2.0
        else:
            if self.__VALUE_MIN <= gene_value <= self.__VALUE_MAX:
                self._light_tolerance = gene_value
            else:
                raise ValueError(
                    f'Light tolerance must be range {self.__VALUE_MIN} to {self.__VALUE_MAX} but {gene_value}')
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
        return (self._light_tolerance - comparison_gene.value()) ** 2

    def mutate(self,
               step_size: float) -> None:
        """
        Make upto 10% random mutation to the Gene
        :param step_size: The size of the mutation to make +/- from current value
        """
        self._light_tolerance = Gene.mutate_float(current_value=self._light_tolerance,
                                                  mutation_rate=self._mutation_rate,
                                                  step_size=step_size,
                                                  v_min=-1.0,
                                                  v_max=+1.0)
        return

    def value(self):
        """
        Return the value of the Gene - the return type is specific to the Gene
        """
        return float(self._light_tolerance)

    @classmethod
    def value_range(cls) -> Tuple[float, float]:
        """
        Return the value range of the Gene
        """
        return LightToleranceGene.__VALUE_MIN, LightToleranceGene.__VALUE_MAX

    def type(self) -> str:
        """
        Return the type of the Gene
        """
        return self.__class__.__name__

    def __copy__(self):
        """
        Deep copy the gene
        """
        return LightToleranceGene(gene_value=self._light_tolerance,
                                  mutation_rate=self._mutation_rate)

    def __eq__(self,
               other: Gene):
        """
        Logical equality
        :param other: The other Gene to test equivalence with
        :return: True if this gene is logically equal to the 'other' given gene
        """
        if isinstance(other, LightToleranceGene):
            return self._light_tolerance == other._light_tolerance
        return False
