import os
import unittest

from unittest.mock import patch
from pathlib import Path
from pyfakefs import fake_filesystem_unittest
from otv.ortho import Tile


class TestTileClassMethods(fake_filesystem_unittest.TestCase):
    lat = "+11"
    long = "-222"
    tile_name = f"zOrtho_{lat}{long}"

    def setUp(self):
        self.setUpPyfakefs()
        self.tile_path = Path(self.tile_name)
        self.tile = Tile(self.tile_path)
        os.mkdir(self.tile_path)

    def test_tile(self):
        self.assertEqual(self.tile.tile, self.tile_path, "Tile is not a pathlib object")

    def test_tile_name(self):
        self.assertEqual(self.tile.name, self.tile_name, "Cannot parse tile.name")

    def test_tile_lat(self):
        self.assertEqual(self.tile.lat, self.lat, "Could not determine latitude")

    def test_tile_long(self):
        self.assertEqual(self.tile.long, self.long, "Could not determine longitude")

    def test_tile_verbose(self):
        self.assertEqual(self.tile.verbose, 0, "verbose does not default to 0")
        new_tile = Tile(self.tile_path, verbose=1)
        self.assertEqual(new_tile.verbose, 1, "verbose is not settable")

    def test_validate_dir_returns_true_with_valid_dir(self):
        test_path = self.tile_path.joinpath("test_dir")
        os.mkdir(test_path)
        with open(test_path.joinpath("test_file"), 'w') as f:
            f.write("This is test file.\n")

        with patch.object(Path, 'is_dir', return_value=True):
            self.assertTrue(self.tile.validate_dir("test_dir"),
                            "#validate_dir is not properly validating directories {}".format(self.tile.errors))

        self.assertEqual(len(self.tile.errors), 0)

    def test_validate_dir_returns_false_with_missing_dir(self):
        self.tile.errors = []

        self.assertFalse(self.tile.validate_dir("test_dir"))
        self.assertEqual(len(self.tile.errors), 1)
        self.assertTrue("NOT FOUND" in self.tile.errors[0])

    def test_validate_dir_returns_false_with_empty_valid_dir(self):
        test_path = self.tile_path.joinpath("test_dir")
        os.mkdir(test_path)

        with patch.object(Path, 'is_dir', return_value=True):
            self.assertFalse(self.tile.validate_dir("test_dir"),
                             "#validate_dir is not properly validating directories {}".format(self.tile.errors))

        self.assertEqual(len(self.tile.errors), 1)
        self.assertTrue("IS EMPTY" in self.tile.errors[0])


if __name__ == '__main__':
    unittest.main()
