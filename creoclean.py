#!/usr/bin/env python
# file: creoclean.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2015 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2015-05-07 18:29:17 +0200
# Last modified: 2022-02-02T13:39:47+0100
"""
Cleans up Creo versioned files.

Works in the named diratories or in the current working directory.
Removes all versions except the last one, and renames that to version 1.
"""

import argparse
import glob
import logging
import os
import re
import sys

__version__ = "2021.02.18"


def main(argv):
    """
    Entry point for creoclean.

    Arguments:
        argv: command line arguments
    """
    dr = "dry run; show what would be done but don't delete files"
    opts = argparse.ArgumentParser(prog="creoclean", description=__doc__)
    opts.add_argument("-d", dest="dry_run", action="store_true", help=dr)
    opts.add_argument("-v", "--version", action="version", version=__version__)
    opts.add_argument(
        "--log",
        default="warning",
        choices=["debug", "info", "warning", "error"],
        help="logging level (defaults to 'warning')",
    )
    opts.add_argument(
        "dirs",
        metavar="dir",
        nargs="*",
        default=[],
        help="one or more directories to process",
    )
    args = opts.parse_args(argv)
    lfmt = "%(levelname)s: %(message)s"
    if args.dry_run:
        logging.basicConfig(level="INFO", format=lfmt)
        logging.info("DRY RUN, no files will be deleted or renamed")
    else:
        logging.basicConfig(level=getattr(logging, args.log.upper(), None), format=lfmt)
    if not args.dirs:
        args.dirs = ["."]
    for directory in [d for d in args.dirs if os.path.isdir(d)]:
        logging.info(f"cleaning up versioned files in '{directory}'")
        clean_versioned(directory, args.dry_run)
        logging.info(f"cleaning up miscellaneous files in '{directory}'")
        clean_miscellaneous(directory, args.dry_run)


def clean_versioned(path, dry_run):  # noqa
    """
    Clean up Creo versioned files in the named directory.

    Arguments:
        path: The path of the directory to clean.
        dry_run: Boolean to indicate a dry run.
    """
    filenames = [e for e in os.listdir(path) if os.path.isfile(os.path.join(path, e))]
    logging.info(f"found {len(filenames)} files")
    splits = [re.split("^(.*)\.([^\.]{3})\.([0-9]+)$", fn) for fn in filenames]
    splits = [s[1:-1] for s in splits if len(s) == 5]
    exts = sorted(set([s[1] for s in splits]))
    os.chdir(path)
    for ext in exts:
        data = [s for s in splits if s[1] == ext]
        cnt = len(data)
        if cnt < 2:
            logging.info(f"not enough '{ext}' files; skipping")
            continue
        logging.info(f"found {cnt} '{ext}' files")
        names = set(p[0] for p in data)
        logging.info(f"found {len(names)} unique '{ext}' file names")
        for nm in names:
            numbers = [int(p[2]) for p in data if p[0] == nm]
            if len(numbers) > 1:
                numbers.sort()
                for n in numbers[:-1]:
                    fn = f"{nm}.{ext}.{n}"
                    logging.info(f"removing '{fn}'")
                    if not dry_run:
                        try:
                            os.remove(fn)
                        except OSError as e:
                            logging.warning(f"removing '{fn}' failed: {e}")
            oldfn = f"{nm}.{ext}.{numbers[-1]}"
            newfn = f"{nm}.{ext}.{1}"
            if oldfn != newfn:
                logging.info(f"renaming '{oldfn}' to '{newfn}'")
                if not dry_run:
                    try:
                        os.rename(oldfn, newfn)
                    except OSError as e:
                        logging.warning(f"renaming '{oldfn}' failed: {e}")


def clean_miscellaneous(path, dry_run):
    """
    Clean up Creo log files in the named directory.

    Arguments:
        path: The path of the directory to clean.
        dry_run: Boolean to indicate a dry run.
    """
    os.chdir(path)
    log = glob.glob("*.log*")
    logging.info(f"{len(log)} log files found.")
    xml = glob.glob("*log.xml")
    logging.info(f"{len(xml)} log.xml files found.")
    inf = glob.glob("*.inf.*")
    logging.info(f"{len(inf)} inf files found.")
    txt = glob.glob("*.txt.*")
    logging.info(f"{len(txt)} txt files found.")
    mp = glob.glob("*.m_p")
    logging.info(f"{len(mp)} m_p files found.")
    xt = glob.glob("*.x_t")
    logging.info(f"{len(xt)} x_t files found.")
    files = log + xml + inf + txt + mp + xt
    for fn in files:
        logging.info(f"removing '{fn}'")
        if not dry_run:
            try:
                os.remove(fn)
            except OSError as e:
                logging.warning(f"removing '{fn}' failed: {e}")


if __name__ == "__main__":
    main(sys.argv[1:])
