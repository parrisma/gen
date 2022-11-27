import unittest
from python.organism.basic.test.BasicUtilsForTesting import BasicUtilsForTesting
from python.id.EntityId import EntityId
from rltrace.Trace import Trace, LogLevel
from python.organism.NN.genes.LayerTypeGene import LayerTypeGene


class TestLayerTypeGene(unittest.TestCase):
    _run: int
    _session_id: str = EntityId().as_str()
    _trace: Trace = Trace(log_level=LogLevel.debug, log_dir_name=".", log_file_name="trace.log")

    def __init__(self, *args, **kwargs):
        super(TestLayerTypeGene, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        cls._trace.log(f'- - - - - - S T A R T - - - - - - \n')
        return

    def setUp(self) -> None:
        TestLayerTypeGene._run += 1
        self._trace.log(f'- - - - - - C A S E {TestLayerTypeGene._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        self._trace.log(f'- - - - - - C A S E {TestLayerTypeGene._run} Passed - - - - - -\n')
        return

    @classmethod
    def tearDownClass(cls) -> None:
        cls._trace.log(f'- - - - - - E N D - - - - - - \n')
        return

    @BasicUtilsForTesting.test_case
    def testGeneConstructionFromDefaults(self):
        ltg = LayerTypeGene()
        n = ltg.num_layer_types()
        lts = ltg.layer_types()
        self.assertTrue(n == len(lts))  # num layers must equal the number of layer types
        return


if __name__ == "__main__":
    unittest.main()
