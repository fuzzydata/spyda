#!/usr/bin/env python

import pytest

from os import path
from json import loads

from url import parse as parse_url

from spyda import extract

from .helpers import urljoin


@pytest.fixture()
def sample_file(request):
    root = path.dirname(__file__)
    return path.relpath(path.join(root, "docroot", "sample.html"), path.join(path.dirname(__file__), ".."))


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


def test_extract_file_output(sample_file, filters, expected_result, tmpdir):
    extract(sample_file, filters, output=str(tmpdir))
    file = tmpdir.join(sample_file)
    result = loads(file.read())
    assert result == expected_result


def test_extract_url(sample_url, filters, expected_result):
    result = extract(sample_url, filters)
    assert result == expected_result


def test_extract_url_output(sample_url, filters, expected_result, tmpdir):
    extract(sample_url, filters, output=str(tmpdir))
    filename = parse_url(sample_url).escape().utf8()
    file = tmpdir.join(filename[(filename.index("://") + 3):])
    result = loads(file.read())
    assert result == expected_result
