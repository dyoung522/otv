=======================
Ortho4XP Tile Validator
=======================

Have you:

- Built dozens if not hundreds of Ortho4XP tiles, but now get mysterious crashes
  when scenery tries to load?
- Had your Ortho4XP process crash during the night and don't know which tiles
  completed successfully?

I have. So I wrote a utility to scan through all the Ortho4XP tiles and validate
them, reporting any tiles that have errors so I can fix them in Ortho4XP.


Installation
____________

If you already have Python(v3) installed and working, you can use ``pip3`` to
install::

    $ pip3 install otv

This will install an executable named **otv**, so if your PATH is setup
correctly you should be able to simply run ``otv`` from your system's command line.


Getting Started
---------------

It's written in python (which is also a dependency of Ortho4XP) so, assuming you
have a working python installation, simply run pip3 install otv - that will
create a command line utility for you named otv.

Running otv without any additional arguments will give you a help message, but
to jump right into it, give it your Ortho4XP directory and it'll start scanning:
e.g: ``otv path_to_your_ortho4XP_directory``

There are other options, which you can see with ``otv --help``::

    usage: Ortho4XP Tile Validator [-h] [-P] [-q | -v] [-V] [tile_directory]

    Scan all Ortho4XP Tiles and report any problems

    positional arguments:
      tile_directory  Directory where Tiles are stored (usually your Ortho4XP dir)
                      - If not provided; use the current directory

    optional arguments:
      -h, --help      show this help message and exit
      -P, --pause     Pause the program before exiting (good for batch files)
      -q, --quiet     Suppresses all output; exit value indicates errors found
      -v, --verbose   Increase output verbosity (may be repeated)
      -V, --version   show program's version number and exit

More Info
---------

Currently, it'll check for things like:

- missing or empty data directories (Earth Nav Data, Terrain, Textures)
- missing references to textures from each terrain file
- textures which exist but aren't referenced from a terrain

You can find the `pip page here <https://pypi.python.org/pypi/otv>`_
and the `source code here <https://github.com/dyoung522/otv>`_

Both provide downloads if you don't have a working pip, or prefer to install
from the package.

It's currently in beta, so if you're interested, please try it out and let me
know how it works for you. I would appreciate any feedback and/or bug reports.

