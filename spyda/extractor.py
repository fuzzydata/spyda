#!/usr/bin/env python

"""Web Extraction Tool"""

from time import clock, time
from optparse import OptionParser

from . import __version__
from . import extract, log

USAGE = "%prog [options] <file|url>"
VERSION = "%prog v" + __version__


def parse_options():
    parser = OptionParser(usage=USAGE, version=VERSION)

    parser.add_option(
        "-f", "--filter",
        action="append", default=None, dest="filters",
        help="A CSS selector in the form: key=expression"
    )

    parser.add_option(
        "-o", "--output",
        action="store", default=None, dest="output",
        help="Output directory to dump output files"
    )

    parser.add_option(
        "-v", "--verbose",
        action="store_true", default=False, dest="verbose",
        help="Enable verbose logging"
    )

    opts, args = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        raise SystemExit(1)

    return opts, args


def main():
    opts, args = parse_options()

    source = args[0]

    opts.verbose and log("Processing: {0:s}", source)

    stime = time()

    print(extract(source, **opts.__dict__))

    if opts.verbose:
        cputime = clock()
        duration = time() - stime

        log("Processed in in {0:0.2f}s using {1:0.2f}s of CPU time.".format(duration, cputime))


if __name__ == "__main__":
    main()
