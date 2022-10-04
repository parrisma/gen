import unittest
import numpy as np
from python.base.Genome import Genome
from python.organism.basic.BasicOrganism import BasicOrganism
from python.organism.basic.test.BasicUtilsForTesting import BasicUtilsForTesting
from python.organism.basic.BasicGenome import BasicGenome
from python.organism.basic.BasicChromosome import BasicChromosome
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene
from python.organism.basic.BasicEnvironmentState import BasicEnvironmentState
from python.id.EntityId import EntityId
from rltrace.Trace import Trace, LogLevel
from test.UtilsForTesting import UtilsForTesting


class TestBasicOrganism(unittest.TestCase):
    _run: int = 0
    _session_id: str = EntityId().as_str()
    _trace: Trace = Trace(log_level=LogLevel.debug, log_dir_name=".", log_file_name="trace.log")

    def __init__(self, *args, **kwargs):
        super(TestBasicOrganism, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        cls._trace.log(f'- - - - - - S T A R T - - - - - - \n')
        UtilsForTesting.clean_up_test_files()
        return

    def setUp(self) -> None:
        TestBasicOrganism._run += 1
        self._trace.log(f'- - - - - - C A S E {TestBasicOrganism._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        self._trace.log(f'- - - - - - C A S E {TestBasicOrganism._run} Passed - - - - - -\n')
        return

    @classmethod
    def tearDownClass(cls) -> None:
        cls._trace.log(f'- - - - - - E N D - - - - - - \n')
        UtilsForTesting.clean_up_test_files()
        return

    @BasicUtilsForTesting.test_case
    def testBasicOrganismConstruction(self):
        r1: float = 0.3141
        r2: float = -0.678
        c1 = BasicChromosome(drought_gene=DroughtToleranceGene(r1), light_gene=LightToleranceGene(r2))
        g1 = BasicGenome([c1])
        basic_organism = BasicOrganism(genome=g1, session_uuid=TestBasicOrganism._session_id)
        g2 = basic_organism.get_genome()
        self.assertTrue(g2.get_chromosome(BasicChromosome).get_gene(DroughtToleranceGene).value() == r1)
        self.assertTrue(g2.get_chromosome(BasicChromosome).get_gene(LightToleranceGene).value() == r2)
        return

    @BasicUtilsForTesting.test_case
    def testBasicOrganismDiversity(self):
        r1, r2, r3, r4, r5, r6 = (-1.0, -1.0, 1.0, 1.0, -1.0, 1.0)
        c1 = BasicChromosome(drought_gene=DroughtToleranceGene(r1), light_gene=LightToleranceGene(r2))
        c2 = BasicChromosome(drought_gene=DroughtToleranceGene(r3), light_gene=LightToleranceGene(r4))
        c3 = BasicChromosome(drought_gene=DroughtToleranceGene(r5), light_gene=LightToleranceGene(r6))

        g1 = BasicGenome([c1])
        g2 = BasicGenome([c2])
        g3 = BasicGenome([c3])

        basic_organism1 = BasicOrganism(genome=g1, session_uuid=TestBasicOrganism._session_id)
        basic_organism2 = BasicOrganism(genome=g2, session_uuid=TestBasicOrganism._session_id)
        basic_organism3 = BasicOrganism(genome=g3, session_uuid=TestBasicOrganism._session_id)

        # Diversity w.r.t. self should be zero.
        self.assertTrue(basic_organism1.get_relative_diversity([basic_organism1]) == 0.0)
        self.assertTrue(basic_organism2.get_relative_diversity([basic_organism2]) == 0.0)

        # Max diversity as both genes are opposite in value
        self.assertTrue(basic_organism2.get_relative_diversity([basic_organism1]) == 4.0)
        self.assertTrue(basic_organism1.get_relative_diversity([basic_organism2]) == 4.0)

        # Mid-diversity
        self.assertTrue(basic_organism1.get_relative_diversity([basic_organism3]) == 2.0)
        self.assertTrue(basic_organism2.get_relative_diversity([basic_organism3]) == 2.0)

        return

    @BasicUtilsForTesting.test_case
    def testBasicOrganismCrossOver(self):
        for _ in range(1000):
            r1, r2, r3, r4 = np.random.random(4)
            c1 = BasicChromosome(drought_gene=DroughtToleranceGene(r1), light_gene=LightToleranceGene(r2))
            c2 = BasicChromosome(drought_gene=DroughtToleranceGene(r3), light_gene=LightToleranceGene(r4))

            g1 = BasicGenome([c1])
            g2 = BasicGenome([c2])

            basic_organism1 = BasicOrganism(genome=g1, session_uuid=TestBasicOrganism._session_id)
            basic_organism2 = BasicOrganism(genome=g2, session_uuid=TestBasicOrganism._session_id)

            # Mix rate of 100% guarantees a full swap
            new_organism = BasicOrganism(session_uuid=TestBasicOrganism._session_id,
                                         genome=basic_organism1.crossover(mix_rate=1.0,  # NOQA
                                                                          organism=basic_organism2))  # NOQA
            new_genes = Genome.gene_list(new_organism.get_genome())
            expected_genes = Genome.gene_list(basic_organism2.get_genome())
            self.assertTrue(new_genes == expected_genes)

            # Mix rate of 0% guarantees a zero swap
            new_organism = BasicOrganism(
                session_uuid=TestBasicOrganism._session_id,
                genome=basic_organism1.crossover(mix_rate=0.0, organism=basic_organism2))  # NOQA
            new_genes = Genome.gene_list(new_organism.get_genome())
            expected_genes = Genome.gene_list(basic_organism1.get_genome())  # expect no genes from organism 2
            self.assertTrue(new_genes == expected_genes)

        return

    @BasicUtilsForTesting.test_case
    def testBasicOrganismMutation(self):
        for _ in range(1000):  # repeat a statistically significant number of time.
            for mutation_rate in [1.0, 0.0]:  # Mutation rate of 100% => guarantee , 0% => no mutation
                r1, r2, step_size = np.random.random(3)
                # Test with fixed float step size for all Genes and gene specific step size.
                for ss in [step_size, {DroughtToleranceGene: step_size, LightToleranceGene: step_size}]:
                    c1 = BasicChromosome(drought_gene=DroughtToleranceGene(r1, mutation_rate=mutation_rate),
                                         light_gene=LightToleranceGene(r2, mutation_rate=mutation_rate))
                    g1 = BasicGenome([c1])
                    basic_organism1 = BasicOrganism(genome=g1, session_uuid=TestBasicOrganism._session_id)
                    basic_organism1.mutate(step_size=ss)
                    new_organism = BasicOrganism(session_uuid=TestBasicOrganism._session_id,
                                                 genome=basic_organism1.get_genome())  # NOQA
                    new_genes = Genome.gene_list(new_organism.get_genome())
                    old_genes = Genome.gene_list(basic_organism1.get_genome())
                    expected_genes = dict()
                    for og in old_genes:
                        expected_genes[type(og)] = og.value()
                    for ng in new_genes:
                        if isinstance(ss, dict):
                            self.assertTrue(
                                np.absolute(ng.value() - expected_genes.get(type(ng))) - (
                                        ss.get(type(ng)) * mutation_rate) < BasicUtilsForTesting.MARGIN_OF_ERROR)
                        else:
                            self.assertTrue(
                                np.absolute(ng.value() - expected_genes.get(type(ng))) - (
                                        ss * mutation_rate) < BasicUtilsForTesting.MARGIN_OF_ERROR)

        return

    @BasicUtilsForTesting.test_case
    def testBasicOrganismFitness(self):
        c1 = BasicChromosome(drought_gene=DroughtToleranceGene(0.5, mutation_rate=0.0),
                             light_gene=LightToleranceGene(0.5, mutation_rate=0.0))
        g1 = BasicGenome([c1])
        basic_organism1 = BasicOrganism(genome=g1, session_uuid=TestBasicOrganism._session_id)
        basic_organism1.mutate(step_size=0.0)
        organism = BasicOrganism(genome=basic_organism1.get_genome(),  # NOQA
                                 session_uuid=TestBasicOrganism._session_id)  # NOQA

        env_state = BasicEnvironmentState(avg_hours_of_light_per_day=12,
                                          avg_hours_between_rain=80,
                                          population=[organism])

        organism.run(environment_state=env_state)
        organism.fitness()  # TODO add asserts

        return
