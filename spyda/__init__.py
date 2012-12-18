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


from StringIO import StringIO

from lxml import etree
from restclient import GET


HEADERS = {
    "User-Agent": "{0} v{1}".format(__name__, __version__)
}


def fetch(url):
    return GET(url, headers=HEADERS, resp=True)


def parse(content):
    parser = etree.HTMLParser()
    return etree.parse(StringIO(content), parser)
