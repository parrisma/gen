from python.base.Gene import Gene
from python.id.GeneId import GeneId


class GeneForTesting(Gene):
    """
    A Gene Type Just for testing.
    """

    def __init__(self):
        pass

    def get_gene_id(self) -> GeneId:
        """
        Get the gene unique identifier
        :return: An gene globally unique id
        """
        raise NotImplementedError

    def get_diversity(self,
                      comparison_gene: 'Gene') -> float:
        """
        Get the diversity of the Gene with respect to the given Gene
        :param comparison_gene: The gene to calculate diversity with respect to.
        :return: The relative diversity
        """
        raise NotImplementedError

    def mutate(self,
               step_size: float) -> None:
        """
        Make a random mutation to the Gene
        :param step_size: The size of the mutation to make +/- from current value
        """
        raise NotImplementedError

    def value(self):
        """
        Return the value of the Gene - the return type is specific to the Gene
        """
        raise NotImplementedError

    def __copy__(self):
        """
        Deep copy the gene
        """
        return GeneForTesting()

    def __eq__(self,
               other: Gene):
        """
        Logical equality
        :param other: The other Gene to test equivalence with
        :return: True if this gene is logically equal to the 'other' given gene
        """
        if isinstance(other, GeneForTesting):
            return True
        return False
