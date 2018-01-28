import pytest
from ovt.ortho import Tile

lat = "+11"
long = "+222"
tile_name = f"zOrtho{lat}{long}"


@pytest.fixture
def tile():
    return Tile(tile_name)


def test_tile_name():
    assert (tile().tile_name) == tile_name


def test_tile_lat():
    assert (tile().lat) == lat


def test_tile_long():
    assert (tile().long) == long


def test_directories_returns_a_list():
    assert type(tile().directories()) is list


def test_directories_returns_valid_items():
    assert len(tile().directories()) is 3

    for dir in ["earth nav data", "textures", "terrain"]:
        assert dir in tile().directories(), "Did not find \"{}\" in list of directories to check".format(dir)
