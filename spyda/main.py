#!/usr/bin/env python

"""Web Crawler Tool"""

from optparse import OptionParser

from . import crawl
from . import __version__

USAGE = "%prog [options] <url>"
VERSION = "%prog v" + __version__


def parse_options():
    parser = OptionParser(usage=USAGE, version=VERSION)

    parser.add_option(
        "-a", "--allowed_domain",
        action="append", default=None, dest="allowed_domains",
        help="Allowed domain to traverse (multiple allowed)."
    )

    parser.add_option(
        "-d", "--max_depth",
        action="store", type=int, default=0, dest="max_depth",
        help="Maximum depth to follow (0 for unlimited)"
    )

    parser.add_option(
        "-p", "--pattern",
        action="append", default=None, dest="patterns",
        help="URL pattern to match (multiple allowed)."
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

    url = args[0]

    result = crawl(url, **opts.__dict__)

    if result["urls"]:
        print("URL(s):")
        print("\n".join(" {0:s} {1:s}".format(*url) for url in result["urls"]))
    else:
        print("No URL(s) found!")

    if result["errors"]:
        print("Error(s):")
        print("\n".join(" {0:d} {1:s}".format(*url) for url in result["errors"]))


if __name__ == "__main__":
    main()
