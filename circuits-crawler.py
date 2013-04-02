#!/usr/bin/env python

"""Web Crawler Tool"""

import warnings
warnings.filterwarnings("ignore")  # Ignore circuits-2.1.1dev warnings!

import sys
from time import clock, time
from collections import deque
from uuid import uuid4 as uuid
from traceback import format_exc
from optparse import OptionParser
from re import escape as escape_regex
from re import compile as compile_regex

try:
    import hotshot
    import hotshot.stats
except ImportError:
    hostshot = None

from url import parse as parse_url
from lxml.html.soupparser import fromstring as html_to_doc

from circuits.web.client import Client, Close, Request
from circuits import handler, Component, Debugger, Event, Task, Worker


__version__ = "0.0.1"


USAGE = "%prog [options] <url>"
VERSION = "%prog v" + __version__


def parse_options():
    parser = OptionParser(usage=USAGE, version=VERSION)

    parser.add_option(
        "-a", "--allowed_url",
        action="append", default=None, dest="allowed_urls",
        help="Allowed url to traverse (multiple allowed)."
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
        "", "--profile",
        action="store_true", default=False, dest="profile",
        help="Enable execution profiling support"
    )

    parser.add_option(
        "-v", "--verbose",
        action="count", default=0, dest="verbose",
        help="Enable verbose logging"
    )

    opts, args = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        raise SystemExit(1)

    return opts, args


def log(msg, *args, **kwargs):
    sys.stderr.write("{0:s}{1:s}".format(
        msg.format(*args),
        kwargs.get("n", "\n"))
    )
    sys.stderr.flush()


def error(e):  # pragma: no cover
    log("ERROR: {0:s}", e)
    log(format_exc())


def status(msg, *args):
    log("\r\x1b[K{0:s}", msg.format(*args), n="")


def parse_html(html):
    return html_to_doc(html)


def get_links(url, html, badchars="\"' \v\f\t\n\r"):
    _url = parse_url(url)
    tags = parse_html(html).cssselect("a")
    hrefs = (tag.get("href") for tag in tags)
    links = (href.strip(badchars) for href in hrefs if href is not None)
    urls = set(sorted(_url.relative(link) for link in links))
    return [url.sanitize().defrag().canonical().utf8()
            for url in urls
            if url._scheme in ("http", "https")]


class Fetch(Event):
    """Fetch Event"""


class Parse(Event):
    """Parse Event"""


class Process(Event):
    """Process Event"""


class WebCrawler(Component):

    channel = "crawler"

    def init(self, url, allowed_urls=None, max_depth=0, patterns=None,
             verbose=0, profile=False, channel=channel):
        self.url = url

        if not allowed_urls:
            allowed_urls = ["^{0:s}.*(?is)".format(
                escape_regex(self.url))
            ]

        self.allowed_urls = [compile_regex(regex) for regex in allowed_urls]

        self.max_depth = max_depth

        self.patterns = [compile_regex(regex) for regex in patterns] \
            if patterns else []
        self.verbose = verbose

        self.queue = deque([self.url])
        self.visited = []
        self.errors = []
        self.urls = []
        self.n = 0
        self.l = 0

        self.worker = Worker(process=True).register(self)

    def error(self, etype, evalue, etraceback, handler=None, fevent=None):
        if self.verbose:
            log("ERROR: {0:s}\n{1:s}", evalue, "\n".join(etraceback))

    def fetch(self, url):
        if self.max_depth and self.n >= self.max_depth:
            raise SystemExit(0)

        self.n += 1
        self.visited.append(url)

        channel = uuid().hex
        client = Client(channel=channel).register(self)
        yield self.wait("ready", channel)

        self.fire(Request("GET", url), channel)
        yield self.wait("response", channel)

        if client.connected:
            self.fire(Close(), channel)
            yield self.wait("disconnected", channel)

        client.unregister()
        yield self.wait("unregistered", channel)

        response = client.response

        if response is None:
            self.queue.append(url)
            return

        if response.status == 200:
            html = response.read()
            #self.fire(Parse(url, html))
            self.fire(Task(get_links, url, html), self.worker)

            self.verbose and log(
                " {0:d} {1:s} {2:s} {3:s} {4:s}",
                response.status, response.reason,
                response.headers["Content-Type"],
                response.headers.get("Content-Length", ""),
                url
            )
        elif response.status in (300, 301, 302, 303, 304, 305, 306, 307,):
            location = response.headers["Location"]
            new_url = parse_url(url)\
                .relative(location)\
                .sanitize()\
                .defrag()\
                .canonical()\
                .utf8()
            self.queue.append(new_url)
        else:
            self.errors.append((response.status, url))

    def parse(self, url, html):
        self.fire(Process(get_links(url, html)))

    def process(self, links):
        for link in links:
            if link in self.urls:
                self.verbose and log("  (S): {0}", link)
                continue

            if link in self.visited:
                self.verbose and log("  (V): {0}", link)
                continue

            if self.allowed_urls and not any((regex.match(link) is not None)
                                             for regex in self.allowed_urls):
                self.visited.append(link)
                self.verbose and log("  (O): {0}", link)
                continue

            self.queue.append(link)

            if self.patterns and not any((regex.match(link) is not None)
                                         for regex in self.patterns):
                self.verbose and log("  (P): {0}", link)
            else:
                self.verbose and log("  (F): {0}", link)
                self.urls.append(link)
                self.l += 1
            yield

    @handler("task_success", channel="*")
    def _on_task_success(self, event, evt, value):
        self.fire(Process(value))

    @handler("generate_events")
    def _on_generate_events(self, event):
        event.reduce_time_left(0)

        while self.queue:
            self.fire(Fetch(self.queue.popleft()))

        if sum([len(self._queue), len(self._tasks)]) == 0:
            raise SystemExit(0)

        if not self.verbose:
            status(
                "F: {0:>4d} V: {1:>4d} L: {2:>4d} E: {3:3>d} T: {4:3>d}".format(
                    self.n, len(self.visited), self.l, len(self._queue), len(self._tasks)
                )
            )


def main():
    opts, args = parse_options()

    url = args[0]

    if opts.verbose:
        print("Crawling {0:s}".format(url))

    stime = time()

    crawler = WebCrawler(url, **opts.__dict__)
    if opts.verbose > 1:
        Debugger().register(crawler)

    if opts.profile and hotshot:
        profiler = hotshot.Profile(".profile")
        profiler.start()

    crawler.run()

    if opts.profile and hotshot:
        profiler.stop()
        profiler.close()

        stats = hotshot.stats.load(".profile")
        stats.strip_dirs()
        stats.sort_stats("time", "calls")
        stats.print_stats(20)

    if crawler.urls:
        if opts.verbose:
            print("URL(s):")
        print("\n".join(crawler.urls))
    else:
        if opts.verbose:
            print("No URL(s) found!")

    if crawler.errors:
        if opts.verbose:
            print >> sys.stderr, "Error(s):"
        print >> sys.stderr, "\n".join(
            " {0:d} {1:s}".format(*url) for url in crawler.errors
        )

    if opts.verbose:
        cputime = clock()
        duration = time() - stime
        urls = len(crawler.urls)
        urls_per_second = int(urls / duration)

        print(
            "{0:d} urls in {1:0.2f}s ({2:d}/s) CPU: {3:0.2f}s".format(
                urls, duration, urls_per_second, cputime
            )
        )

if __name__ == "__main__":
    main()
