#!/usr/bin/env python3
# file: creoclean.py
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2015-05-07 18:29:17 +0200
# Last modified: 2015-05-07 21:15:18 +0200
#
# To the extent possible under law, R.F. Smith has waived all copyright and
# related or neighboring rights to cadclean.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

"""Cleans up Creo versioned files in the current working directory."""

import argparse
import logging
import os
import re
import sys

__version__ = '0.1.0'


def main(argv):
    """
    Entry point for cadclean.

    Arguments:
        param argv: command line arguments
    """
    dr = "dry run; show what would be done but don't delete files"
    opts = argparse.ArgumentParser(prog='cadclean', description=__doc__)
    opts.add_argument('-d', dest='dry_run', action="store_true", help=dr)
    opts.add_argument('-v', '--version', action='version',
                      version=__version__)
    opts.add_argument('--log', default='warning',
                      choices=['debug', 'info', 'warning', 'error'],
                      help="logging level (defaults to 'warning')")
    args = opts.parse_args(argv)
    lfmt = '%(levelname)s: %(message)s'
    if args.dry_run:
        logging.basicConfig(level='INFO', format=lfmt)
        logging.info('DRY RUN, no files will be deleted')
    else:
        logging.basicConfig(level=getattr(logging, args.log.upper(), None),
                            format=lfmt)
    filenames = [e for e in os.listdir() if os.path.isfile(e)]
    logging.info('found {} files'.format(len(filenames)))
    splits = [re.split('^(.*)\.([^\.]{3})\.([0-9]+)$', fn) for fn in filenames]
    splits = [s[1:-1] for s in splits if len(s) == 5]
    exts = sorted(set([s[1] for s in splits]))
    for ext in exts:
        data = [s for s in splits if s[1] == ext]
        cnt = len(data)
        if cnt < 2:
            logging.info("not enough '{}' files; skipping".format(ext))
            continue
        logging.info("found {} '{}' files".format(cnt, ext))
        names = set(p[0] for p in data)
        logging.info("found {} unique '{}' file names".format(len(names), ext))
        for nm in names:
            numbers = [int(p[2]) for p in data if p[0] == nm]
            if len(numbers) > 1:
                numbers.sort()
                for n in numbers[:-1]:
                    fn = "{}.{}.{}".format(nm, ext, n)
                    logging.info("removing {}".format(fn))
                    if not args.dry_run:
                        os.remove(fn)
            logging.info("(leaving {}.{}.{})".format(nm, ext, numbers[-1]))


if __name__ == '__main__':
    main(sys.argv[1:])
