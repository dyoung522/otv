import colorama as color
import os
import sys
from .ortho import Tile

# Global variables

AUTHOR = "Donovan C. Young"
ORTHO = "Ortho4XP"
PROGRAM = "{} Tile Validator".format(ORTHO)
VERSION = "0.1.0"

ortho_dir = None


# Classes

class Version:
    program_name = None

    def __init__(self):
        self.program_name = os.path.basename(sys.argv[0]).rstrip(".py")

    def __format__(self, format_spec):
        return "{} ({}) v{} - written by {}".format(PROGRAM, self.program_name, VERSION, AUTHOR)


# Functions

def setup():
    global ortho_dir

    color.init(autoreset=True)  # Colorama

    try:
        ortho_dir = sys.argv[1]
    except:
        usage()


def usage(message=""):
    if message != "": print(color.Fore.RED + color.Style.BRIGHT + f"!!! {message} !!!")

    print()
    print(f"{color.Fore.LIGHTGREEN_EX}{Version()}\n")
    print("""When given a valid {} directory, this program will scan all Tiles and report any problems it finds."""
          .format(ORTHO))
    print(color.Style.BRIGHT + "\nUsage: {} <{} directory>".format(sys.argv[0], ORTHO))

    exit()


# Main

def main():
    errors = []

    setup()  # Initialize the program

    if not os.path.isdir(ortho_dir): usage("Please provide a valid {} directory".format(ORTHO))

    os.chdir(ortho_dir)

    if not os.path.exists("Tiles"):
        usage("\"{}\" does not appear to be a valid {} directory, if it is, I cannot find any Tiles."
              .format(ortho_dir, ORTHO))

    for tile in os.listdir("Tiles"):
        errors.extend(Tile(tile).validate())

    print()
    if len(errors) == 0:
        print(color.Fore.LIGHTGREEN_EX + "All Tiles OKAY")
    else:
        print(color.Fore.LIGHTRED_EX + "Errors Found:")
        for error in errors:
            print("  ->", error)

    color.deinit()  # Colorama
