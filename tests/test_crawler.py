#!/usr/bin/env python

import pytest

from os import path
from urlparse import urljoin

from spyda import crawl


@pytest.fixture()
def sample_output(request, webapp):
    return open(path.join(path.dirname(__file__), "output.txt"), "r").read().format(webapp.server.base)


@pytest.fixture()
def expected_links(request, webapp):
    lines = (x.strip() for x in open(path.join(path.dirname(__file__), "links.txt"), "r"))
    return sorted(x.format(webapp.server.base) for x in lines)


def test_crawl(webapp, expected_links):
    result = crawl(webapp.server.base)
    print(repr(result["urls"]))
    assert set(result["errors"]) == set([(404, urljoin(webapp.server.base, "asdf/"))])
    assert sorted(result["urls"]) == expected_links


def test_crawl_allowed_urls(webapp):
    result = crawl(urljoin(webapp.server.base, "external"), allowed_urls=["^http\:\/\/localhost.*"])
    assert not result["urls"]
    assert not result["errors"]


def test_crawl_max_depth(webapp):
    result = crawl(webapp.server.base, max_depth=1)
    assert not result["errors"]
    assert sorted(result["urls"]) == list(x.format(webapp.server.base) for x in ("{0:s}/asdf/", "{0:s}/foo/"))


def test_crawl_patterns(webapp):
    result = crawl(webapp.server.base, patterns=["^.*\/foo\/$"])
    assert set(result["errors"]) == set([(404, urljoin(webapp.server.base, "asdf/"))])
    assert sorted(result["urls"]) == list(x.format(webapp.server.base) for x in ("{0:s}/foo/",))


def test_crawl_verbose(webapp, expected_links, sample_output, capsys):
    result = crawl(webapp.server.base, verbose=True)
    assert set(result["errors"]) == set([(404, urljoin(webapp.server.base, "asdf/"))])
    assert sorted(result["urls"]) == expected_links

    expected_output = sample_output.format(base_url=webapp.server.base)

    out, err = capsys.readouterr()
    assert err == expected_output