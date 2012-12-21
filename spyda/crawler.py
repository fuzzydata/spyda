"""Crawler Module

This module implements a :py:class:`Crawler` class that crawls a given url and all urls found recursively and accepts optional parameters that control:
 * Whether to restrict following to the domain of the starting URL.
"""

from collections import deque
from urlparse import urlparse, urlunparse

from .import fetch_url
from .import get_links


class Crawler:
    """Crawler Class

    Implements a basic Web Crawer that fetches the given URL.

    :param url: Initial starting URL
    :type  url: str

    :param restricted: ``True`` to restrict to the domain of the starting URL.
    :type  restricted: bool
    """

    def __init__(self, url, restricted=True):
        "initializes x; see x.__class__.__doc__ for signature"

        self.url = url
        self.restricted = restricted

        self.parsed_url = urlparse(self.url)

    def __call__(self):
        queue = deque([self.url])
        visited = []
        depth = 0

        while queue:
            url = queue.popleft()
            depth += 1

            if url not in visited:
                parsed_url = urlparse(url)

                visited.append(url)

                response, content = fetch_url(url)
                links = [link.get("href") for link in get_links(content)]

                for link in links:
                    if link not in visited:
                        scheme, netloc, path, params, query, fragment = urlparse(link)

                        if self.restricted and netloc and (netloc != self.parsed_url.netloc):
                            continue

                        yield link

                        if not scheme:
                            scheme = self.parsed_url.scheme
                        if not netloc:
                            netloc = self.parsed_url.netloc

                        data = (scheme, netloc, path, params, query, fragment,)
                        url = urlunparse(data)
                        queue.append(url)
