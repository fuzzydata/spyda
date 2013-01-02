#!/usr/bin/env python

import pytest

from urlparse import urljoin

from py import path

from spyda import crawl, fetch_url, get_links


def pytest_generate_tests(metafunc):
    if metafunc.fixturenames == ["s", "expected_links"]:
        tests = []
        for p in path.local(__file__).dirpath().visit(fil="*.html", rec=True):
            s = p.read()
            expected_links = [link for link in p.new(basename="links.txt").readlines(False) if link]
            args = (s, expected_links,)
            tests.append(args)

        metafunc.parametrize(["s", "expected_links"], tests)


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


def test_get_links(s, expected_links):
    actual_links = [element.get("href") for element in get_links(s)]
    assert actual_links == expected_links


def test_crawl(webapp, expected_links):
    assert set(map(lambda x: x[0], crawl(webapp.server.base, allowed_domains=["localhost"]))) == set(expected_links)
