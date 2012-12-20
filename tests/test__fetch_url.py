from urlparse import urljoin

from spyda import fetch_url


def test(webapp):
    res, data = fetch_url(urljoin(webapp.server.base, "hello"))

    assert res.status == 200
    assert data == "Hello World!"
