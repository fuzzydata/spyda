# Package:  spyda
# Date:     18th December 2012
# Author:   James Mills, j dot mills at griffith dot edu dot au

"""Spyda - Python Spider Tool and Library

spyda is a simple tool and library written in the `Python Programming Language`_ to crawl a given url whilst allowing you to restrict results to a specified
domain and optionally also perform pattern matching against urls crawled. spyda will report on any urls it was unable to crawl along with their status code
and store successfully cralwed links and their content in a directory structure that matches the domain and urls searched.

:copyright: CopyRight (C) 2012 by James Mills

.. _Python Programming Language: http://www.python.org/
"""

__author__ = "James Mills, j dot mills at griffith dot edu dot au"
__date__ = "18th December 2012"
__version__ = "0.0.1dev"


from functools import partial
from collections import deque

from restclient import GET
from url import parse as parse_url
from re import compile as compile_regex
from lxml.html import fromstring as parse_html

HEADERS = {
    "User-Agent": "{0} v{1}".format(__name__, __version__)
}


fetch_url = partial(GET, headers=HEADERS, resp=True)


def get_links(html):
    return parse_html(html).cssselect("a")


def crawl(root_url, allowed_domains=None, max_depth=0, patterns=None, verbose=False):
    """Crawl a given url recursively for urls.

    :param root_url: Root URL to start crawling from.
    :type  root_url: str

    :param allowed_domains: A list of allowed domains to traverse. If evaluates to ``False``, allows all domains.
                            By default the domain of the starting URL above is added to the list.
    :type  allowed_domains: list or None or False

    :param max_depth: Maximum depth to follow, 0 for unlimited depth.
    :param max_depth: int

    :param patterns: A list of regex patterns to match urls against. If evaluates to ``False``, matches all urls.
    :type  patterns: list or None or False

    :param verbose: If ``True`` will print verbose logging
    :param verbose: bool

    In verbose mode the following single-character letters are used to denonate meaning for URLs being processing:
     - (I) Invalid URL
     - (F) Found a valid URL
     - (E) Error fetching URL
     - (V) URL already visitied
     - (Q) URL already enqueued
     - (O) URL outside allowed domains
    """

    def log(msg, *args):
        if verbose:
            print(msg.format(*args))

    patterns = [compile_regex(pattern) for pattern in patterns] if patterns else []
    root_url = parse_url(root_url)
    queue = deque([root_url])
    visited = set()
    errors = set()
    urls = set()
    n = 0

    if allowed_domains:
        allowed_domains.append(root_url._host)

    log("Crawling {0}", root_url.utf8())

    while queue:
        if max_depth and n >= max_depth:
            break

        n += 1
        current_url = queue.popleft()
        visited.add(current_url)

        response, content = fetch_url(current_url.utf8())

        log(
            " Followed: {0:d} {1:s} {2:s} {3:s} {4:s}",
            response.status, response.reason,
            response["content-type"], response["content-length"],
            current_url.utf8()
        )

        if not response.status == 200:
            errors.add((response.status, current_url.utf8()))
            links = []
        else:
            links = filter(lambda link: link is not None, (link.get("href") for link in get_links(content)))

        log("  Links:   {0}", len(links))

        for link in links:
            url, absurl = parse_url(link), current_url.relative(link).defrag().canonical()

            if absurl._scheme not in ("http", "https"):
                log("  (I): {0}", absurl.utf8())
                continue

            if any(absurl.equiv(url) for url in visited):
                log("  (V): {0}", absurl.utf8())
                continue

            if any(absurl.equiv(url) for url in queue):
                log("  (Q): {0}", absurl.utf8())
                continue

            if allowed_domains and absurl._host not in allowed_domains:
                log("  (O): {0}", absurl.utf8())
                continue

            queue.append(absurl)

            if patterns and not any((pattern.match(url.utf8()) is not None) or (pattern.match(absurl.utf8()) is not None) for pattern in patterns):
                log("  (P): {0}", absurl.utf8())
            else:
                log("  (F): {0}", absurl.utf8())
                urls.add((url.utf8(), absurl.utf8()))

    return {
        "urls": urls,
        "errors": errors
    }


__all__ = ("crawl", "fetch_url", "get_links",)
