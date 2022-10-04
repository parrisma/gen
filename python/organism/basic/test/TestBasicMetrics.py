import unittest
import numpy as np
from copy import copy
from typing import Dict
from python.organism.basic.test.BasicUtilsForTesting import BasicUtilsForTesting
from python.organism.basic.BasicMetrics import BasicMetrics
from python.id.EntityId import EntityId
from rltrace.Trace import Trace, LogLevel
from test.UtilsForTesting import UtilsForTesting


class TestBasicMetrics(unittest.TestCase):
    _run: int
    _session_id: str = EntityId().as_str()
    _trace: Trace = Trace(log_level=LogLevel.debug, log_dir_name=".", log_file_name="trace.log")

    def __init__(self, *args, **kwargs):
        super(TestBasicMetrics, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        cls._trace.log(f'- - - - - - S T A R T - - - - - - \n')
        UtilsForTesting.clean_up_test_files()
        return

    def setUp(self) -> None:
        TestBasicMetrics._run += 1
        self._trace.log(f'- - - - - - C A S E {TestBasicMetrics._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        self._trace.log(f'- - - - - - C A S E {TestBasicMetrics._run} Passed - - - - - -\n')
        return

    @classmethod
    def tearDownClass(cls) -> None:
        cls._trace.log(f'- - - - - - E N D - - - - - - \n')
        UtilsForTesting.clean_up_test_files()
        return

    @BasicUtilsForTesting.test_case
    def testBasicMetricsConstructor(self):
        ids_already_seen: Dict[str, str] = {}
        for _ in range(100):
            fitness = np.random.rand()
            diversity = np.random.rand()
            alive = True
            if np.random.rand() > 0.5:
                alive = False
            bm = BasicMetrics(alive=alive,
                              fitness=float(fitness),
                              diversity=float(diversity))
            self.assertFalse(bm.get_metrics_id() in ids_already_seen)
            ids_already_seen[bm.get_metrics_id()] = bm.get_metrics_id()
            self.assertTrue(bm.is_alive() == alive)
            self.assertTrue(bm.get_fitness() - fitness < BasicUtilsForTesting.MARGIN_OF_ERROR)
        return

    @BasicUtilsForTesting.test_case
    def testMetricsCopy(self):
        fitness = np.random.rand()
        diversity = np.random.rand()
        alive = True
        bm = BasicMetrics(alive=alive,
                          fitness=float(fitness),
                          diversity=float(diversity))
        bm_copy = copy(bm)
        self.assertTrue(bm == bm_copy)
        self.assertFalse(bm.get_metrics_id() == bm_copy.get_metrics_id())
        return
