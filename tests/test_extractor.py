#!/usr/bin/env python

import pytest

from os import path

from spyda import extract

from .helpers import urljoin


@pytest.fixture()
def sample_file(request):
    return path.join(path.dirname(__file__), "docroot", "sample.html")


@pytest.fixture()
def sample_url(request, webapp):
    return urljoin(webapp.server.base, "sample.html")


@pytest.fixture()
def filters(request):
    return ["title=#article .title", "content=#article #content"]


@pytest.fixture()
def expected_result(request):
    return {"title": "Test Article", "content": "James Mills says \"Hello World!\""}


def test_extract_file(sample_file, filters, expected_result):
    result = extract(sample_file, filters)
    assert result == expected_result


def test_extract_url(sample_url, filters, expected_result):
    result = extract(sample_url, filters)
    assert result == expected_result
