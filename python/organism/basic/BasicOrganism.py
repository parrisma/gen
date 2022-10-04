from typing import List, Dict, Union, Callable
import numpy as np
from copy import copy
from python.id.OrganismId import OrganismId
from python.base.Organism import Organism
from python.base.Genome import Genome
from python.base.EnvironmentState import EnvironmentState
from python.base.Metrics import Metrics
from python.base.Gene import Gene
from python.organism.basic.BasicMetrics import BasicMetrics
from python.organism.basic.BasicEnvironmentAttributes import BasicEnvironmentAttributes
from python.organism.basic.BasicChromosome import BasicChromosome
from python.organism.basic.BasicGenome import BasicGenome
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from rltrace.Trace import LogLevel
from rltrace.elastic.ElasticTraceBootStrap import ElasticTraceBootStrap


class BasicOrganism(Organism):
    LIGHT_TOLERANCE: str = "LightTolerance"
    DROUGHT_TOLERANCE: str = "DroughtTolerance"

    @classmethod
    def __as_pct(cls,
                 v: float,
                 lim: float):
        """
        Return the given value as a % where lim = 100%
        :param v: The value to be converted to %
        :param lim: The limit that represents 100%
        :return: The value as %
        """
        return np.maximum(0, np.minimum(np.absolute(v), lim)) / lim

    def __init__(self,
                 session_uuid: str,
                 genome: BasicGenome):
        self._id: OrganismId = OrganismId()
        self._trace = ElasticTraceBootStrap(log_level=LogLevel.debug,
                                            session_uuid=session_uuid,
                                            index_name='genetic_simulator').trace
        self._genome: BasicGenome = genome
        self._metrics: BasicMetrics = BasicMetrics(alive=True, fitness=Metrics.LEAST_FIT, diversity=0.0)
        # Express Chromosomes
        chromosome: BasicChromosome = self._genome.get_chromosome(BasicChromosome)  # NOQA
        self._light_tolerance: Gene = chromosome.get_gene(LightToleranceGene)
        self._drought_tolerance: Gene = chromosome.get_gene(DroughtToleranceGene)
        return

    @classmethod
    def light_fitness_func(cls,
                           environment_light_level: float,
                           light_tolerance: float) -> float:
        """
        Calculate fitness as a function of light tolerance and light level
        :param light_tolerance: The genetic driven light tolerance -1.0 to 1.0
        :param environment_light_level: The environment light level 0.0 to 1.0
        :return: The fitness of the organism given its light tolerance and the ambient light levels
        """
        return 1 - np.sin(np.absolute((environment_light_level - ((1 + light_tolerance) / 2))) * (np.pi / 2))

    @classmethod
    def drought_fitness_func(cls,
                             environment_drought_level: float,
                             drought_tolerance: float) -> float:
        """
        Calculate fitness as a function of drought tolerance and light level
        :param drought_tolerance: The genetic driven drought tolerance -1.0 to 1.0
        :param environment_drought_level: The environment drought level 0.0 to 1.0
        :return: The fitness of the organism given its drought tolerance and the drought level
        """
        return 1 - np.power(((1 + drought_tolerance) / 2 - environment_drought_level), 2)

    @classmethod
    def hybrid_fitness_func(cls,
                            environment_light_level: float,
                            environment_drought_level: float,
                            scenario_index: int,
                            **kwargs) -> float:
        """
        Calculate Organism fitness as a function of light tolerance and drought tolerance
        :param environment_light_level: The current environmental light level as a % of 24 hrs
        :param environment_drought_level: The current environmental drought level as a % of 24 hrs
        :param scenario_index: The scenario index for surface rendering
        :param kwargs: Optional arguments for passing organism specific details.
        :return:
        """
        # Extract optional (defaulted) arguments for the calculation.
        light_tol = kwargs.get(BasicOrganism.LIGHT_TOLERANCE, None)
        drought_tol = kwargs.get(BasicOrganism.DROUGHT_TOLERANCE, None)

        if light_tol is None or drought_tol is None:
            raise ValueError("Light and Drought tolerance Parameter scenarios must be passed in kwargs")
        else:
            if isinstance(light_tol, Callable):
                light_tol = light_tol(scenario_index=scenario_index)
            if isinstance(drought_tol, Callable):
                drought_tol = drought_tol(scenario_index=scenario_index)

        light_fitness = BasicOrganism.light_fitness_func(environment_light_level=environment_light_level,
                                                         light_tolerance=light_tol)

        drought_fitness = BasicOrganism.drought_fitness_func(environment_drought_level=environment_drought_level,
                                                             drought_tolerance=drought_tol)

        return (light_fitness + drought_fitness) / 2

    def run(self,
            environment_state: EnvironmentState) -> Organism:
        """
        Execute a life cycle of the organism an update the metrics
        :param environment_state: The current state of the environment in which the organism is living.
        :return: A reference to this (self) Organism after it has executed a life cycle.
        """
        self._trace.log(f'Organism {self._id} run')
        bm: Dict[BasicEnvironmentAttributes, object] = environment_state.get_attributes()  # NOQA

        ave_light = float(bm.get(BasicEnvironmentAttributes.AVG_HOURS_OF_LIGHT_PER_DAY))
        ave_drought = float(bm.get(BasicEnvironmentAttributes.AVG_HOURS_BETWEEN_RAIN))

        kwargs = {BasicOrganism.LIGHT_TOLERANCE: self._light_tolerance.value(),
                  BasicOrganism.DROUGHT_TOLERANCE: self._drought_tolerance.value()}

        fitness: float = BasicOrganism.hybrid_fitness_func(environment_light_level=ave_light,
                                                           environment_drought_level=ave_drought,
                                                           scenario_index=0,
                                                           **kwargs)

        diversity: float = self.get_relative_diversity(bm.get(BasicEnvironmentAttributes.POPULATION))

        self._metrics = BasicMetrics(alive=True,
                                     fitness=fitness,
                                     diversity=diversity)  # TODO

        return self

    def is_alive(self) -> bool:
        """
        Establish if the organism is still alive an operable in the environment
        :return: True, if the organism is alive
        """
        return self._metrics.is_alive()

    def fitness(self) -> float:
        """
        Return a number that represents the fitness of the organism.

        Until the organism has run at least once the fitness will be the value for least-fit.

        :return: Organism fitness expressed as a float.
        """
        return self._metrics.get_fitness()

    def metrics(self) -> Metrics:
        """
        Return the current metrics for the organism

        Until the organism has run at least once the metrics will be default values

        :return: Organism fitness expressed as a float.
        """
        return copy(self._metrics)

    def get_id(self) -> str:
        """
        Get the globally unique id of the Organism
        :return: The organisms globally unique id as string.
        """
        return self._id.as_str()

    def get_relative_diversity(self,
                               comparison_organisms: List['Organism']) -> float:
        """
        Get the diversity of the Organism with respect to the given Organism
        :param comparison_organisms: The Organism to calculate diversity with respect to.
        :return: The relative diversity
        """
        rel_div = list()
        for o in comparison_organisms:
            rel_div.append(self._genome.get_diversity(o.get_genome()))  # NOQA

        return (np.asarray(rel_div).sum()) / len(rel_div)

    def get_genome(self) -> Genome:
        """
        Get the chromosomes of the Organism
        :return: A list of chromosomes
        """
        return self._genome

    def crossover(self,
                  mix_rate: float,
                  organism: 'Organism') -> Genome:
        """
        Based on the mix rate return a list of chromosomes with genes mixed between the Organism and the given
        chromosomes.
        :param mix_rate: The rate of mixing of Genes between the Chromosomes
        :param organism: The organism to cross genes with
        :return: The Genome resulting from the crossover.
        """
        return Genome.cross_genomes(mix_percent=mix_rate,
                                    from_genome=organism.get_genome(),
                                    to_genome=self.get_genome())

    def mutate(self,
               step_size: Union[float, Dict[type, float]]):
        """
        Based on a defined <mutation_rate>. introduce random perturbation into the Organisms populations Genes
        :param step_size: An absolute step size as float to be applied to all gene types ot
        :return: The Genome resulting from the mutation.
        """
        self._genome = Genome.mutate(genome_to_mutate=self.get_genome(), step_size=step_size)

    def __eq__(self, other):
        """
        Test equality between BasicOrganism and a given object
        :param other: Object to check equality with.
        :return: True if BasicOrganism fields match
        Note: This is not an identity check, so we do not compare the id
        """
        if isinstance(other, BasicOrganism):
            if self._genome == other.get_genome():
                if self._light_tolerance == other._light_tolerance:
                    if self._drought_tolerance == other._drought_tolerance:
                        return True
        return False

    def __str__(self) -> str:
        """
        Basic Organism as string
        :return: Organism as String
        """
        return f' BasicOrganism [{self.get_id()}]'

    def __repr__(self, *args, **kwargs) -> str:
        """
        Basic Organism as printable form
        :param args:
        :param kwargs:
        :return: Organism as printable string
        """
        return self.__str__()
