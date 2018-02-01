import os
import re
import colorama as color


class Tile:
    DIRECTORIES = ["earth nav data", "terrain", "textures"]

    lat = None
    long = None
    tile_dir = None
    tile_name = None
    opts = {}
    errors = []

    def __init__(self, tile, **opts):
        self.tile_name = tile
        self.tile_dir = os.path.join("Tiles", self.tile_name)
        (self.lat, self.long) = re.findall("([+-]\d+)", self.tile_name.lstrip("zOrtho4XP_").strip())
        self.opts["verbose"] = opts["verbose"] if "verbose" in opts else 0

    def validate(self):
        for dir in self.DIRECTORIES:
            if self.opts["verbose"] > 1: print("  directory {:.<20}".format(dir), end="")
            if getattr(self, "validate_{}".format(re.sub("\s+", "_", dir)))():
                if self.opts["verbose"] > 1: print(color.Fore.GREEN + " OKAY")
            else:
                if self.opts["verbose"] > 1: print(color.Fore.RED + " ERROR")

        return self.errors

    def validate_dir(self, dir):
        path = os.path.join(self.tile_dir, dir)

        if not os.path.isdir(path):
            self.errors.append("Directory \"{}\" for Tile {} NOT FOUND".format(dir, self.tile_name))
            return False

        if not os.listdir(path):
            self.errors.append("Directory \"{}\" for Tile {} IS EMPTY".format(dir, self.tile_name))
            return False

        return True

    def validate_earth_nav_data(self):
        if not self.validate_dir("earth nav data"):
            return False

        return True

    def validate_terrain(self):
        no_errors_found = True
        path = os.path.join(self.tile_dir, "terrain")

        # May not exist (e.g. Water only tile)
        if os.path.isdir(path):
            for terrain_file in os.listdir(path):
                texture_file = os.path.basename(
                    re.search("../textures/(.+\.dds)", open(os.path.join(path, terrain_file)).read())[0])
                texture_path = os.path.join(self.tile_dir, "textures", texture_file)

                if not os.path.exists(texture_path):
                    no_errors_found = False
                    self.errors.append(
                        "Terrain for Tile {} points to {}, which does not exist".format(self.tile_name, texture_file))

        return no_errors_found

    def validate_textures(self):
        if not self.validate_dir("textures"):
            return False

        return True
