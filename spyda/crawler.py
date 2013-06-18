#!/usr/bin/env python

"""Web Crawler Tool"""

import sys
from warnings import warn
from time import clock, time
from optparse import OptionParser

from . import crawl
from . import __version__

USAGE = "%prog [options] <url>"
VERSION = "%prog v" + __version__


def parse_options():
    parser = OptionParser(usage=USAGE, version=VERSION)

    # XXX: Remove this block in spyda>0.0.2
    parser.add_option(
        "-a", "--allowed_url",
        action="append", default=None, dest="allowed_urls",
        help="(@deprecated) Allowed url to traverse (multiple allowed)."
    )

    parser.add_option(
        "-b", "--blacklist",
        action="append", default=None, dest="blacklist",
        help="Blacklisted URL to not traverse (multiple allowed)."
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

    parser.add_option(
        "-w", "--whitelist",
        action="append", default=None, dest="whitelist",
        help="Whitelisted URL to traverse (multiple allowed)."
    )

    opts, args = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        raise SystemExit(1)

    # XXX: Remove this block in spyda>0.0.2
    if opts.allowed_urls:
        warn("The use of the ``-a/--allowed_url`` option is deprecated. Please use ``-w/--whitelist`` instead.", category=DeprecationWarning)

    return opts, args


def main():
    opts, args = parse_options()

    url = args[0]

    if opts.verbose:
        print("Crawling {0:s}".format(url))

    stime = time()
    result = crawl(url, **opts.__dict__)

    if result["urls"]:
        if opts.verbose:
            print("URL(s):")
        print("\n".join(result["urls"]))
    else:
        if opts.verbose:
            print("No URL(s) found!")

    if result["errors"]:
        if opts.verbose:
            print >> sys.stderr, "Error(s):"
        print >> sys.stderr, "\n".join(
            " {0:d} {1:s}".format(*url) for url in result["errors"]
        )

    if opts.verbose:
        cputime = clock()
        duration = time() - stime
        urls = len(result["urls"])
        urls_per_second = int(urls / duration)

        print(
            "{0:d} urls in {1:0.2f}s ({2:d}/s) CPU: {3:0.2f}s".format(
                urls, duration, urls_per_second, cputime
            )
        )

if __name__ == "__main__":
    main()
