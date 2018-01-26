#! env python

import colorama as color
import os
import re
import sys

# Constants

AUTHOR = "Donovan C. Young"
VERSION = "0.0.2"
PROGRAM = "Ortho4XP Tile Validator"

# Global variables

errors = []
ortho_dir = None
tiles = []


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
    print("When given a valid Ortho4 directory, this program will scan all Tiles and report any problems it finds.")
    print(color.Style.BRIGHT + f"\nUsage: {sys.argv[0]} <Ortho4XP-directory>")

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

    def validate(self):
        errors = []

        print(f"Analyzing {self.tile_name}...", end="")

        if not os.path.isdir(f"{self.tile_dir}/earth nav data"): errors.append('No "Earth Nav Data" directory found')
        if not os.path.isdir(f"{self.tile_dir}/terrain"): errors.append('No terrain directory found')
        if not os.path.isdir(f"{self.tile_dir}/terrain"): errors.append('No textures directory found')

        if len(errors) != 0:
            print(color.Fore.RED + " Errors!")
            for error in errors:
                print("  ->", color.Fore.RED + error)
            print()
        else:
            print(" Okay")


########
# MAIN #
########
if __name__ == '__main__':
    setup()  # Initialize the program

    if not os.path.isdir(ortho_dir): usage("Please provide a valid Ortho4 directory")

    os.chdir(ortho_dir)

    if not os.path.exists("Tiles"):
        usage(f"'{ortho_dir}' does not appear to be a valid Ortho directory, if it is, I cannot find any Tiles.")

    tiles.extend(os.listdir("Tiles"))

    for tile in tiles:
        OrthoTile(tile).validate()

    color.deinit()  # Colorama
