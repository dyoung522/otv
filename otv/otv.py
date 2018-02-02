import atexit
import colorama as color
import os
import sys

from .argparse import ArgParse
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
    tile_count = 0

    atexit.register(cleanup)

    color.init(autoreset=True)  # Colorama

    argparse = ArgParse(epilog=VERSION_STR, prog=PROGRAM)

    args = argparse.args
    help_message = argparse.help

    tile_dir = os.path.join(args.tile_directory, "Tiles")

    vquiet = args.verbosity == 0
    vnormal = args.verbosity >= 1
    verbose = args.verbosity > 1

    if not os.path.isdir(args.tile_directory):
        usage(help_message,
              "Please provide a directory where Ortho4XP Tiles can be found"
              )

    if not os.path.exists(tile_dir):
        usage(help_message,
              "\"{}\" does not appear to be a valid Ortho4XP directory, or if it is, I cannot find any Tiles."
              .format(args.tile_directory),
              args.verbosity
              )

    os.chdir(args.tile_directory)

    if not vquiet: print(VERSION_STR + os.linesep)

    if vnormal:
        print(color.Fore.LIGHTCYAN_EX + "Analyzing Tiles... this may take some time, please wait...")
        print("(Optionally, you can CTRL-C now and use the --verbose option to see the progress)")
        
    # Run the validations for each Tile
    for tile in sorted(os.listdir(tile_dir)):
        tile_count += 1
        err_count = len(errors)

        if verbose:
            print("Analyzing Tile {:.<33} ".format(tile), end=(os.linesep if args.verbosity > 2 else ""))

        errors.extend(Tile(tile, verbose=args.verbosity).validate())

        if len(errors) == err_count:
            if args.verbosity == 2: print(color.Fore.GREEN + "OKAY")
        else:
            if args.verbosity == 2: print(color.Fore.RED + "ERROR")
            bad_tiles[tile] = (len(errors) - err_count)

    if vnormal:
        err_count = len(errors)
        
        print(os.linesep + "Scanned {}... ".format(pluralize(tile_count, "Tile")), end="")

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
                for error in errors: f.write(error)

            print(os.linesep + "{} need attention".format(bad_tiles_string))
            for (bad_tile_name, bad_tile_count) in bad_tiles.items():
                print("  -> {} ({})".format(
                    color.Fore.LIGHTWHITE_EX + bad_tile_name, pluralize(bad_tile_count, "error")),
                    file=sys.stderr
                )

    sys.exit(err_count)
