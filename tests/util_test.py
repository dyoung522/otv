import pytest
from ovt.util import *


@pytest.mark.parametrize("count, singular, plural, expect", [
    (0, "person", "people", "no people"),
    (1, "person", "people", "1 person"),
    (2, "person", "people", "2 people"),
    (2, "tree", None, "2 trees"),
    (1, "tree", None, "1 tree"),
    (0, "tree", None, "no trees"),
])
def test_pluralize(count, singular, plural, expect):
    assert pluralize(count, singular, plural) == expect
