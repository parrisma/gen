import unittest
import numpy as np
from copy import copy
from python.base.Gene import Gene
from python.organism.basic.test.BasicUtilsForTesting import BasicUtilsForTesting
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene
from python.id.EntityId import EntityId
from rltrace.Trace import Trace, LogLevel
from test.UtilsForTesting import UtilsForTesting


class TestBasicGenes(unittest.TestCase):
    _run: int
    _session_id: str = EntityId().as_str()
    _trace: Trace = Trace(log_level=LogLevel.debug, log_dir_name=".", log_file_name="trace.log")

    def __init__(self, *args, **kwargs):
        super(TestBasicGenes, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        cls._trace.log(f'- - - - - - S T A R T - - - - - - \n')
        UtilsForTesting.clean_up_test_files()
        return

    def setUp(self) -> None:
        TestBasicGenes._run += 1
        self._trace.log(f'- - - - - - C A S E {TestBasicGenes._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        self._trace.log(f'- - - - - - C A S E {TestBasicGenes._run} Passed - - - - - -\n')
        return

    @classmethod
    def tearDownClass(cls) -> None:
        cls._trace.log(f'- - - - - - E N D - - - - - - \n')
        UtilsForTesting.clean_up_test_files()
        return

    @BasicUtilsForTesting.test_case
    def testBasicGeneConstruction(self):
        for gene_type in [DroughtToleranceGene, LightToleranceGene]:
            for r in np.random.random_sample(10):
                gene = gene_type(gene_value=r)
                self.assertEqual(r, gene.value())
        return

    @BasicUtilsForTesting.test_case
    def testGeneMutation(self):
        for gene_type in [DroughtToleranceGene, LightToleranceGene]:
            mutation_rate: float = float(np.random.rand())
            for r in np.random.random_sample(1000):
                gene = gene_type(gene_value=r,
                                 mutation_rate=mutation_rate)
                old_value = gene.value()
                step_size = float(np.random.rand())
                gene.mutate(step_size=step_size)
                new_value = gene.value()
                self.assertTrue(
                    (np.absolute(old_value - new_value) - step_size) <= BasicUtilsForTesting.MARGIN_OF_ERROR)
        return

    @BasicUtilsForTesting.test_case
    def testGeneDiversity(self):
        for gene_type in [DroughtToleranceGene, LightToleranceGene]:
            for r1, r2 in np.random.rand(1000, 2):
                gene1 = gene_type(gene_value=r1)
                gene2 = gene_type(gene_value=r2)
                self.assertTrue(gene1.get_diversity(gene2) == (r1 - r2) ** 2)
        return

    @BasicUtilsForTesting.test_case
    def testGeneExceptions(self):

        for gene_type in [DroughtToleranceGene, LightToleranceGene]:
            for v in [-1.001, 1.001]:
                with self.assertRaises(ValueError):
                    _ = gene_type(gene_value=v)
        return

    @BasicUtilsForTesting.test_case
    def testGeneCopy(self):
        dtg = DroughtToleranceGene(gene_value=float(np.random.rand()))
        ltg = LightToleranceGene(gene_value=float(np.random.rand()))

        original_gene: Gene
        copy_gene: Gene
        for original_gene, copy_gene in [[dtg, copy(dtg)], [ltg, copy(ltg)]]:
            self.assertTrue(original_gene == copy_gene)
            self.assertFalse(original_gene.get_gene_id() == copy_gene.get_gene_id())
        return


if __name__ == "__main__":
    unittest.main()
