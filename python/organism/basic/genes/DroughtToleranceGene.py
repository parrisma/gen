import numpy as np
from python.exceptions.GeneTypeMismatch import GeneTypeMismatch
from python.base.Gene import Gene
from python.id.GeneId import GeneId


class DroughtToleranceGene(Gene):
    """
    A Gene that controls the tolerance of an organism to wet or dry conditions
    """

    _id: GeneId
    _drought_tolerance: float

    def __init__(self,
                 gene_value: float = None):

        self._id = GeneId()
        # Range is -1 likes wet to +1 likes dry
        #
        if gene_value is None:
            self._drought_tolerance = (np.random.random(1) * 2) - 1
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
        return (self._drought_tolerance - comparison_gene.value()) ^ 2

    def mutate(self) -> None:
        """
        Make a 10% random mutation to the Gene
        """
        self._drought_tolerance = self._drought_tolerance + ((np.random.random(1) * .2) - .1)

    def value(self):
        """
        Return the value of the Gene - the return type is specific to the Gene
        """
        return float(self._drought_tolerance)

    def __eq__(self, other):
        if isinstance(other, DroughtToleranceGene):
            return self._drought_tolerance == other._drought_tolerance
        return False
