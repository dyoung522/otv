#! env python

import colorama as color
import os
import re
import sys

# Constants

AUTHOR = "Donovan C. Young"
ORTHO = "Ortho4XP"
PROGRAM = "{} Tile Validator".format(ORTHO)
VERSION = "0.0.3"

# Global variables

ortho_dir = None


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
    print("When given a valid {} directory, this program will scan all Tiles and report any problems it finds.".format(
        ORTHO))
    print(color.Style.BRIGHT + "\nUsage: {} <{} directory>".format(sys.argv[0], ORTHO))

    exit()


# Classes

class Version:
    program_name = None

    def __init__(self):
        self.program_name = os.path.basename(sys.argv[0]).rstrip(".py")

    def __format__(self, format_spec):
        return "{} ({}) v{} - written by {}".format(PROGRAM, self.program_name, VERSION, AUTHOR)


class OrthoTile:
    lat = None
    long = None
    tile_dir = None
    tile_name = None

    def __init__(self, tile):
        self.tile_name = tile
        self.tile_dir = f"Tiles/{self.tile_name}"
        (self.lat, self.long) = re.findall("([+-]\d+)", self.tile_name.lstrip("zOrtho4XP_").strip())

    def directories(self):
        return ["earth nav data", "terrain", "textures"]

    def validate(self):
        errors = []

        print(f"Analyzing {self.tile_name}... ")

        print("  Directories...")
        for dir in self.directories():
            print("    {} -> ".format(dir), end="")

            if not os.path.isdir(f"{self.tile_dir}/{dir}"):
                print(color.Fore.RED + "Not Found!")
                errors.append("Directory \"{}\" for Tile {} NOT FOUND".format(dir, self.tile_name))
            else:
                print(color.Fore.GREEN + "Okay")

        return errors


########
# MAIN #
########
if __name__ == '__main__':
    errors = []

    setup()  # Initialize the program

    if not os.path.isdir(ortho_dir): usage("Please provide a valid {} directory".format(ORTHO))

    os.chdir(ortho_dir)

    if not os.path.exists("Tiles"):
        usage("\"{}\" does not appear to be a valid {} directory, if it is, I cannot find any Tiles.".format(
            ortho_dir, ORTHO))

    for tile in os.listdir("Tiles"):
        errors.extend(OrthoTile(tile).validate())

    print()
    if len(errors) == 0:
        print(color.Fore.LIGHTGREEN_EX + "All Tiles OKAY")
    else:
        print(color.Fore.LIGHTRED_EX + "Errors Found:")
        for error in errors:
            print("  ->", error)

    color.deinit()  # Colorama
