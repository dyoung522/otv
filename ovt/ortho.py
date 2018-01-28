import os
import re
import colorama as color


class Tile:
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

        print("Analyzing {}... ".format(self.tile_name))

        print("  Directories...")

        for dir in self.directories():
            print("    {} -> ".format(dir), end="")

            if not os.path.isdir(f"{self.tile_dir}/{dir}"):
                print(color.Fore.RED + "Not Found!")
                errors.append("Directory \"{}\" for Tile {} NOT FOUND".format(dir, self.tile_name))
            else:
                print(color.Fore.GREEN + "Okay")

        return errors
