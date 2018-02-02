import argparse


class ArgParse:
    help = None
    args = None

    def __init__(self, **opts):
        parser = argparse.ArgumentParser(description="""Scan all Ortho4XP Tiles and report any problems""", **opts)

        # Positional Arguments
        parser.add_argument("tile_directory",
                            nargs="?",
                            default=".",
                            help="Directory where Tiles are stored (usually your Ortho4XP dir)")

        # Optional Arguments
        parser.add_argument("-V", "--version", action="version", version=opts["epilog"])

        group = parser.add_mutually_exclusive_group()
        group.add_argument("-v", "--verbose", dest="verbosity", action="count", default=1,
                           help="Increase output verbosity (may be repeated)")
        group.add_argument("-q", "--quiet", action="store_true",
                           help="Suppresses all output; exit value indicates errors found.")

        self.args = parser.parse_args()
        self.help = parser.format_help()

        self.args.tile_directory = self.args.tile_directory.rstrip("/\\")

        if self.args.quiet: self.args.verbosity = 0
