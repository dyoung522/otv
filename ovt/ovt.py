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
    ortho_dir = None

    color.init(autoreset=True)  # Colorama

    try:
        ortho_dir = sys.argv[1]
    except:
        usage()

    if not os.path.isdir(ortho_dir): usage("Please provide a valid {} directory".format(ORTHO))

    os.chdir(ortho_dir)

    if not os.path.exists("Tiles"):
        usage("\"{}\" does not appear to be a valid {} directory, if it is, I cannot find any Tiles."
              .format(ortho_dir, ORTHO))

    for tile in os.listdir("Tiles"):
        tile_count += 1
        errors.extend(Tile(tile).validate())

    print("\nScanned {}... ".format(pluralize(tile_count, "Tile", "Tiles")), end="")

    err_count = len(errors)
    if err_count == 0:
        print(color.Fore.LIGHTGREEN_EX + "All OKAY")
    else:
        print(color.Fore.LIGHTRED_EX + "Found {}:".format(pluralize(err_count, "Error", "Errors")))
        for error in errors:
            print("  ->", error)

    for c in range(0, 3):
        print(pluralize(c, "test", "tests"))
        
    color.deinit()  # Colorama
