import unittest
import numpy as np
from python.organism.basic.test.TestUtil import TestUtil
from python.organism.basic.BasicChromosome import BasicChromosome
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene
from python.exceptions.NoSuchGeneTypeInChromosome import NoSuchGeneTypeInChromosome
from python.exceptions.NotAGene import NotAGene


class TestBasicGenes(unittest.TestCase):
    _run: int

    def __init__(self, *args, **kwargs):
        super(TestBasicGenes, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        return

    def setUp(self) -> None:
        TestBasicGenes._run += 1
        print(f'- - - - - - C A S E {TestBasicGenes._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        print(f'- - - - - - C A S E {TestBasicGenes._run} Passed - - - - - -\n')
        return

    @TestUtil.test_case
    def testBasicGeneConstruction(self):
        for gene_type in [DroughtToleranceGene, LightToleranceGene]:
            for r in np.random.random_sample(10):
                gene = gene_type(gene_value=r)
                self.assertEqual(r, gene.value())
        return

    @TestUtil.test_case
    def testGeneMutation(self):
        for gene_type in [DroughtToleranceGene, LightToleranceGene]:
            mutation_rate: float = float(np.random.rand())
            for r in np.random.random_sample(1000):
                gene = gene_type(gene_value=r,
                                 mutation_rate=mutation_rate)
                old_value = gene.value()
                gene.mutate()
                new_value = gene.value()
                self.assertTrue(np.abs((old_value - new_value) / old_value) <= mutation_rate)
        return

    @TestUtil.test_case
    def testGeneDiversity(self):
        for gene_type in [DroughtToleranceGene, LightToleranceGene]:
            for r1, r2 in np.random.rand(1000, 2):
                gene1 = gene_type(gene_value=r1)
                gene2 = gene_type(gene_value=r2)
                self.assertTrue(gene1.get_diversity(gene2) == (r1 - r2) ** 2)
        return

    @TestUtil.test_case
    def testGeneExceptions(self):

        for gene_type in [DroughtToleranceGene, LightToleranceGene]:
            for v in [-1.001, 1.001]:
                with self.assertRaises(ValueError):
                    _ = gene_type(gene_value=v)
        return

    if __name__ == "__main__":
        unittest.main()
