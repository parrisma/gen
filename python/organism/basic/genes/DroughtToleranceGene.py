import numpy as np
from copy import copy
from python.exceptions.GeneTypeMismatch import GeneTypeMismatch
from python.base.Gene import Gene
from python.id.GeneId import GeneId


class DroughtToleranceGene(Gene):
    """
    A Gene that controls the tolerance of an organism to wet or dry conditions
    """

    _id: GeneId
    _drought_tolerance: float
    _mutation_rate: float

    def __init__(self,
                 gene_value: float = None,
                 mutation_rate: float = 0.1):

        self._id = GeneId()
        self._mutation_rate = mutation_rate
        # Range is -1 likes wet to +1 likes dry
        #
        if gene_value is None:
            self._drought_tolerance = (np.random.rand() - 0.5) * 2.0
        else:
            if -1.0 <= gene_value <= 1.0:
                self._drought_tolerance = gene_value
            else:
                raise ValueError(f'Drought tolerance must be in range -1.0 to +1.0 but given {gene_value}')
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
        return (self._drought_tolerance - comparison_gene.value()) ** 2

    def mutate(self) -> None:
        """
        Make upto 10% random mutation to the Gene
        """
        r = (np.random.rand() - 0.5) * 2.0
        if r > 1.0:
            r = -r
        self._drought_tolerance += self._drought_tolerance * (r * self._mutation_rate)

    def value(self):
        """
        Return the value of the Gene - the return type is specific to the Gene
        """
        return float(self._drought_tolerance)

    def __copy__(self):
        """
        Deep copy the gene
        """
        return DroughtToleranceGene(gene_value=copy(self._drought_tolerance),
                                    mutation_rate=copy(self._mutation_rate))

    def __eq__(self,
               other: Gene):
        """
        Logical equality
        :param other: The other Gene to test equivalence with
        :return: True if this gene is logically equal to the 'other' given gene
        """
        if isinstance(other, DroughtToleranceGene):
            return self._drought_tolerance == other._drought_tolerance
        return False
