import colorama as color
import os
import sys
from .ortho import Tile
from .util import pluralize

# Global variables

AUTHOR = "Donovan C. Young"
ORTHO = "Ortho4XP"
PROGRAM = "{} Tile Validator".format(ORTHO)
VERSION = "0.1.0"


# Classes

class Version:
    program_name = None

    def __init__(self):
        self.program_name = os.path.basename(sys.argv[0]).rstrip(".py")

    def __format__(self, format_spec):
        return "{} ({}) v{} - written by {}".format(PROGRAM, self.program_name, VERSION, AUTHOR)


# Functions

def usage(message=""):
    if message != "":
        print(color.Fore.RED + color.Style.BRIGHT + f"!!! {message} !!!")

    print()
    print(f"{color.Fore.LIGHTGREEN_EX}{Version()}\n")
    print("""When given a valid {} directory, this program will scan all Tiles and report any problems it finds."""
          .format(ORTHO))
    print(color.Style.BRIGHT + "\nUsage: {} <{} directory>".format(sys.argv[0], ORTHO))

    exit()


# Main

def main():
    errors = []
    tile_count = 0

    color.init(autoreset=True)  # Colorama

    # ToDo: Make these command line arguments
    ortho_dir = None
    verbose = 1

    try:
        ortho_dir = sys.argv[1]
    except:
        usage()

    if not os.path.isdir(ortho_dir): usage("Please provide a valid {} directory".format(ORTHO))

    os.chdir(ortho_dir)

    if not os.path.exists("Tiles"):
        usage("\"{}\" does not appear to be a valid {} directory, if it is, I cannot find any Tiles."
              .format(ortho_dir, ORTHO))

    # Run the validations for each Tile
    for tile in os.listdir("Tiles"):
        tile_count += 1
        err_count = len(errors)

        print("Analyzing Tile {:.<25} ".format(tile), end="")
        if verbose > 1: print("validating...")

        errors.extend(Tile(tile, {"verbose": verbose > 1}).validate())

        if len(errors) == err_count:
            if verbose == 1: print(color.Fore.GREEN + "OKAY")
        else:
            if verbose == 1: print(color.Fore.RED + "ERROR")

    print("\nScanned {}... ".format(pluralize(tile_count, "Tile")), end="")

    err_count = len(errors)
    if err_count == 0:
        print(color.Fore.LIGHTGREEN_EX + "All OKAY")
    else:
        print(color.Fore.LIGHTRED_EX + "Found {}:".format(pluralize(err_count, "Error")))
        for error in errors:
            print("  ->", error)

    color.deinit()  # Colorama
