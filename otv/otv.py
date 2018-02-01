import colorama as color
import os

from .argparse import ArgParse
from .globals import *
from .ortho import Tile
from .util import *


# Main

def main():
    errors = []
    tile_count = 0

    color.init(autoreset=True)  # Colorama

    argparse = ArgParse(epilog=VERSION_STR, prog=PROGRAM)

    args = argparse.args
    help_message = argparse.help

    if args.quiet: args.verbosity = 0

    verbose = args.verbosity > 0

    if not os.path.isdir(args.tile_directory):
        usage(help_message,
              "Please provide a directory where Ortho4XP Tiles can be found"
              )

    os.chdir(args.tile_directory)

    if not os.path.exists("Tiles"):
        usage(help_message,
              "\"{}\" does not appear to be a valid Ortho4XP directory, or if it is, I cannot find any Tiles."
              .format(args.tile_directory),
              args.verbosity
              )

    # Run the validations for each Tile
    for tile in os.listdir("Tiles"):
        tile_count += 1
        err_count = len(errors)

        if verbose: log("Analyzing Tile ", end="")
        if args.verbosity == 1:
            log("{:.<25} ".format(tile), end="")
        else:
            if verbose: log("{}".format(tile))

        errors.extend(Tile(tile, {"verbose": args.verbosity}).validate())

        if len(errors) == err_count:
            if args.verbosity == 1: log(color.Fore.GREEN + "OKAY")
        else:
            if args.verbosity == 1: log(color.Fore.RED + "ERROR")

    if verbose: log("\nScanned {}... ".format(pluralize(tile_count, "Tile")), end="")

    err_count = len(errors)
    if err_count == 0:
        if verbose: log(color.Fore.LIGHTGREEN_EX + "All OKAY")
    else:
        if verbose: log(color.Fore.LIGHTRED_EX + "Found {}:".format(pluralize(err_count, "Error")))
        for error in errors:
            if verbose: log("  -> {}".format(error))

    color.deinit()  # Colorama

    exit(err_count)
