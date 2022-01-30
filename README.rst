Cleaning up Creo Parametric versioned files
###########################################

:date: 2015-05-10
:author: Roland Smith

.. Last modified: 2022-01-30T18:38:42+0100


Introduction
============

The `Creo Parametric`_ software (f.k.a. Pro/Engineer) saves its files as numbered
versions. While this is in itself commendable (it's nice to be able to
roll-back to a previously known good version of a file) it is an old-fashioned
approach in the age of modern revision control software such as e.g. git_.
If you save often when working in Creo (which is generally a good idea) you
end up with lots of versions of the same file.

.. _Creo Parametric: http://www.ptc.com/cad/3d-cad/creo-parametric
.. _git: http://git-scm.com/

So I wrote a script to help clean up this mess. For obvious reasons it is
called ``creoclean``.


.. NOTE::

    On ``posix`` platforms like Linux, BSD and OSX, the script is installed
    without an extension. On MS windows platforms, the scripts needs to be
    installed as ``creoclean.py`` so that it is linked to the Python program
    that has to run it. So of you are on the windows platform, please read
    ``creoclean.py`` whereever you see ``creoclean``.

License
-------

This program is licensed under the `MIT`_ license.

.. _MIT: http://opensource.org/licenses/MIT


Usage
=====

.. NOTE::

    You should probably *close all open files* in the directory *and* purge
    them from the Creo session *before* running this script in a directory!

You can use this program basically in two ways::

    creoclean

This cleans up the current working directory. Or you can use::

    creoclean <dir1> <dir2> ...

This cleans up the directories named on the command line.

Options
-------

The ``-h`` option displays the online help.::

    > creoclean -h
    usage: creoclean [-h] [-d] [-v] [--log {debug,info,warning,error}]
                    [dir [dir ...]]

    Cleans up Creo versioned files in the named diratories or in the current
    working directory. Removes all versions except the last one, and renames that
    to version 1.

    positional arguments:
    dir                   one or more directories to process

    optional arguments:
    -h, --help            show this help message and exit
    -d                    dry run; show what would be done but don't delete
                            files
    -v, --version         show program's version number and exit
    --log {debug,info,warning,error}
                            logging level (defaults to 'warning')

The ``-d`` option makes the program perform a dry run. This means that all
actions are listed but not carried out.::

    > creoclean -d ~/tmp/spam-eggs/
    INFO: DRY RUN, no files will be deleted or renamed
    INFO: cleaning in '/home/jdoe/tmp/spam-eggs/'
    INFO: found 21 files
    INFO: not enough 'asm' files; skipping
    INFO: found 9 'prt' files
    INFO: found 2 unique 'prt' file names
    INFO: removing 'spamshaper.prt.10'
    INFO: removing 'spamshaper.prt.11'
    INFO: removing 'spamshaper.prt.12'
    INFO: renaming 'spamshaper.prt.13' to 'spamshaper.prt.1'
    INFO: removing 'eggcontainer.prt.5'
    INFO: removing 'eggcontainer.prt.6'
    INFO: removing 'eggcontainer.prt.7'
    INFO: removing 'eggcontainer.prt.8'
    INFO: renaming 'eggcontainer.prt.9' to 'eggcontainer.prt.1'

You can see the same information during a real run by specifying the
``--log info`` option.

Installation
============

Requirements
------------

This script requires Python 3. It has been developed and tested on Python 3.4.
It has no further dependencies outside of the Python standard library.

General
-------

To install it for the local user, run::

    python setup.py install

This will install it in the user path for Python scripts.
For POSIX operating systems this is ususally ``~/.local/bin``.
For ms-windows this is the ``Scripts`` directory of your Python installation
or another local directory.
Make sure that this directory is in your ``$PATH`` environment variable.

Windows
-------

After installation, you can then call it from a ``cmd.exe`` window, if the ``.py``
extension is associated with a filetype, and the filetype has an appropriate
action defined.  If trying to run ``creoclean.py`` gives an error, try
executing the following commands in a ``cmd.exe`` window::

    assoc .py=Python.File
    ftype Python.File="C:\Anaconda3\python.exe" "%1" %*

Note that ``C:\Anaconda3`` is just an example! You should of course substitute
the real path to your ``python.exe``.

Linux, the BSD variants and OS-X
--------------------------------

The installation program copies ``creoclean`` to ``~/.local/bin``.
Make sure that directory is in your ``$PATH``.
