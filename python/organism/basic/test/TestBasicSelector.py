import unittest
from typing import List, Dict
import numpy as np
from python.base.Organism import Organism
from python.base.Selector import Selector
from python.organism.basic.test.BasicUtilsForTesting import BasicUtilsForTesting
from python.organism.basic.BasicSelector import BasicSelector
from python.organism.basic.test.OrganismForTesting import OrganismForTesting


class TestBasicSelector(unittest.TestCase):
    _run: int

    def __init__(self, *args, **kwargs):
        super(TestBasicSelector, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        return

    def setUp(self) -> None:
        TestBasicSelector._run += 1
        print(f'- - - - - - C A S E {TestBasicSelector._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        print(f'- - - - - - C A S E {TestBasicSelector._run} Passed - - - - - -\n')
        return

    @BasicUtilsForTesting.test_case
    def testSelectionProbabilityGenerator(self):
        expected_probs: List[float] = [  # expected probs for 10 items with initial prob of selection = 20%
            0.2, 0.16, 0.128, 0.1024, 0.08192, 0.065536, 0.0524288,
            0.04194304, 0.033554432, 0.134217728]
        actual_probs = Selector.rank_selection_probabilities(initial_prob=.2, num=10)
        self.assertTrue(np.sum(actual_probs) == 1.0)
        for expected, actual in zip(expected_probs, actual_probs):
            self.assertTrue(expected - actual < BasicUtilsForTesting.MARGIN_OF_ERROR)
        return

    @BasicUtilsForTesting.test_case
    def testSelectionOfOrganisms(self):
        bs = BasicSelector(selection_probability=0.2)
        num_to_generate: int = 10
        population: List[Organism] = [OrganismForTesting(fitness=i, diversity=num_to_generate - i) for i in
                                      range(num_to_generate)]

        # A means to count the selection frequency by fitness
        survival_stats: Dict[str, int] = {}
        for o in population:
            survival_stats[str(o.fitness())] = int(0)

        for _ in range(10000):
            survivors = bs.select_survivors(population=population)  # NOQA
            for s in survivors:
                survival_stats[str(s.fitness())] = survival_stats[str(s.fitness())] + 1

        # Check when sorted by selection frequency the fitness (keys) come back in order 0 .. n as this matches the
        # probability distribution with which they were selected.
        self.assertTrue(all([int(a) == int(b) for a, b in
                             zip([k for k, v in sorted([s for s in survival_stats.items()], key=lambda o: o[1])],
                                 range(num_to_generate))]))
        return
