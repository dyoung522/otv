import unittest
from otv.util import *


class TestUtilFunctions(unittest.TestCase):
    PARAMS = [
        (0, "person", "people", "no people"),
        (1, "person", "people", "1 person"),
        (2, "person", "people", "2 people"),
        (2, "tree", None, "2 trees"),
        (1, "tree", None, "1 tree"),
        (0, "tree", None, "no trees"),
    ]

    def test_pluralize(self):
        for params in self.PARAMS:
            with self.subTest(result=params[3]):
                self.assertEqual(pluralize(params[0], params[1], params[2]), params[3])
