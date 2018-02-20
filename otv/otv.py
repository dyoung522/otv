import atexit
import colorama as color
import itertools
import os
import platform
import sys

from glob import glob
from pathlib import Path
from tqdm import tqdm

from .db import DB
from .options import ArgParse
from .globals import *
from .ortho import Tile
from .util import *


# Called during sys.exit()
def cleanup():
    color.deinit()  # Colorama


def __get_tiles_dir(directory):
    path = Path(directory)

    if not path.is_dir():
        return None

    if glob(str(path / "zOrtho4XP_*")):
        return path

    return path if path.name == "Tiles" else (path / "Tiles")


def main():
    err_count = 0
    tile_errors = dict()

    atexit.register(cleanup)

    color.init(autoreset=True)  # Colorama

    argparse = ArgParse(epilog=VERSION_STR, prog=PROGRAM)

    args = argparse.args
    help_message = argparse.help

    vquiet = args.verbosity == 0
    vnormal = args.verbosity == 1
    verbose = args.verbosity > 1

    tiles_dir = __get_tiles_dir(args.tile_directory)

    if tiles_dir is None or not tiles_dir.is_dir():
        usage(help_message, "Please provide a directory where Ortho4XP Tiles can be found", pause=args.pause)

    tiledb = DB(tiles_dir.parent)

    tiles = sorted(tiles_dir.glob("zOrtho4XP_*"))
    total_tiles_count = len(tiles)

    # Eliminate any tiles we've previously validated
    if not args.all:
        for tile in tiles:
            if tiledb.find_tile(tile):
                tiles.remove(tile)

    tiles_count = len(tiles)

    if total_tiles_count == 0:
        usage(help_message,
              "\"{}\" does not appear to be a valid Ortho4XP Tiles directory, or if it is, I cannot find any Tiles."
              .format(tiles_dir), pause=args.pause)

    if not vquiet: print(VERSION_STR + os.linesep)

    if tiles_count == 0:
        if not vquiet:
            print(color.Fore.LIGHTGREEN_EX + "All tiles have been validated")

    # Validate Tiles
    else:
        if vnormal:
            print(color.Fore.LIGHTCYAN_EX + "Analyzing {} Tiles{}... this may take some time, please wait...".format(
                tiles_count,
                "" if tiles_count == total_tiles_count else " (out of {})".format(total_tiles_count)
            ))
            if args.progress_bar:
                t = tqdm(total=tiles_count, unit="tiles", leave=True)

        # Run the validations for each Tile
        for tile in tiles:
            tile_name = tile.name

            if vnormal and args.progress_bar: t.update(1)

            if verbose:
                if args.verbosity > 2: print()
                print("Analyzing Tile {:.<33} ".format(tile_name), end=(os.linesep if args.verbosity > 2 else ""))

            tile_errors[tile_name] = Tile(tile, verbose=args.verbosity).validate()

            if len(tile_errors[tile_name]) == 0:
                if args.verbosity == 2: print(color.Fore.GREEN + "OKAY")
                tiledb.add_tile(tile)
                tile_errors.pop(tile_name)
            else:
                if args.verbosity == 2: print(color.Fore.RED + "ERROR")

        err_count = len(list(itertools.chain.from_iterable(tile_errors.values())))

        if not vquiet:
            if vnormal and args.progress_bar:
                t.close()

            print(os.linesep + "Scanned {}... ".format(pluralize(tiles_count, "Tile")), end="")

            if err_count == 0:
                print(color.Fore.LIGHTGREEN_EX + "All OKAY")
            else:
                bad_tiles_count = len(tile_errors.values())
                bad_tiles_string = pluralize(bad_tiles_count, "tile")
                err_count_string = pluralize(err_count, "error")

                print(color.Fore.LIGHTRED_EX + "Found {} with a total of {}".format(bad_tiles_string, err_count_string))

                print(os.linesep +
                      color.Fore.LIGHTRED_EX +
                      "{} need attention:".format(bad_tiles_string), file=sys.stderr)

                for tile, errors in tile_errors.items():
                    print(os.linesep + "  {}".format(color.Fore.LIGHTWHITE_EX + tile), file=sys.stderr)
                    for error in errors:
                        print("    -> {}".format(color.Fore.LIGHTRED_EX + error), file=sys.stderr)

    if args.pause or (platform.system() == "Windows"):
        input(os.linesep + "Press ENTER key to exit")

    sys.exit(err_count)


if __name__ == "__main__": main()
