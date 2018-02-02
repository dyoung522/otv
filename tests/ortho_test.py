import os
from otv.ortho import Tile
import pytest

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


def test_validate_dir_returns_true_with_valid_dir(tile):
    tile.tile_dir = "."
    assert (tile.validate_dir(".")) is True
    assert (len(tile.errors)) == 0


def test_validate_dir_returns_false_with_invalid_dir(tile, monkeypatch):
    tile.errors = []
    tile.tile_dir = "."

    def mock_isdir(path): return False

    monkeypatch.setattr(os.path, 'isdir', mock_isdir)

    assert (tile.validate_dir(".")) is False
    assert (len(tile.errors)) == 1
    assert ("NOT FOUND" in tile.errors[0])


def test__validate_dir_returns_false_with_empty_valid_dir(tile, monkeypatch):
    tile.errors = []
    tile.tile_dir = "."

    def mock_listdir(path): return []

    monkeypatch.setattr(os, 'listdir', mock_listdir)

    assert (tile.validate_dir(".")) is False
    assert (len(tile.errors)) == 1
    assert ("IS EMPTY" in tile.errors[0])
