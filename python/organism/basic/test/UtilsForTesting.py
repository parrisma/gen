import unittest
from typing import List
from python.organism.basic.BasicChromosome import BasicChromosome
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene


class UtilsForTesting:
    MARGIN_OF_ERROR: float = 1e-06

    @classmethod
    def verify_matching_basic_chromosome_and_genes(cls,
                                                   test_case: unittest.TestCase,
                                                   basic_chromosome: BasicChromosome,
                                                   ltg: LightToleranceGene,
                                                   dtg: DroughtToleranceGene):
        test_case.assertTrue(isinstance(basic_chromosome, BasicChromosome))
        test_case.assertTrue(isinstance(ltg, LightToleranceGene))
        test_case.assertTrue(isinstance(dtg, DroughtToleranceGene))
        test_case.assertTrue(basic_chromosome.get_gene(DroughtToleranceGene) == dtg)
        test_case.assertTrue(basic_chromosome.get_gene(LightToleranceGene) == ltg)
        test_case.assertTrue(basic_chromosome.get_gene(DroughtToleranceGene).value() == dtg.value())
        test_case.assertTrue(basic_chromosome.get_gene(LightToleranceGene).value() == ltg.value())
        return

    @classmethod
    def test_types(cls,
                   test_case: unittest.TestCase,
                   actual_types: List[type],
                   expected_types: List[type]):
        test_case.assertTrue(len(actual_types), len(expected_types))
        for t in expected_types:
            test_case.assertTrue(t in actual_types)
        return

    @classmethod
    def test_case(cls,
                  func):
        def annotated_test_case(*args, **kwargs):
            print(f'- - - - - - R U N  {func.__name__}  - - - - - -')
            func(*args, **kwargs)

        return annotated_test_case
