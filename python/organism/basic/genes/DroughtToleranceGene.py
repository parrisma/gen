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

    def __init__(self):
        self._id = GeneId()

        # Range is -1 likes wet to +1 likes dry
        #
        self._drought_tolerance = (np.random.random(1) * 2) - 1
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
        if self.type() is not comparison_gene.type():
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

    def type(self) -> str:
        """
        Return the type of the Gene
        """
        return self.__class__.__name__
