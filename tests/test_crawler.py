import pytest
from py import path

from spyda import crawler


@pytest.fixture()
def expected_links():
    links = []
    for p in path.local(__file__).dirpath().visit(fil="links.txt", rec=True):
        links.extend([link for link in p.readlines(False) if link])
    return links


def test(webapp, expected_links):
    assert set(crawler(webapp.server.base)()) == set(expected_links)
