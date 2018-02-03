import atexit
import colorama as color
import os
import sys

from .options import ArgParse
from .globals import *
from .ortho import Tile
from .util import *


# Called during sys.exit()
def cleanup():
    color.deinit()  # Colorama


# Main

def main():
    errors = []
    bad_tiles = {}

    atexit.register(cleanup)

    color.init(autoreset=True)  # Colorama

    argparse = ArgParse(epilog=VERSION_STR, prog=PROGRAM)

    args = argparse.args
    help_message = argparse.help

    vquiet = args.verbosity == 0
    vnormal = args.verbosity == 1
    verbose = args.verbosity > 1

    if os.path.basename(args.tile_directory) == "Tiles":
        tiles_dir = args.tile_directory
    else:
        tiles_dir = os.path.join(args.tile_directory, "Tiles")

    if not os.path.isdir(tiles_dir):
        usage(help_message, "Please provide a directory where Ortho4XP Tiles can be found")

    tiles = sorted(os.listdir(tiles_dir))
    tiles_count = len(tiles)

    if tiles_count == 0:
        usage(help_message,
              "\"{}\" does not appear to be a valid Ortho4XP Tiles directory, or if it is, I cannot find any Tiles."
              .format(tiles_dir))

    if not vquiet: print(VERSION_STR + os.linesep)

    if vnormal:
        # ToDo: Create a progress bar for this
        print(color.Fore.LIGHTCYAN_EX + "Analyzing Tiles... this may take some time, please wait...")
        print("(Optionally, you can CTRL-C now and use the --verbose option to see the progress)")

    # Run the validations for each Tile
    for tile in tiles:
        err_count = len(errors)

        if verbose:
            if args.verbosity > 2: print()
            print("Analyzing Tile {:.<33} ".format(tile), end=(os.linesep if args.verbosity > 2 else ""))

        errors.extend(Tile(tile, dir=tiles_dir, verbose=args.verbosity).validate())

        if len(errors) == err_count:
            if args.verbosity == 2: print(color.Fore.GREEN + "OKAY")
        else:
            if args.verbosity == 2: print(color.Fore.RED + "ERROR")
            bad_tiles[tile] = (len(errors) - err_count)

    err_count = len(errors)

    if args.verbosity > 0:
        print(os.linesep + "Scanned {}... ".format(pluralize(tiles_count, "Tile")), end="")

        if err_count == 0:
            print(color.Fore.LIGHTGREEN_EX + "All OKAY")
        else:
            bad_tiles_count = len(bad_tiles)
            bad_tiles_string = pluralize(bad_tiles_count, "tile")
            err_count_string = pluralize(err_count, "error")

            print(color.Fore.LIGHTRED_EX + "Found {} with {} in total".format(
                bad_tiles_string, err_count_string
            ))

            with open("{}.error.log".format(PROGRAM_SHORT), "w") as f:
                print(os.linesep + "{} written to {}".format(err_count_string, f.name))
                for error in errors: f.write(error + os.linesep)

            print(os.linesep + "{} need attention".format(bad_tiles_string), file=sys.stderr)
            for (bad_tile_name, bad_tile_count) in bad_tiles.items():
                print("  -> {} ({})".format(
                    color.Fore.LIGHTWHITE_EX + bad_tile_name, pluralize(bad_tile_count, "error")),
                    file=sys.stderr
                )

    if args.pause:
        input(os.linesep + "Press ENTER key to exit")

    sys.exit(err_count)


if __name__ == "__main__": main()
