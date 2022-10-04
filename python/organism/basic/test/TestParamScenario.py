import unittest
import numpy as np
from python.organism.basic.test.BasicUtilsForTesting import BasicUtilsForTesting
from python.visualise.ParamScenario import ParamScenario


class TestParamScenario(unittest.TestCase):
    _run: int

    def __init__(self, *args, **kwargs):
        super(TestParamScenario, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        return

    def setUp(self) -> None:
        TestParamScenario._run += 1
        print(f'- - - - - - C A S E {TestParamScenario._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        print(f'- - - - - - C A S E {TestParamScenario._run} Passed - - - - - -\n')
        return

    @BasicUtilsForTesting.test_case
    def testParamScenarioSingleValue(self):
        num_to_test = 100
        test_value: np.ndarray = np.random.rand()
        param_scenario: ParamScenario = ParamScenario(scenario_name="ParamScenarioTest1",
                                                      param_values_by_index=np.array(test_value).reshape(1))

        # For Single value, we expect the same answer irrespective of the scenario index.
        for index in range(num_to_test):
            self.assertTrue(param_scenario(scenario_index=index) == test_value)

        return

    @BasicUtilsForTesting.test_case
    def testParamScenarioMultiValue(self):
        num_to_test = 100
        test_values: np.ndarray = np.random.rand(num_to_test)
        param_scenario: ParamScenario = ParamScenario(scenario_name="ParamScenarioTest2",
                                                      param_values_by_index=test_values)

        # For Multi value, we expect the corresponding value for the given scenario index.
        for index in range(100):
            self.assertTrue(param_scenario(scenario_index=index) == test_values[index])

        return
