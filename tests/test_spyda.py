#!/usr/bin/env python

import pytest

from urlparse import urljoin

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
 Followed: {base_url:s}/
  Status:  200
  Links:   5
  (V): {base_url:s}/
  (V): {base_url:s}/
  (F): {base_url:s}/foo/
  (Q): {base_url:s}/foo/
  (I): mailto:j.mills@griffith.edu.au
 Followed: {base_url:s}/foo/
  Status:  200
  Links:   3
  (V): {base_url:s}/foo/
  (V): {base_url:s}/
  (F): {base_url:s}/foo/bar/
 Followed: {base_url:s}/foo/bar/
  Status:  200
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
    return links


def test_fetch_url(webapp):
    res, data = fetch_url(urljoin(webapp.server.base, "hello"))
    assert res.status == 200
    assert data == "Hello World!"


def test_get_links(sample_content):
    links = [element.get("href") for element in get_links(sample_content)]
    assert links == [".", "..", "foo/", "mailto:j.mills@griffith.edu.au"]


def test_crawl(webapp, expected_links):
    assert set(map(lambda x: x[0], crawl(webapp.server.base, allowed_domains=["localhost"]))) == set(expected_links)


def test_crawl_allowed_domains(webapp):
    assert not set(map(lambda x: x[0], crawl(urljoin(webapp.server.base, "external"), allowed_domains=["localhost"])))


def test_crawl_max_depth(webapp):
    assert set(map(lambda x: x[0], crawl(webapp.server.base, allowed_domains=["localhost"], max_depth=1))) == set(["foo/"])


def test_crawl_patterns(webapp):
    assert set(map(lambda x: x[0], crawl(webapp.server.base, allowed_domains=["localhost"], patterns=["^.*\/foo\/$"]))) == set(["foo/"])


def test_crawl_verbose(webapp, expected_links, capsys):
    assert set(map(lambda x: x[0], crawl(webapp.server.base, allowed_domains=["localhost"], verbose=True))) == set(expected_links)

    expected_output = SAMPLE_VERBOSE_OUTPUT.format(base_url=webapp.server.base)

    out, err = capsys.readouterr()
    assert out == expected_output
