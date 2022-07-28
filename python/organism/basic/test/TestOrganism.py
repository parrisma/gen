import unittest
import numpy as np
from python.base.Genome import Genome
from python.organism.basic.BasicOrganism import BasicOrganism
from python.organism.basic.test.TestUtil import TestUtil
from python.organism.basic.BasicGenome import BasicGenome
from python.organism.basic.BasicChromosome import BasicChromosome
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene


class TestOrganism(unittest.TestCase):
    _run: int

    def __init__(self, *args, **kwargs):
        super(TestOrganism, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        return

    def setUp(self) -> None:
        TestOrganism._run += 1
        print(f'- - - - - - C A S E {TestOrganism._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        print(f'- - - - - - C A S E {TestOrganism._run} Passed - - - - - -\n')
        return

    @TestUtil.test_case
    def testBasicOrganismConstruction(self):
        r1: float = 0.3141
        r2: float = -0.678
        c1 = BasicChromosome(drought_gene=DroughtToleranceGene(r1), light_gene=LightToleranceGene(r2))
        g1 = BasicGenome([c1])
        basic_organism = BasicOrganism(genome=g1)
        g2 = basic_organism.get_genome()
        self.assertTrue(g2.get_chromosome(BasicChromosome).get_gene(DroughtToleranceGene).value() == r1)
        self.assertTrue(g2.get_chromosome(BasicChromosome).get_gene(LightToleranceGene).value() == r2)
        return

    @TestUtil.test_case
    def testBasicOrganismDiversity(self):
        r1, r2, r3, r4, r5, r6 = (-1.0, -1.0, 1.0, 1.0, -1.0, 1.0)
        c1 = BasicChromosome(drought_gene=DroughtToleranceGene(r1), light_gene=LightToleranceGene(r2))
        c2 = BasicChromosome(drought_gene=DroughtToleranceGene(r3), light_gene=LightToleranceGene(r4))
        c3 = BasicChromosome(drought_gene=DroughtToleranceGene(r5), light_gene=LightToleranceGene(r6))

        g1 = BasicGenome([c1])
        g2 = BasicGenome([c2])
        g3 = BasicGenome([c3])

        basic_organism1 = BasicOrganism(genome=g1)
        basic_organism2 = BasicOrganism(genome=g2)
        basic_organism3 = BasicOrganism(genome=g3)

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

    @TestUtil.test_case
    def testBasicOrganismCrossOver(self):
        for _ in range(100):
            r1, r2, r3, r4 = np.random.random(4)
            c1 = BasicChromosome(drought_gene=DroughtToleranceGene(r1), light_gene=LightToleranceGene(r2))
            c2 = BasicChromosome(drought_gene=DroughtToleranceGene(r3), light_gene=LightToleranceGene(r4))

            g1 = BasicGenome([c1])
            g2 = BasicGenome([c2])

            basic_organism1 = BasicOrganism(genome=g1)
            basic_organism2 = BasicOrganism(genome=g2)

            # Mix rate of 100% guarantees a full swap
            new_organism = BasicOrganism(basic_organism1.crossover(mix_rate=0.5, organism=basic_organism2))  # NOQA
            new_genes = Genome.gene_list(new_organism.get_genome())
            expected_genes = Genome.gene_list(basic_organism2.get_genome())
            self.assertTrue(new_genes == expected_genes)

            # Mix rate of 0% guarantees a zero swap
            new_organism = BasicOrganism(basic_organism1.crossover(mix_rate=0.0, organism=basic_organism2))  # NOQA
            new_genes = Genome.gene_list(new_organism.get_genome())
            expected_genes = Genome.gene_list(basic_organism2.get_genome())
            self.assertTrue(new_genes == expected_genes)

        return
