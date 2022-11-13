from python.base.OrganismFactory import OrganismFactory
from python.base.Genome import Genome
from python.base.Organism import Organism
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene
from python.organism.basic.BasicChromosome import BasicChromosome
from python.organism.basic.BasicGenome import BasicGenome
from python.organism.basic.BasicOrganism import BasicOrganism
from rltrace.Trace import Trace


class BasicOrganismFactory(OrganismFactory):
    """
    Create basic Organisms
    """

    def __init__(self,
                 trace: Trace):
        self._trace = trace
        return

    def new(self,
            genome: Genome = None) -> Organism:
        """
        Create a new organism from the given Chromosomes
        :param genome: The Genome to use to create the organism, if None a randomised Genome is used.
        :return: An Organism
        """
        new_organism: Organism = None  # NOQA
        if genome is None:
            new_organism = BasicOrganism(session_uuid=self._trace.session_uuid,
                                         genome=
                                         BasicGenome([BasicChromosome(drought_gene=DroughtToleranceGene(),
                                                                      light_gene=LightToleranceGene())]))
        else:
            new_organism = BasicOrganism(session_uuid=self._trace.session_uuid,
                                         genome=genome)  # NOQA

        return new_organism
