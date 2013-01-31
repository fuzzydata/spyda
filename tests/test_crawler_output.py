#!/usr/bin/env python

import pytest

from os import path

from circuits.net.sockets import Close
from circuits import Debugger, Manager

from spyda import crawl

from .helpers import urljoin
from .conftest import WebApp, Watcher


@pytest.fixture(scope="module")
def localmanager(request):
    localmanager = Manager()

    def finalizer():
        localmanager.stop()

    request.addfinalizer(finalizer)

    localmanager.start()

    if request.config.option.verbose:
        Debugger().register(localmanager)

    return localmanager


@pytest.fixture(scope="module")
def localwatcher(request, localmanager):
    localwatcher = Watcher().register(localmanager)

    def finalizer():
        localwatcher.unregister()

    return localwatcher


@pytest.fixture(scope="function")
def localwebapp(request, localmanager, localwatcher, webapp, tmpdir):
    result = crawl(webapp.server.base, output=str(tmpdir))
    assert set(result["errors"]) == set([(404, urljoin(webapp.server.base, "asdf/"))])

    docroot = tmpdir.join(webapp.server.base[(webapp.server.base.index("://") + 3):])
    localwebapp = WebApp(docroot=str(docroot)).register(localmanager)

    def finalizer():
        localwebapp.fire(Close(), localwebapp.server)
        localwebapp.stop()

    request.addfinalizer(finalizer)

    assert localwatcher.wait("ready", localwebapp.channel)

    return localwebapp


@pytest.fixture()
def sample_output(request, localwebapp):
    return open(path.join(path.dirname(__file__), "output2.txt"), "r").read().format(localwebapp.server.base)


@pytest.fixture()
def expected_links(request, localwebapp):
    lines = (x.strip() for x in open(path.join(path.dirname(__file__), "links.txt"), "r"))
    return sorted(x.format(localwebapp.server.base) for x in lines)


def test_crawl_output(localwebapp, expected_links, sample_output, capsys):
    result = crawl(localwebapp.server.base, verbose=True)
    assert not result["errors"]
    assert sorted(result["urls"]) == expected_links

    expected_output = sample_output.format(localwebapp.server.base)

    out, err = capsys.readouterr()
    assert err == expected_output
