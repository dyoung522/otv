import colorama as color
import os
import sys
from .ortho import Tile
from .util import pluralize
from .argparse import ArgParse

# Global variables

AUTHOR = "Donovan C. Young"
ORTHO = "Ortho4XP"
PROGRAM = "{} Tile Validator".format(ORTHO)
VERSION = "0.2.1-dev"

global args


# Classes

class Version:
    program_name = None

    def __init__(self):
        self.program_name = os.path.basename(sys.argv[0]).rstrip(".py")

    def __format__(self, format_spec):
        return "{} ({}) v{} - written by {}".format(PROGRAM, self.program_name, VERSION, AUTHOR)


# Functions

def log(message, verbosity=0, newline=True):
    global args

    extra_opts = dict()

    if not newline:
        extra_opts = dict(end="")

    if args.verbose > verbosity:
        print(message, **extra_opts)


def usage(help_message, error_message=""):
    if error_message != "": log(color.Fore.RED + color.Style.BRIGHT + f"!!! {error_message} !!!\n")
    log(help_message)
    exit()


# Main

def main():
    global args

    errors = []
    tile_count = 0

    color.init(autoreset=True)  # Colorama

    argparse = ArgParse(version=f"{Version()}")

    args = argparse.args
    help_message = argparse.help

    if args.quiet: args.verbose = 0

    if not os.path.isdir(args.tile_directory): usage(help_message, "Please provide a valid {} directory".format(ORTHO))

    os.chdir(args.tile_directory)

    if not os.path.exists("Tiles"):
        usage(help_message, "\"{}\" does not appear to be a valid {} directory, if it is, I cannot find any Tiles."
              .format(args.tile_directory, ORTHO))

    # Run the validations for each Tile
    for tile in os.listdir("Tiles"):
        tile_count += 1
        err_count = len(errors)

        log("Analyzing Tile ", newline=False)
        if args.verbose == 1:
            log("{:.<25} ".format(tile), newline=False)
        else:
            log("{}".format(tile))

        errors.extend(Tile(tile, {"verbose": args.verbose}).validate())

        if len(errors) == err_count:
            if args.verbose == 1: log(color.Fore.GREEN + "OKAY")
        else:
            if args.verbose == 1: log(color.Fore.RED + "ERROR")

    log("\nScanned {}... ".format(pluralize(tile_count, "Tile")), newline=False)

    err_count = len(errors)
    if err_count == 0:
        log(color.Fore.LIGHTGREEN_EX + "All OKAY")
    else:
        log(color.Fore.LIGHTRED_EX + "Found {}:".format(pluralize(err_count, "Error")))
        for error in errors:
            log("  -> {}".format(error))

    color.deinit()  # Colorama

    exit(err_count)
