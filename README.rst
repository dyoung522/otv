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

Otherwise, head over to GitHub_ or PyPi_ and download the latest release.


Getting Started
---------------

There are three ways to run the program:

#. If you installed via the ``pip3`` installer, you'll have an executable named
   **otv** available, so you should be able to:

   #. cd into your Ortho4XP directory
   #. run ``otv``

#. Download the latest release from PyPi_ or GitHub_ and extract it into a
   folder. From the command line, run::

    python3 bin/ovt YourOrtho4XPdir

   *(Obviously; change "YourOrtho4XPdir" to wherever you've stored your
   Ortho Tiles)*

#. If you're on windows, and prefer an EXE, download the latest release from
   the GitHub_ Releases page, then:

   #. Extract and unzip ``bin/otv.exe.zip`` (save it anywhere)
   #. Create a shortcut to the unzipped ``otv.exe`` on your desktop
      (**must** be a shortcut).
   #. Go to the *Properties* of the shortcut and change the "Start In" field to
      point to your Ortho4XP directory.
   #. In the Target field, add a " -P" on the end of the command
      (i.e. "... otv.exe -P") - along with any other options you would like.

   Then you can simply double click the shortcut to run the utility anytime.


More Info
---------

- Running otv without any additional arguments will give you a help message::

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

- Currently, it checks for things like:

  - missing or empty data directories (Earth Nav Data, Terrain, Textures)
  - missing references to textures from each terrain file
  - textures which exist but aren't referenced from a terrain

- You can find the pip page on PyPi_ and the source code on GitHub_ (both
  provide package downloads)

OTV is currently in beta, so if you're interested, please try it out and let me
know how it works for you. I would appreciate any feedback and/or bug reports.

.. _PyPi: https://pypi.python.org/pypi/otv
.. _GitHub: https://github.com/dyoung522/otv
