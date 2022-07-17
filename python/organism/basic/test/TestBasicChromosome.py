import unittest
from python.organism.basic.test.TestUtil import TestUtil
from python.organism.basic.BasicChromosome import BasicChromosome
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene
from python.exceptions.NoSuchGeneTypeInChromosome import NoSuchGeneTypeInChromosome
from python.exceptions.NotAGene import NotAGene


class TestBasicChromosome(unittest.TestCase):
    _run: int

    def __init__(self, *args, **kwargs):
        super(TestBasicChromosome, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        return

    def setUp(self) -> None:
        TestBasicChromosome._run += 1
        print(f'- - - - - - C A S E {TestBasicChromosome._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        print(f'- - - - - - C A S E {TestBasicChromosome._run} Passed - - - - - -')
        return

    def testBasicChromosomeConstruction(self):
        basic_chromosome = BasicChromosome()
        self.assertTrue(len(str(basic_chromosome.get_chromosome_id())) > 0)
        return

    def testChromosomeGeneComposition(self):
        basic_chromosome = BasicChromosome()
        gene_types = basic_chromosome.get_gene_types()
        TestUtil.test_types(test_case=self,
                            actual_types=gene_types,
                            expected_types=[DroughtToleranceGene, LightToleranceGene])
        return

    def testChromosomeGeneConstructor(self):
        dtg = DroughtToleranceGene(.314159)
        ltg = LightToleranceGene(-0.314159)
        basic_chromosome = BasicChromosome(drought_gene=dtg,
                                           light_gene=ltg)

        TestUtil.verify_matching_basic_chromosome_and_genes(test_case=self,
                                                            basic_chromosome=basic_chromosome,
                                                            ltg=ltg,
                                                            dtg=dtg)
        return

    def testChromosomeGeneSetGet(self):
        basic_chromosome = BasicChromosome()
        dtg = DroughtToleranceGene(.314159)
        ltg = LightToleranceGene(-0.314159)

        basic_chromosome.set_gene(dtg)
        basic_chromosome.set_gene(ltg)

        gene_types = basic_chromosome.get_gene_types()
        TestUtil.test_types(test_case=self,
                            actual_types=gene_types,
                            expected_types=[DroughtToleranceGene, LightToleranceGene])

        TestUtil.verify_matching_basic_chromosome_and_genes(test_case=self,
                                                            basic_chromosome=basic_chromosome,
                                                            ltg=ltg,
                                                            dtg=dtg)

    def testChromosomeExceptions(self):
        dtg = DroughtToleranceGene(.314159)
        ltg = LightToleranceGene(-0.314159)
        basic_chromosome = BasicChromosome(drought_gene=dtg,
                                           light_gene=ltg)

        with self.assertRaises(NoSuchGeneTypeInChromosome):
            basic_chromosome.get_gene(float)

        with self.assertRaises(NotAGene):
            basic_chromosome.set_gene(float(0.1))  # NOQA

        return

    if __name__ == "__main__":
        unittest.main()
