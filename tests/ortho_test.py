import pytest
from ovt.ortho import Tile

lat = "+11"
long = "-222"
tile_name = f"zOrtho_{lat}{long}"


@pytest.fixture
def tile():
    return Tile(tile_name)


def test_tile_name(tile):
    assert (tile.tile_name) == tile_name


def test_tile_lat(tile):
    assert (tile.lat) == lat


def test_tile_long(tile):
    assert (tile.long) == long


def test_tile_directories(tile):
    assert type(tile.directories()) is list
    assert len(tile.directories()) is 3
    for dir in ["earth nav data", "textures", "terrain"]:
        assert dir in tile.directories(), "Did not find \"{}\" in list of directories to check".format(dir)
