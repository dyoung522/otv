import argparse
import os


class ArgParse:
    help = None
    args = None

    def __init__(self, **opts):
        parser = argparse.ArgumentParser(description="""Scan all Ortho4XP Tiles and report any problems""",
                                         add_help=False, **opts)

        # Positional Arguments
        parser.add_argument("tile_directory",
                            nargs="?",
                            default=".",
                            help="Directory where Tiles are stored (usually your Ortho4XP dir) - " +
                                 "If not provided; will use the current directory")

        # Optional Arguments
        output_group = parser.add_argument_group("display output")
        verbose_group = output_group.add_mutually_exclusive_group()
        verbose_group.add_argument("-q", "--quiet", action="store_true",
                                   help="Suppresses all output; exit value indicates errors found")
        verbose_group.add_argument("-v", "-V", "--verbose", dest="verbosity", action="count", default=1,
                                   help="Increase verbosity (repeat to increase verbosity more)")

        defaults_group = parser.add_argument_group("alter defaults")

        pause_group = defaults_group.add_mutually_exclusive_group()
        pause_group.add_argument("-p", "-P", "--pause", action="store_true",
                                 help="Pause the program before exiting (default for Windows)")
        pause_group.add_argument("--no-pause", dest="pause", action="store_false",
                                 help="Disable auto-pause")

        defaults_group.add_argument("--no-progress", dest="progress_bar", action="store_false", default=True,
                                    help="Disables the progress bar display")

        info_group = parser.add_argument_group("help and information")
        info_group.add_argument("-h", "--help", action="help", help="show this help message and exit")
        info_group.add_argument("--version", action="version", version=opts["epilog"])

        self.args = parser.parse_args()
        self.help = parser.format_help()

        self.args.tile_directory = self.args.tile_directory.rstrip("/\\")

        if self.args.quiet:
            self.args.verbosity = 0
            self.progress_bar = False
