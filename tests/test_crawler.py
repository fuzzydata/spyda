#!/usr/bin/env python

import pytest

from urlparse import urljoin
from operator import itemgetter

from py import path

from spyda import crawl, fetch_url, get_links


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
