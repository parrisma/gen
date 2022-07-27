import unittest
from typing import List
from python.base.Organism import Organism
from python.organism.basic.test.TestUtil import TestUtil
from python.organism.basic.BasicSelector import BasicSelector
from python.organism.basic.BasicOrganismFactory import BasicOrganismFactory


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

    @TestUtil.test_case
    def test1(self):
        f = BasicOrganismFactory()
        bs = BasicSelector()
        population: List[Organism] = [f.new() for _ in range(10)]
        for o in population:
            o.run()
        return
