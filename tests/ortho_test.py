import os
import pytest
from ovt.ortho import Tile

lat = "+11"
long = "-222"
tile_name = f"zOrtho_{lat}{long}"
test_dir = "xxxTESTDIRxxx"


@pytest.fixture
def tile():
    return Tile(tile_name)


def setup():
    os.mkdir(test_dir)


def teardown():
    os.rmdir(test_dir)


def test_tile_name(tile):
    assert (tile.tile_name) == tile_name


def test_tile_lat(tile):
    assert (tile.lat) == lat


def test_tile_long(tile):
    assert (tile.long) == long


def test_validate_dir_returns_true_with_valid_dir(tile):
    tile.tile_dir = "."
    assert (tile.validate_dir(".")) is True
    assert (len(tile.errors)) == 0


def test_validate_dir_returns_false_with_invalid_dir(tile):
    tile.errors = []
    tile.tile_dir = "."

    assert (tile.validate_dir("xxxFOOxxx")) is False
    assert (len(tile.errors)) == 1
    assert ("NOT FOUND" in tile.errors[0])


def test__validate_dir_returns_false_with_empty_valid_dir(tile):
    tile.errors = []
    tile.tile_dir = "."

    assert (tile.validate_dir(test_dir)) is False
    assert (len(tile.errors)) == 1
    assert ("IS EMPTY" in tile.errors[0])
