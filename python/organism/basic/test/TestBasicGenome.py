import unittest
from python.organism.basic.test.TestUtil import TestUtil
from python.organism.basic.BasicGenome import BasicGenome
from python.organism.basic.BasicChromosome import BasicChromosome
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene


class TestBasicGenome(unittest.TestCase):
    _run: int

    def __init__(self, *args, **kwargs):
        super(TestBasicGenome, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        return

    def setUp(self) -> None:
        TestBasicGenome._run += 1
        print(f'- - - - - - C A S E {TestBasicGenome._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        print(f'- - - - - - C A S E {TestBasicGenome._run} Passed - - - - - -')
        return

    def testBasicGenomeConstruction(self):
        genome = BasicGenome()
        self.assertTrue(len(str(genome.get_genome_id())) > 0)
        return

    def testChromosomeComposition(self):
        genome = BasicGenome()
        chromosome_types = genome.get_chromosome_types()
        self.assertTrue(len(chromosome_types) == 1)
        self.assertTrue(BasicChromosome in chromosome_types)
        return

    def testGenomeConstructor(self):
        dtg = DroughtToleranceGene(.314159)
        ltg = LightToleranceGene(-0.314159)
        basic_chromosome = BasicChromosome(drought_gene=dtg,
                                           light_gene=ltg)
        genome = BasicGenome(chromosomes=[basic_chromosome])

        chromosome_types = genome.get_chromosome_types()
        self.assertTrue(len(chromosome_types) == 1)
        self.assertTrue(BasicChromosome in chromosome_types)

        chromosome = genome.get_chromosome(BasicChromosome)
        TestUtil.verify_matching_basic_chromosome_and_genes(self,
                                                            basic_chromosome=chromosome,  # NOQA
                                                            ltg=ltg,
                                                            dtg=dtg)

        return

    def testGeneSetGet(self):
        dtg = DroughtToleranceGene(.314159)
        ltg = LightToleranceGene(-0.314159)
        basic_chromosome = BasicChromosome(drought_gene=dtg,
                                           light_gene=ltg)
        genome = BasicGenome(chromosomes=[basic_chromosome])

        alternate_dtg = DroughtToleranceGene(.314159 * 2.0)
        alternate_ltg = LightToleranceGene(-0.314159 * 2.0)
        alternate_chromosome = BasicChromosome(drought_gene=alternate_dtg,
                                               light_gene=alternate_ltg)
        genome.set_chromosome(alternate_chromosome)

        chromosome_types = genome.get_chromosome_types()
        TestUtil.test_types(test_case=self,
                            actual_types=chromosome_types,
                            expected_types=[BasicChromosome])

        chromosome = genome.get_chromosome(BasicChromosome)
        TestUtil.verify_matching_basic_chromosome_and_genes(self,
                                                            basic_chromosome=chromosome,  # NOQA
                                                            ltg=alternate_ltg,
                                                            dtg=alternate_dtg)

        return


if __name__ == "__main__":
    unittest.main()
