from urlparse import urljoin

from spyda import fetch


def test_fetch(webapp):
    res, data = fetch(urljoin(webapp.server.base, "hello"))

    assert res.status == 200
    assert data == "Hello World!"
