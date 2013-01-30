#!/usr/bin/env python

import pytest

from os import path

from spyda import extract


@pytest.fixture()
def sample_source(request):
    return path.join(path.dirname(__file__), "sample.html")


@pytest.fixture()
def filters(request):
    return ["title=#article .title", "content=#article #content"]


@pytest.fixture()
def expected_result(request):
    return {"title": "Test Article", "content": "James Mills says \"Hello World!\""}


def test_extract(sample_source, filters, expected_result):
    result = extract(sample_source, filters)
    assert result == expected_result
