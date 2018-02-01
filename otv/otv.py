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
    tile_count = 0

    atexit.register(cleanup)

    color.init(autoreset=True)  # Colorama

    argparse = ArgParse(epilog=VERSION_STR, prog=PROGRAM)

    args = argparse.args
    help_message = argparse.help

    tile_dir = os.path.join(args.tile_directory, "Tiles")
    verbose = args.verbosity > 0

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

    if verbose: log(VERSION_STR)

    # Run the validations for each Tile
    for tile in os.listdir(tile_dir):
        tile_count += 1
        err_count = len(errors)

        if verbose: log(os.linesep + "Analyzing Tile ", end="")
        if args.verbosity == 1:
            log("{:.<25} ".format(tile), end="")
        else:
            if verbose: log("{}".format(tile))

        errors.extend(Tile(tile, verbose=args.verbosity).validate())

        if len(errors) == err_count:
            if args.verbosity == 1: log(color.Fore.GREEN + "OKAY")
        else:
            if args.verbosity == 1: log(color.Fore.RED + "ERROR")

    if verbose: log(os.linesep + "Scanned {}... ".format(pluralize(tile_count, "Tile")), end="")

    err_count = len(errors)
    if err_count == 0:
        if verbose: log(color.Fore.LIGHTGREEN_EX + "All OKAY")
    else:
        if verbose: log(color.Fore.LIGHTRED_EX + "Found {}:".format(pluralize(err_count, "Error")))
        for error in errors:
            if verbose: log("  -> {}".format(error))

    sys.exit(err_count)
