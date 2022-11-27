import unittest
import random
from python.id.EntityId import EntityId
from python.util.TypeUtil import TypeUtil
from rltrace.Trace import Trace, LogLevel


class TestTypeUtil(unittest.TestCase):
    _run: int
    _session_id: str = EntityId().as_str()
    _trace: Trace = Trace(log_level=LogLevel.debug, log_dir_name=".", log_file_name="trace.log")
    _module_and_name: str = 'python.id.EntityId.EntityId'
    _module_and_name_bits = _module_and_name.split(sep='.')

    def __init__(self, *args, **kwargs):
        super(TestTypeUtil, self).__init__(*args, **kwargs)
        return

    @classmethod
    def setUpClass(cls):
        cls._run = 0
        cls._trace.log(f'- - - - - - S T A R T - - - - - - \n')
        return

    def setUp(self) -> None:
        TestTypeUtil._run += 1
        self._trace.log(f'- - - - - - C A S E {TestTypeUtil._run} Start - - - - - -')
        return

    def tearDown(self) -> None:
        self._trace.log(f'- - - - - - C A S E {TestTypeUtil._run} Passed - - - - - -\n')
        return

    @classmethod
    def tearDownClass(cls) -> None:
        cls._trace.log(f'- - - - - - E N D - - - - - - \n')
        return

    def test_simple_module_and_name(self):
        assert TypeUtil.module_and_name(EntityId) == TestTypeUtil._module_and_name
        return

    def test_contains_module_and_name(self):
        assert TypeUtil.module_and_name(EntityId, TestTypeUtil._module_and_name[0]) == TestTypeUtil._module_and_name
        return

    def test_contains_all_module_and_name(self):
        assert TypeUtil.module_and_name(EntityId,
                                        tuple(TestTypeUtil._module_and_name_bits)) == TestTypeUtil._module_and_name
        return

    def test_contains_all_shuffle_module_and_name(self):
        bits = random.sample(TestTypeUtil._module_and_name_bits, len(TestTypeUtil._module_and_name_bits))
        assert TypeUtil.module_and_name(EntityId, tuple(bits)) == TestTypeUtil._module_and_name
        return

    def test_module_and_name_exception_missing(self):
        redq: str = "Missing"
        expected: str = f'{TestTypeUtil._module_and_name} does not contain required element {redq}'
        with self.assertRaisesRegex(ValueError, expected) as e:
            TypeUtil.module_and_name(EntityId, redq)
        return

    def test_module_and_name_exception_type(self):
        expected: str = 'contains param must be a string or tuple of strings'
        with self.assertRaisesRegex(ValueError, expected) as e:
            TypeUtil.module_and_name(EntityId, float(1.0))  # NOQA
        return

    def test_module_and_name_exception_tuple_content(self):
        expected: str = 'contains param must be a tuple of strings'
        with self.assertRaisesRegex(ValueError, expected) as e:
            TypeUtil.module_and_name(EntityId, tuple([float(1.0), TestTypeUtil._module_and_name_bits[0]]))  # NOQA
        return


if __name__ == "__main__":
    unittest.main()
