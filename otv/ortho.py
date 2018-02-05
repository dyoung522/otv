import os
import re
import colorama as color


class Tile:
    DIRECTORIES = ["earth nav data", "terrain", "textures"]

    lat = None
    long = None
    tile_dir = None
    tile_name = None
    water_only = False
    opts = {}

    def __init__(self, tile, dir, **opts):
        self.tile_name = tile
        self.tile_dir = os.path.join(dir, self.tile_name)
        (self.lat, self.long) = re.findall("([+-]\d+)", self.tile_name.lstrip("zOrtho4XP_").strip())
        self.verbose = opts["verbose"] if "verbose" in opts else 0
        self.errors = list()
        self.textures = dict()

    def validate(self):
        for dir in self.DIRECTORIES:
            getattr(self, "validate_{}".format(re.sub("\s+", "_", dir)))()

        return self.errors

    def validate_dir(self, dir):
        path = os.path.join(self.tile_dir, dir)

        if self.verbose > 2: print("  Validating {:.<35} ".format(dir.upper() + " directory"), end="")

        if not os.path.isdir(path):
            if dir != "terrain":
                if self.verbose > 2: print(color.Fore.RED + "NOT FOUND")
                self.errors.append("Directory \"{}\" NOT FOUND".format(dir))

            return False

        if not os.listdir(path):
            if self.verbose > 2: print(color.Fore.RED + "IS EMPTY")
            self.errors.append("Directory \"{}\" IS EMPTY".format(dir))
            return False

        if self.verbose > 2: print(color.Fore.GREEN + "OKAY")

        return True

    def validate_earth_nav_data(self):
        if not self.validate_dir("earth nav data"):
            return False

        return True

    def validate_terrain(self):
        no_errors_found = True
        path = os.path.join(self.tile_dir, "terrain")

        self.textures = dict(terrain_check=True)

        # May not exist (e.g. Water only tile)
        # if os.path.isdir(path):
        if not self.validate_dir("terrain"):
            self.water_only = True
            if self.verbose > 2: print(color.Fore.YELLOW + "Water Only? (if Textures are okay, this is safe to ignore)")
            return True

        if self.verbose > 2:
            print("  Validating {:.<35} ".format("TERRAIN DATA"), end=(os.linesep if self.verbose > 3 else ""))

        for terrain_file in sorted(os.listdir(path)):

            if self.verbose > 3: print("    Checking {:.<35} ".format(terrain_file), end="")

            with open(os.path.join(path, terrain_file)) as tf:
                texture_data = tf.read()

            try:
                texture_file = os.path.basename(re.search("../textures/(.+\.dds)", texture_data)[0])
                texture_path = os.path.join(self.tile_dir, "textures", texture_file)

                if not os.path.exists(texture_path):
                    no_errors_found = False
                    if self.verbose > 3: print(color.Fore.RED + "NO REFERENCE IN TEXTURES")
                    if texture_file not in self.textures:
                        self.errors.append("Terrain points to {}, which does not exist".format(texture_file))
                else:
                    if self.verbose > 3: print(color.Fore.GREEN + "OKAY")

                self.textures[texture_file] = None
            except TypeError:
                no_errors_found = False
                if self.verbose > 3: print(color.Fore.RED + "NO TEXTURES FOUND")
                self.errors.append("Terrain {} does not reference any Textures".format(terrain_file))

        if 2 < self.verbose <= 3:
            if no_errors_found:
                print(color.Fore.GREEN + "OKAY")
            else:
                print(color.Fore.RED + "ERROR")

        return no_errors_found

    def validate_textures(self):
        texture_count = 0
        no_errors_found = True
        path = os.path.join(self.tile_dir, "textures")

        if not self.validate_dir("textures"): return False

        if "terrain_check" not in self.textures: raise RuntimeError("Textures called before Terrains")

        if self.verbose > 2:
            print("  Validating {:.<35} ".format("TEXTURES DATA"), end=(os.linesep if self.verbose > 3 else ""))

        for texture_file in sorted(os.listdir(path)):
            if re.match(".*\.dds", texture_file) is None: continue

            texture_count += 1

            if self.verbose > 3: print("    Checking {:.<35} ".format(texture_file), end="")

            if texture_file not in self.textures:
                no_errors_found = False

                if self.verbose > 3: print(color.Fore.RED + "ERROR")

                if self.water_only:
                    if 2 < self.verbose <= 3:
                        print(color.Fore.RED + "ERROR")

                    self.errors.append("Textures were found, but no TERRAIN directory exists")
                    return False  # no need to check the remaining files
                else:
                    self.errors.append(
                        "Texture file {} exists, but was not referenced".format(texture_file))
            else:
                if self.verbose > 3: print(color.Fore.GREEN + "OKAY")

        if texture_count == 0 and self.verbose > 3:
            if self.water_only:
                print("    {:.<44} {}".format("Water Only Tile", color.Fore.GREEN + "OKAY"))
            else:
                print("    {:.<44} {}".format("NO TEXTURE DATA", color.Fore.RED + "ERROR"))

        if 2 < self.verbose <= 3:
            if no_errors_found:
                print(color.Fore.GREEN + "OKAY")
            else:
                print(color.Fore.RED + "ERROR")

        return no_errors_found
