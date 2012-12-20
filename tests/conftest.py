# Module:   conftest
# Date:     20th December 2012
# Author:   James Mills, j dot mills at griffith dot edu dot au

"""pytest config"""

from os import path
from time import sleep

import pytest


DOCROOT = path.join(path.dirname(__file__), "docroot")


@pytest.fixture(scope="session")
def webapp(request):
    from circuits import Component
    from circuits.net.sockets import Close
    from circuits.web import Controller, Server, Static

    class Root(Controller):

        def hello(self):
            return "Hello World!"

    class WebApp(Component):

        def init(self, docroot):
            self.docroot = docroot

            self.server = Server(0).register(self)
            Root().register(self)
            Static(docroot=self.docroot).register(self)

    webapp = WebApp(DOCROOT)

    webapp.start()
    sleep(1)  # Give circuits.web time to startup

    def finalizer():
        webapp.fire(Close(), webapp.server)
        webapp.stop()

    request.addfinalizer(finalizer)

    return webapp
