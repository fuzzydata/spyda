#!/usr/bin/env python

"""Web Crawler Tool"""

from optparse import OptionParser

from . import crawler
from . import __version__

USAGE = "%prog [options] <url>"
VERSION = "%prog v" + __version__


def parse_options():
    parser = OptionParser(usage=USAGE, version=VERSION)

    parser.add_option(
        "", "--maxdepth",
        action="store", type="int", default=0, dest="maxdepth",
        help="Maximum depth to traverse"
    )

    opts, args = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        raise SystemExit(1)

    return opts, args


def main():
    opts, args = parse_options()

    url = args[0]

    print("\n".join(crawler(url, maxdepth=opts.maxdepth)()))


if __name__ == "__main__":
    main()
