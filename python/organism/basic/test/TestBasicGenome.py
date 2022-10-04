import unittest
import pickle
import numpy as np
from typing import Dict
from copy import copy
from python.organism.basic.test.BasicUtilsForTesting import BasicUtilsForTesting
from python.exceptions.NoSuchChromosomeInGenome import NoSuchChromosomeInGenome
from python.exceptions.NotAChromosome import NotAChromosome
from python.organism.basic.BasicGenome import BasicGenome
from python.organism.basic.BasicChromosome import BasicChromosome
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene
from python.id.EntityId import EntityId
from rltrace.Trace import Trace, LogLevel
from test.UtilsForTesting import UtilsForTesting


class TestBasicGenome(unittest.TestCase):
    _run: int
    _session_id: str = EntityId().as_str()
    _trace: Trace = Trace(log_level=LogLevel.debug, log_dir_name=".", log_file_name="trace.log")

    def __init__(self, *args, **kwargs):
        super(TestBasicGenome, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        cls._trace.log(f'- - - - - - S T A R T - - - - - - \n')
        UtilsForTesting.clean_up_test_files()
        return

    def setUp(self) -> None:
        TestBasicGenome._run += 1
        self._trace.log(f'- - - - - - C A S E {TestBasicGenome._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        self._trace.log(f'- - - - - - C A S E {TestBasicGenome._run} Passed - - - - - -\n')
        return

    @classmethod
    def tearDownClass(cls) -> None:
        cls._trace.log(f'- - - - - - E N D - - - - - - \n')
        UtilsForTesting.clean_up_test_files()
        return

    @BasicUtilsForTesting.test_case
    def testBasicGenomeConstruction(self):
        genome = BasicGenome()
        self.assertTrue(len(str(genome.get_genome_id())) > 0)
        return

    @BasicUtilsForTesting.test_case
    def testGenomeChromosomeComposition(self):
        genome = BasicGenome()
        chromosome_types = genome.get_chromosome_types()
        self.assertTrue(len(chromosome_types) == 1)
        self.assertTrue(BasicChromosome in chromosome_types)
        return

    @BasicUtilsForTesting.test_case
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
        BasicUtilsForTesting.verify_matching_basic_chromosome_and_genes(self,
                                                                        basic_chromosome=chromosome,  # NOQA
                                                                        ltg=ltg,
                                                                        dtg=dtg)

        return

    @BasicUtilsForTesting.test_case
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
        BasicUtilsForTesting.test_types(test_case=self,
                                        actual_types=chromosome_types,
                                        expected_types=[BasicChromosome])

        chromosome = genome.get_chromosome(BasicChromosome)
        BasicUtilsForTesting.verify_matching_basic_chromosome_and_genes(self,
                                                                        basic_chromosome=chromosome,  # NOQA
                                                                        ltg=alternate_ltg,
                                                                        dtg=alternate_dtg)

        return

    @BasicUtilsForTesting.test_case
    def testGenomeExceptions(self):
        dtg = DroughtToleranceGene(.314159)
        ltg = LightToleranceGene(-0.314159)
        basic_chromosome = BasicChromosome(drought_gene=dtg,
                                           light_gene=ltg)
        genome = BasicGenome(chromosomes=[basic_chromosome])

        with self.assertRaises(NoSuchChromosomeInGenome):
            genome.get_chromosome(float)

        with self.assertRaises(NotAChromosome):
            genome.set_chromosome(float(0.1))  # NOQA

        return

    @BasicUtilsForTesting.test_case
    def testGenomeDiversity(self):
        for r1, r2, r3, r4 in np.random.rand(1000, 4):
            c1 = BasicChromosome(drought_gene=DroughtToleranceGene(r1), light_gene=LightToleranceGene(r2))
            c2 = BasicChromosome(drought_gene=DroughtToleranceGene(r3), light_gene=LightToleranceGene(r4))

            g1 = BasicGenome([c1])
            g2 = BasicGenome([c2])

            self.assertTrue(g1.get_diversity(g2) == ((r1 - r3) ** 2 + (r2 - r4) ** 2) / 2.0)

            return

    @BasicUtilsForTesting.test_case
    def testGenomeCopy(self):
        dtg = DroughtToleranceGene(.314159)
        ltg = LightToleranceGene(-0.314159)
        basic_chromosome = BasicChromosome(drought_gene=dtg,
                                           light_gene=ltg)
        genome = BasicGenome(chromosomes=[basic_chromosome])
        genome_copy = copy(genome)

        self.assertTrue(genome == genome_copy)
        self.assertFalse(genome.get_genome_id() == genome_copy.get_genome_id())
        for ct in genome.get_chromosome_types():
            self.assertTrue(ct in genome_copy.get_chromosome_types())
            ch = genome.get_chromosome(ct)
            chc = genome_copy.get_chromosome(ct)
            self.assertFalse(
                ch.get_chromosome_id() == chc.get_chromosome_id())
            for gt in ch.get_gene_types():
                self.assertTrue(gt in chc.get_gene_types())
                g = ch.get_gene(gt)
                gc = chc.get_gene(gt)
                self.assertFalse(g.get_gene_id() == gc.get_gene_id())

    @BasicUtilsForTesting.test_case
    def testGenomeMutate(self):
        drought_initial_value = 0.0
        light_initial_value = 0.0
        dtg = DroughtToleranceGene(drought_initial_value, mutation_rate=0.5)
        ltg = LightToleranceGene(light_initial_value, mutation_rate=0.5)
        basic_chromosome = BasicChromosome(drought_gene=dtg,
                                           light_gene=ltg)
        genome = BasicGenome(chromosomes=[basic_chromosome])

        prev_gene_values: Dict[type, float] = dict()
        gene_mutation_count: Dict[type, float] = dict()
        for k, v in map(lambda x: (type(x), x.value()), BasicGenome.gene_list(genome)):
            prev_gene_values[k] = v
            gene_mutation_count[k] = 0

        num_trials: int = 9999
        for _ in range(num_trials):
            mutation_step_size = float(np.random.rand() * 0.1)
            genome = BasicGenome.mutate(genome_to_mutate=genome, step_size=mutation_step_size)
            for k, v in prev_gene_values.items():
                new_v = genome.get_chromosome(type(basic_chromosome)).get_gene(k).value()
                if new_v != v:
                    # print(f'k {k} new {new_v} old {v} step {mutation_step_size}')
                    gene_mutation_count[k] = gene_mutation_count[k] + 1
                    self.assertTrue((abs(new_v - v) - mutation_step_size) < 0.0000001)
                    prev_gene_values[k] = new_v

        for k in gene_mutation_count.keys():
            self.assertTrue(gene_mutation_count[k] > 0)

        return


if __name__ == "__main__":
    unittest.main()
