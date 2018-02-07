import atexit
import colorama as color
import itertools
import os
import platform
import re
import sys

from tqdm import tqdm

from .options import ArgParse
from .globals import *
from .ortho import Tile
from .util import *


# Called during sys.exit()
def cleanup():
    color.deinit()  # Colorama


# Main

def main():
    tile_errors = dict()
    ortho_pattern = re.compile("zOrtho4XP_([+-]\d+){2}")

    atexit.register(cleanup)

    color.init(autoreset=True)  # Colorama

    argparse = ArgParse(epilog=VERSION_STR, prog=PROGRAM)

    args = argparse.args
    help_message = argparse.help

    vquiet = args.verbosity == 0
    vnormal = args.verbosity == 1
    verbose = args.verbosity > 1

    try:
        test_file = os.listdir(args.tile_directory)[0]
    except IndexError:
        test_file = ""

    if (os.path.basename(args.tile_directory) == "Tiles") or re.match(ortho_pattern, test_file):
        tiles_dir = args.tile_directory
    else:
        tiles_dir = os.path.join(args.tile_directory, "Tiles")

    if not os.path.isdir(tiles_dir):
        usage(help_message, "Please provide a directory where Ortho4XP Tiles can be found", pause=args.pause)

    tiles = [f for f in sorted(os.listdir(tiles_dir)) if re.match(ortho_pattern, f)]
    tiles_count = len(tiles)

    if tiles_count == 0:
        usage(help_message,
              "\"{}\" does not appear to be a valid Ortho4XP Tiles directory, or if it is, I cannot find any Tiles."
              .format(tiles_dir), pause=args.pause)

    if not vquiet: print(VERSION_STR + os.linesep)

    if vnormal:
        print(color.Fore.LIGHTCYAN_EX + "Analyzing {} Tiles... this may take some time, please wait...".format(
            tiles_count))
        if args.progress_bar:
            t = tqdm(total=tiles_count, unit="tiles", leave=True)

    # Run the validations for each Tile
    for tile in tiles:
        if vnormal and args.progress_bar: t.update(1)

        if verbose:
            if args.verbosity > 2: print()
            print("Analyzing Tile {:.<33} ".format(tile), end=(os.linesep if args.verbosity > 2 else ""))

        tile_errors[tile] = Tile(tile, dir=tiles_dir, verbose=args.verbosity).validate()

        if len(tile_errors[tile]) == 0:
            if args.verbosity == 2: print(color.Fore.GREEN + "OKAY")
            tile_errors.pop(tile)
        else:
            if args.verbosity == 2: print(color.Fore.RED + "ERROR")

    err_count = len(list(itertools.chain.from_iterable(tile_errors.values())))

    if args.verbosity > 0:
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
