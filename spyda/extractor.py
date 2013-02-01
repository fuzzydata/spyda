#!/usr/bin/env python

"""Web Extraction Tool"""

from os import environ
from json import dumps
from time import clock, time
from optparse import OptionGroup, OptionParser

from . import __version__
from . import extract, log
from .utils import dict_to_text

try:
    from calais import Calais
    from .processors import process_calais
except ImportError:
    Calais = None  # NOQA

USAGE = "%prog [options] <file|url>"
VERSION = "%prog v" + __version__


def calais_options(parser):
    group = OptionGroup(
        parser,
        "Open Calais Options",
        "These options can be used to perform text analysis "
        "with the OpenCalais (http://www.opencalais.com/) "
        "web service. You must specify --calais-key or set "
        "the environment variable CALAIS_KEY to your key."
    )

    group.add_option(
        "", "--calais",
        action="store_true", default=False, dest="calais",
        help="Perform OpenCalais Text Analysis"
    )

    group.add_option(
        "", "--calais-key",
        action="store", type="string", metavar="KEY", default=environ.get("CALAIS_KEY", ""), dest="calais_key",
        help="OpenCalais API Key"
    )

    parser.add_option_group(group)


def parse_options():
    parser = OptionParser(usage=USAGE, version=VERSION)

    parser.add_option(
        "-f", "--filter",
        action="append", type="string", metavar="FILTER", default=None, dest="filters",
        help="A CSS selector in the form: key=expression"
    )

    parser.add_option(
        "-v", "--verbose",
        action="store_true", default=False, dest="verbose",
        help="Enable verbose logging"
    )

    if Calais is not None:
        calais_options(parser)

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

    result = extract(source, opts.filters)

    if Calais is not None and opts.calais:
        result.update(process_calais(dict_to_text(result), key=opts.calais_key))

    print(dumps(result))

    if opts.verbose:
        cputime = clock()
        duration = time() - stime

        log("Processed in in {0:0.2f}s using {1:0.2f}s of CPU time.".format(duration, cputime))


if __name__ == "__main__":
    main()
