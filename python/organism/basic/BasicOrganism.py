from typing import List
from python.id.OrganismId import OrganismId
from python.base.Organism import Organism
from python.base.Chromosome import Chromosome
from python.base.EnvironmentState import EnvironmentState
from python.organism.basic.BasicMetrics import BasicMetrics
from python.organism.basic.BasicChromosome import BasicChromosome
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene


class BasicOrganism(Organism):
    _id: OrganismId
    _chromosomes: List[BasicChromosome]
    _metrics: BasicMetrics
    _light_tolerance: float
    _drought_tolerance: float

    def __init__(self):
        self._id = OrganismId()
        self._chromosomes = [BasicChromosome()]
        self._metrics = BasicMetrics(self.get_id())
        # Express Chromosomes
        for chromosome in self._chromosomes:
            if isinstance(chromosome, BasicChromosome):
                self._light_tolerance = chromosome.get_gene(LightToleranceGene).value()
                self._drought_tolerance = chromosome.get_gene(DroughtToleranceGene).value()
        return

    def __call__(self, *args, **kwargs):
        # return self.run()
        # ToDo
        return

    def run(self,
            environment_state: EnvironmentState) -> Organism:
        self._metrics.set_alive(False)
        return self

    def is_alive(self) -> bool:
        """
        Establish if the organism is still alive an operable in the environment
        :return: True, if the organism is alive
        """
        return self._metrics.is_alive()

    def get_id(self) -> str:
        return self._id.as_str()

    def get_relative_diversity(self,
                               comparison_organism: List['Organism']) -> float:
        """
        Get the diversity of the Organism with respect to the given Organism
        :param comparison_organism: The Organism to calculate diversity with respect to.
        :return: The relative diversity
        """

        raise NotImplementedError

    def get_genome(self) -> List[Chromosome]:
        """
        Get the chromosomes of the Organism
        :return: A list of chromosomes
        """
        return self._chromosomes

    def crossover(self,
                  mix_rate: float,
                  organism: 'BasicOrganism') -> List[Chromosome]:
        """
        Based on the mix rate return a list of chromosomes with genes mixed between the Organism and the given
        chromosomes.
        :param mix_rate: The rate of mixing of Genes between the Chromosomes
        :param organism: The organism to cross with
        :return: The Chromosomes resulting from the crossover.
        """
        raise NotImplementedError

    def mutate(self,
               mutation_rate: float) -> List[Chromosome]:
        """
        Based on a defined <mutation_rate>. introduce random perturbation into the Organisms populations Genes
        :param mutation_rate: The rate at which Genes are affected by random perturbations
        :return: The Chromosomes resulting from the mutation.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.get_id()

    def __repr__(self, *args, **kwargs) -> str:
        return self.__str__()
