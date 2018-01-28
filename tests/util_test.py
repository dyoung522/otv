from ovt.util import *


def test_pluralize_with_zero():
    assert (pluralize(0, "person", "people")) == "no people"


def test_pluralize_with_one():
    assert (pluralize(1, "person", "people")) == "1 person"


def test_pluralize_with_two():
    assert (pluralize(2, "person", "people")) == "2 people"
