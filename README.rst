Cleaning up Creo Parametric versioned files
###########################################

:date: 2022-02-12
:author: Roland Smith

.. Last modified: 2022-02-14T22:21:17+0100


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
called ``creoclean.pyw``.

As of version 2022.02.11, it is a GUI program, mainly meant for use on
ms-windows.


License
-------

This program is licensed under the `MIT`_ license.

.. _MIT: http://opensource.org/licenses/MIT


Usage
=====

.. Warning::

    You should *close all open Creo files* in the directory and *erase
    them from the Creo session* **before** running this script on a directory!

Start ``creoclean``, e.g. from a link on your desktop. It will look like as
shown below.

.. image:: screenshot.png
    :alt: screenshot of the GUI
    :width: 100%

* Select a directory to clean.
* Select the required options.

  * ``dry run`` does everything except the actual removal/renaming.
  * ``clean miscellaneous`` also cleans log and information files.

* Press ``Go!`` to start the cleaning process. This button will only be
  enabled after a directory is selected.
* The text window shows the progress of the cleanup operation.


Installation
============

Requirements
------------

This script requires Python 3.6 or later. It has been developed and tested on
Python 3.9.  It has no further dependencies outside of the Python standard
library.

Windows
-------

You should use either a default Python install, or a custom install with the
optional feature “tcl/tk and IDLE” enabled.

Clone this repo, or download the zip-file and unpack it.
Start ``cmd.exe``, and in it ``cd`` to the directory that contains the
contents of this repo.
Then run the following command from ``cmd.exe``::

    python setup.py install

This will install it in the user path for Python scripts.
It will print a message where it has installed the script.

For convenience, make a shortcut from the installed program to your desktop.
