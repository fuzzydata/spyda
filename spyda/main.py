#!/usr/bin/env python

"""Web Crawler Tool"""

from optparse import OptionParser

from . import crawl
from . import __version__

USAGE = "%prog [options] <url>"
VERSION = "%prog v" + __version__


def parse_options():
    parser = OptionParser(usage=USAGE, version=VERSION)

    opts, args = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        raise SystemExit(1)

    return opts, args


def main():
    opts, args = parse_options()

    url = args[0]

    print("\n".join(map(lambda x: x[1], crawl(url))))


if __name__ == "__main__":
    main()
