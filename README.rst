Ortho4XP Tile Validator
=======================

Have you:

-  Built dozens if not hundreds of Ortho4XP tiles, but now get
   mysterious crashes when scenery tries to load?
-  Had your Ortho4XP process crash during the night and don't know which
   tiles completed successfully?

I have. So I wrote a utility to scan through all the Ortho4XP tiles and
validate them, reporting any tiles that have errors so I can fix them in
Ortho4XP.

Installation
~~~~~~~~~~~~

If you already have Python(v3) installed and working, you can use
``pip3`` to install:

::

    $ pip3 install otv

Otherwise, head over to `GitHub <https://github.com/dyoung522/otv>`__ or
`PyPi <https://pypi.python.org/pypi/otv>`__ and download the latest
release.

Getting Started
~~~~~~~~~~~~~~~

There are three ways to run the program:

1. If you installed via the ``pip3`` installer, you'll have an
   executable named **otv** available, so you should be able to:

   1. cd into your Ortho4XP directory
   2. run ``otv``

2. Download the latest release from
   `PyPi <https://pypi.python.org/pypi/otv>`__ or
   `GitHub <https://github.com/dyoung522/otv>`__ and extract it into a
   folder. From the command line, run:

   ::

       python3 bin/otv YourOrtho4XPdir

   *(Obviously; change "YourOrtho4XPdir" to wherever you've stored your
   Ortho Tiles)*

3. If you're on windows, and prefer an EXE, download the latest release
   from `GitHub <https://github.com/dyoung522/otv>`__ or
   `PyPi <https://pypi.python.org/pypi/otv>`__, then:

   1. Extract the package (anywhere on your filesystem)
   2. Create a shortcut from ``bin/otv.exe`` on your desktop (*must* be
      a shortcut).
   3. Go to the *Properties* of the **shortcut** and change the "Start
      In" field to point to your Ortho4XP directory.

   Then you can simply double click the shortcut to run the utility
   anytime.

More Info
~~~~~~~~~

-  Running otv without any additional arguments will give you a help
   message:

   ::

       usage: Ortho4XP Tile Validator [-q | -v] [-p | --no-pause] [--no-progress]
                                      [-h] [--version]
                                      [tile_directory]

       Scan all Ortho4XP Tiles and report any problems

       positional arguments:
         tile_directory     Directory where Tiles are stored (usually your Ortho4XP
                            dir) - If not provided; will use the current directory

       display output:
         -q, --quiet        Suppresses all output; exit value indicates errors found
         -v, -V, --verbose  Increase verbosity (repeat to increase verbosity more)

       alter defaults:
         -p, -P, --pause    Pause the program before exiting (default for Windows)
         --no-pause         Disable auto-pause
         --no-progress      Disables the progress bar display

       help and information:
         -h, --help         show this help message and exit
         --version          show program's version number and exit

-  Currently, it checks for things like:

   -  missing or empty data directories (Earth Nav Data, Terrain,
      Textures)
   -  missing references to textures from each terrain file
   -  textures which exist but aren't referenced from a terrain

-  You can find the pip page on
   `PyPi <https://pypi.python.org/pypi/otv>`__ and the source code on
   `GitHub <https://github.com/dyoung522/otv>`__ (both provide package
   downloads)

OTV is currently in beta, so if you're interested, please try it out and
let me know how it works for you. I would appreciate any feedback and/or
bug reports.

Known Issues
~~~~~~~~~~~~

-  On Windows, the utility will pause after each run, even if running
   from a command line. This is done because most Windows users will be
   running the util from a Shortcut, so the pause is necessary without
   having to specifically add it. You can use the ``--no-pause`` option
   to disable this functionality
