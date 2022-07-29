import unittest
import numpy as np
from copy import copy
from typing import Dict
from python.organism.basic.test.UtilsForTesting import UtilsForTesting
from python.organism.basic.BasicMetrics import BasicMetrics


class TestBasicMetrics(unittest.TestCase):
    _run: int

    def __init__(self, *args, **kwargs):
        super(TestBasicMetrics, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        return

    def setUp(self) -> None:
        TestBasicMetrics._run += 1
        print(f'- - - - - - C A S E {TestBasicMetrics._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        print(f'- - - - - - C A S E {TestBasicMetrics._run} Passed - - - - - -\n')
        return

    @UtilsForTesting.test_case
    def testBasicMetricsConstructor(self):
        ids_already_seen: Dict[str, str] = {}
        for _ in range(100):
            fitness = np.random.rand()
            alive = True
            if np.random.rand() > 0.5:
                alive = False
            bm = BasicMetrics(alive=alive,
                              fitness=float(fitness))
            self.assertFalse(bm.get_metrics_id() in ids_already_seen)
            ids_already_seen[bm.get_metrics_id()] = bm.get_metrics_id()
            self.assertTrue(bm.is_alive() == alive)
            self.assertTrue(bm.get_fitness() - fitness < UtilsForTesting.MARGIN_OF_ERROR)
        return

    @UtilsForTesting.test_case
    def testMetricsCopy(self):
        fitness = np.random.rand()
        alive = True
        bm = BasicMetrics(alive=alive,
                          fitness=float(fitness))
        bm_copy = copy(bm)
        self.assertTrue(bm == bm_copy)
        self.assertFalse(bm.get_metrics_id() == bm_copy.get_metrics_id())
        return
