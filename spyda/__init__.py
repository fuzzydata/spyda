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


from collections import deque

from restclient import GET
from lxml.html import fromstring
from url import parse as parse_url

HEADERS = {
    "User-Agent": "{0} v{1}".format(__name__, __version__)
}


def fetch_url(url):
    return GET(url, headers=HEADERS, resp=True)


def get_links(html):
    dom = fromstring(html)
    return dom.cssselect("a")


def crawl(root_url, allowed_domains=None, verbose=False):
    """Crawl a given url recursively for urls.

    :param root_url: Root URL to start crawling from.
    :type  root_url: str

    :param allowed_domains: A list of allowed domains to traverse. If evaluates to ``False``, allows all domains.
                            By default the domain of the starting URL above is added to the list.
    :type  allowed_domains: list or None or False

    :param verbose: If ``True`` will print verbose logging
    :param verbose: bool
    """

    def log(msg, *args):
        if verbose:
            print(msg.format(*args))

    root_url = parse_url(root_url)
    queue = deque([root_url])
    visited = set()

    if allowed_domains:
        allowed_domains.append(root_url._host)

    log("Crawling {0}", root_url.utf8())

    while queue:
        current_url = queue.popleft()
        visited.add(current_url.utf8())

        response, content = fetch_url(current_url.utf8())
        log(" Followed: {0}", current_url.utf8())
        log("  Status:  {0}", response.status)

        links = filter(lambda link: link is not None, (link.get("href") for link in get_links(content)))
        log("  Links:   {0}", len(links))

        for link in links:
            url, absurl = parse_url(link), current_url.relative(link)

            if absurl.utf8() in visited:
                continue

            if allowed_domains and absurl._host not in allowed_domains:
                continue

            queue.append(absurl)

            log("  {0}", link)
            yield url.utf8(), absurl.utf8()

__all__ = ("crawl", "fetch_url", "get_links",)
