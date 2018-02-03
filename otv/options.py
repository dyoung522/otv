import argparse
import os


class ArgParse:
    help = None
    args = None

    def __init__(self, **opts):
        parser = argparse.ArgumentParser(description="""Scan all Ortho4XP Tiles and report any problems""", **opts)

        # Positional Arguments
        parser.add_argument("tile_directory",
                            nargs="?",
                            default=".",
                            help="Directory where Tiles are stored (usually your Ortho4XP dir) - " +
                                 "If not provided; use the current directory")

        # Optional Arguments
        parser.add_argument("-P", "--pause", action="store_true",
                            help="Pause the program before exiting (good for batch files)")

        group = parser.add_mutually_exclusive_group()
        group.add_argument("-q", "--quiet", action="store_true",
                           help="Suppresses all output; exit value indicates errors found")
        group.add_argument("-v", "--verbose", dest="verbosity", action="count", default=1,
                           help="Increase output verbosity (may be repeated)")

        parser.add_argument("-V", "--version", action="version", version=opts["epilog"])

        self.args = parser.parse_args()
        self.help = parser.format_help()

        self.args.tile_directory = self.args.tile_directory.rstrip("/\\")

        if self.args.quiet: self.args.verbosity = 0
