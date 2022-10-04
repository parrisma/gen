import unittest
import numpy as np
from copy import copy
from python.organism.basic.test.BasicUtilsForTesting import BasicUtilsForTesting
from python.organism.basic.test.GeneForTesting import GeneForTesting
from python.organism.basic.BasicChromosome import BasicChromosome
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene
from python.exceptions.NoSuchGeneTypeInChromosome import NoSuchGeneTypeInChromosome
from python.exceptions.NotAGene import NotAGene
from python.exceptions.ChromosomeMissMatch import ChromosomeMissMatch
from python.id.EntityId import EntityId
from rltrace.Trace import Trace, LogLevel
from test.UtilsForTesting import UtilsForTesting


class TestBasicChromosome(unittest.TestCase):
    _run: int
    _session_id: str = EntityId().as_str()
    _trace: Trace = Trace(log_level=LogLevel.debug, log_dir_name=".", log_file_name="trace.log")

    def __init__(self, *args, **kwargs):
        super(TestBasicChromosome, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        cls._trace.log(f'- - - - - - S T A R T - - - - - - \n')
        UtilsForTesting.clean_up_test_files()
        return

    def setUp(self) -> None:
        TestBasicChromosome._run += 1
        self._trace.log(f'- - - - - - C A S E {TestBasicChromosome._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        self._trace.log(f'- - - - - - C A S E {TestBasicChromosome._run} Passed - - - - - -\n')
        return

    @classmethod
    def tearDownClass(cls) -> None:
        cls._trace.log(f'- - - - - - E N D - - - - - - \n')
        UtilsForTesting.clean_up_test_files()
        return
    
    @BasicUtilsForTesting.test_case
    def testBasicChromosomeConstruction(self):
        basic_chromosome = BasicChromosome()
        self.assertTrue(len(str(basic_chromosome.get_chromosome_id())) > 0)
        return

    @BasicUtilsForTesting.test_case
    def testChromosomeGeneComposition(self):
        basic_chromosome = BasicChromosome()
        gene_types = basic_chromosome.get_gene_types()
        BasicUtilsForTesting.test_types(test_case=self,
                                        actual_types=gene_types,
                                        expected_types=[DroughtToleranceGene, LightToleranceGene])
        return

    @BasicUtilsForTesting.test_case
    def testChromosomeGeneConstructor(self):
        dtg = DroughtToleranceGene(.314159)
        ltg = LightToleranceGene(-0.314159)
        basic_chromosome = BasicChromosome(drought_gene=dtg,
                                           light_gene=ltg)

        BasicUtilsForTesting.verify_matching_basic_chromosome_and_genes(test_case=self,
                                                                        basic_chromosome=basic_chromosome,
                                                                        ltg=ltg,
                                                                        dtg=dtg)
        return

    @BasicUtilsForTesting.test_case
    def testChromosomeGeneSetGet(self):
        basic_chromosome = BasicChromosome()
        dtg = DroughtToleranceGene(.314159)
        ltg = LightToleranceGene(-0.314159)

        basic_chromosome.set_gene(dtg)
        basic_chromosome.set_gene(ltg)

        gene_types = basic_chromosome.get_gene_types()
        BasicUtilsForTesting.test_types(test_case=self,
                                        actual_types=gene_types,
                                        expected_types=[DroughtToleranceGene, LightToleranceGene])

        BasicUtilsForTesting.verify_matching_basic_chromosome_and_genes(test_case=self,
                                                                        basic_chromosome=basic_chromosome,
                                                                        ltg=ltg,
                                                                        dtg=dtg)

    @BasicUtilsForTesting.test_case
    def testChromosomeExceptions(self):
        dtg = DroughtToleranceGene(.314159)
        ltg = LightToleranceGene(-0.314159)
        basic_chromosome = BasicChromosome(drought_gene=dtg,
                                           light_gene=ltg)

        with self.assertRaises(NoSuchGeneTypeInChromosome):
            basic_chromosome.get_gene(float)

        with self.assertRaises(NotAGene):
            basic_chromosome.set_gene(float(0.1))  # NOQA

        basic_chromosome2 = BasicChromosome(drought_gene=GeneForTesting(),  # NOQA
                                            light_gene=ltg)
        with self.assertRaises(ChromosomeMissMatch):
            basic_chromosome.get_diversity(basic_chromosome2)

        return

    @BasicUtilsForTesting.test_case
    def testChromosomeDiversity(self):
        for r1, r2, r3, r4 in np.random.rand(1000, 4):
            c1 = BasicChromosome(drought_gene=DroughtToleranceGene(r1), light_gene=LightToleranceGene(r2))
            c2 = BasicChromosome(drought_gene=DroughtToleranceGene(r3), light_gene=LightToleranceGene(r4))
            self.assertTrue(c1.get_diversity(c2) == ((r1 - r3) ** 2 + (r2 - r4) ** 2) / 2.0)

            return

    @BasicUtilsForTesting.test_case
    def testChromosomeCopy(self):
        dtg = DroughtToleranceGene(.314159)
        ltg = LightToleranceGene(-0.314159)
        basic_chromosome = BasicChromosome(drought_gene=dtg,
                                           light_gene=ltg)
        basic_chromosome_copy = copy(basic_chromosome)
        self.assertTrue(basic_chromosome == basic_chromosome_copy)
        self.assertFalse(basic_chromosome.get_chromosome_id() == basic_chromosome_copy.get_chromosome_id())
        self.assertFalse(
            basic_chromosome.get_gene(DroughtToleranceGene).get_gene_id() == basic_chromosome_copy.get_gene(
                DroughtToleranceGene).get_gene_id())
        self.assertFalse(
            basic_chromosome.get_gene(LightToleranceGene).get_gene_id() == basic_chromosome_copy.get_gene(
                LightToleranceGene).get_gene_id())

        return


if __name__ == "__main__":
    unittest.main()
