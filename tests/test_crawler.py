#!/usr/bin/env python

import pytest

from os import path

from spyda.crawler import crawl

from .helpers import urljoin


@pytest.fixture()
def sample_output(request, baseurl):
    return open(
        path.join(path.dirname(__file__), "output.txt"), "r"
    ).read().format(baseurl)


@pytest.fixture()
def expected_links(request, baseurl):
    lines = (
        x.strip()
        for x in open(path.join(path.dirname(__file__), "links.txt"), "r")
    )

    return sorted(x.format(baseurl) for x in lines)


def test_crawl(baseurl, expected_links):
    result = crawl(baseurl)
    assert set(result["errors"]) == set([(404, urljoin(baseurl, "asdf/"))])
    assert sorted(result["urls"]) == expected_links


def test_crawl_allowed_urls(baseurl):
    result = crawl(
        urljoin(baseurl, "external"),
        blacklist=[".*"],
        allowed_urls=["^http\:\/\/localhost.*"]
    )

    assert result["urls"] == ["http://www.google.com/"]
    assert not result["errors"]


def test_crawl_blacklist(baseurl):
    result = crawl(baseurl, blacklist=[".*"])

    assert set(result["urls"]) == set(
        [urljoin(baseurl, x) for x in ("foo/", "asdf/",)]
    )

    assert not result["errors"]


def test_crawl_whitelist(baseurl):
    result = crawl(
        urljoin(baseurl, "external"),
        blacklist=[".*"],
        allowed_urls=["^http\:\/\/localhost.*"]
    )

    assert result["urls"] == ["http://www.google.com/"]
    assert not result["errors"]


def test_crawl_max_depth(baseurl):
    result = crawl(baseurl, max_depth=1)
    assert not result["errors"]
    assert sorted(result["urls"]) == list(
        x.format(baseurl)
        for x in ("{0:s}/asdf/", "{0:s}/foo/")
    )


def test_crawl_patterns(baseurl):
    result = crawl(baseurl, patterns=["^.*\/foo\/$"])
    assert set(result["errors"]) == set([(404, urljoin(baseurl, "asdf/"))])
    assert sorted(result["urls"]) == list(
        x.format(baseurl)
        for x in ("{0:s}/foo/",)
    )


def test_crawl_verbose(baseurl, expected_links, sample_output, capsys):
    result = crawl(baseurl, verbose=True)
    assert set(result["errors"]) == set([(404, urljoin(baseurl, "asdf/"))])
    assert sorted(result["urls"]) == expected_links

    expected_output = sample_output.format(base_url=baseurl)

    out, err = capsys.readouterr()
    assert err == expected_output
