#!/usr/bin/env python

import pytest

from urlparse import urljoin
from operator import itemgetter

from py import path

from spyda import crawl, fetch_url, get_links


SAMPLE_CONTENT = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head>
 <title>/</title>
</head>

<body>
 <p>Hello World!</p>
 <p><a href=".">.</a></p>
 <p><a href="..">..</a></p>
 <p><a href="foo/">foo/</a></p>
 <p>Test suite created by <a href="mailto:j.mills@griffith.edu.au">James Mills, j dot mills at griffith dot edu dot au</a></p>
</body>
</html>
"""


SAMPLE_VERBOSE_OUTPUT = """\
Crawling {base_url:s}/
 Followed: 200 OK text/html 535 {base_url:s}/
  Links:   6
  (V): {base_url:s}/
  (V): {base_url:s}/
  (F): {base_url:s}/foo/
  (Q): {base_url:s}/foo/
  (F): {base_url:s}/asdf/
  (I): mailto:j.mills@griffith.edu.au
 Followed: 200 OK text/html 338 {base_url:s}/foo/
  Links:   3
  (V): {base_url:s}/foo/
  (V): {base_url:s}/
  (F): {base_url:s}/foo/bar/
 Followed: 404 Not Found text/html; charset=utf-8 640 {base_url:s}/asdf/
  Links:   0
 Followed: 200 OK text/html 313 {base_url:s}/foo/bar/
  Links:   2
  (V): {base_url:s}/foo/bar/
  (V): {base_url:s}/foo/
"""


@pytest.fixture()
def sample_content():
    return SAMPLE_CONTENT


@pytest.fixture()
def expected_links():
    links = []
    for p in path.local(__file__).dirpath().visit(fil="links.txt", rec=True):
        links.extend([link for link in p.readlines(False) if link])
    return sorted(links)


def test_fetch_url(webapp):
    res, data = fetch_url(urljoin(webapp.server.base, "hello"))
    assert res.status == 200
    assert data == "Hello World!"


def test_get_links(sample_content):
    links = [element.get("href") for element in get_links(sample_content)]
    assert links == [".", "..", "foo/", "mailto:j.mills@griffith.edu.au"]


def test_crawl(webapp, expected_links):
    result = crawl(webapp.server.base)
    assert result["errors"] == set([(404, urljoin(webapp.server.base, "asdf/"))])
    assert sorted(map(itemgetter(0), result["urls"])) == expected_links


def test_crawl_allowed_domains(webapp):
    result = crawl(urljoin(webapp.server.base, "external"), allowed_domains=["localhost"])
    assert not result["urls"]
    assert not result["errors"]


def test_crawl_max_depth(webapp):
    result = crawl(webapp.server.base, max_depth=1)
    assert not result["errors"]
    assert sorted(map(itemgetter(0), result["urls"])) == ["asdf/", "foo/"]


def test_crawl_patterns(webapp):
    result = crawl(webapp.server.base, patterns=["^.*\/foo\/$"])
    assert result["errors"] == set([(404, urljoin(webapp.server.base, "asdf/"))])
    assert sorted(map(itemgetter(0), result["urls"])) == ["foo/"]


def test_crawl_verbose(webapp, expected_links, capsys):
    result = crawl(webapp.server.base, verbose=True)
    assert result["errors"] == set([(404, urljoin(webapp.server.base, "asdf/"))])
    assert sorted(map(itemgetter(0), result["urls"])) == expected_links

    expected_output = SAMPLE_VERBOSE_OUTPUT.format(base_url=webapp.server.base)

    out, err = capsys.readouterr()
    assert out == expected_output
