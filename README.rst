.. _Python Programming Language: http://www.python.org/
.. _Python Standard Library: http://docs.python.org/library/
.. _restclient: http://pypi.python.org/pypi/restclient
.. _cssselect: http://pypi.python.org/pypi/cssselect
.. _lxml: http://pypi.python.org/pypi/lxml/3.0.2
.. _url: http://pypi.python.org/pypi/url
.. _nltk: https://pypi.python.org/pypi/nltk
.. _calais: https://bitbucket.org/prologic/calais
.. _BeautifulSoup: https://pypi.python.org/pypi/BeautifulSoup
.. _Griffith University: http://www.griffith.edu.au/
.. _Project Website: http://bitbucket.org/prologic/spyda
.. _PyPi Page: http://pypi.python.org/pypi/spyda
.. _Read the Docs: http://spyda.readthedocs.org/en/latest/
.. _Downloads Page: https://bitbucket.org/prologic/spyda/downloads


spyda is a simple tool and library written in the `Python Programming Language`_ to crawl a given url whilst allowing you to restrict results to a specified
domain and optionally also perform pattern matching against URLs crawled. spyda will report on any URLs it was unable to crawl along with their status code
and store successfully crawled links and their content in a directory structure that matches the domain and URLs searched.

spyda was developed at `Griffith University`_ as a tool and library to assist with web crawling tasks and data extraction and has been used to help
match researcher names against publications as well as extract data and links from external sources of data.

- Visit the `Project Website`_
- `Read the Docs`_
- Download it from the `Downloads Page`_

.. image:: https://pypip.in/v/spyda/badge.png
   :target: https://crate.io/packages/spyda/
   :alt: Latest PyPI version

.. image:: https://pypip.in/d/spyda/badge.png
   :target: https://crate.io/packages/spyda/
   :alt: Number of PyPI downloads

.. image:: https://jenkins.shiningpanda-ci.com/prologic/job/spyda/badge/icon
   :target: https://jenkins.shiningpanda-ci.com/prologic/job/spyda/
   :alt: Build Status


Requirements
------------

- `restclient`_
- `cssselect`_
- `lxml`_
- `url`_
- `nltk`_
- `calais`_
- `BeautifulSoup`_

spyda also comes basic documentation and a full comprehensive unit test suite which require the following:

To build the docs:

- `sphinx <https://pypi.python.org/pypi/Sphinx>`_
- `sphinxcontrib-bitbucket <https://pypi.python.org/pypi/sphinxcontrib-bitbucket>`_

To run the unit tests:

- `pytest <https://pypi.python.org/pypi/pytest>`_
- `circuits <https://pypi.python.org/pypi/circuits>`_


Installation
------------

The simplest and recommended way to install spyda is with pip.
You may install the latest stable release from PyPI with pip::

    > pip install spyda

If you do not have pip, you may use easy_install::

    > easy_install spyda

Alternatively, you may download the source package from the
`PyPI Page`_ or the `Downloads page`_ on the `Project Website`_;
extract it and install using::

    > python setup.py install

You can also install the
`latest-development version <https://bitbucket.org/prologic/spyda/get/tip.tar.gz#egg=spyda-dev>`_ by using ``pip`` or ``easy_install``::
    
    > pip install spyda==dev

or::
    
    > easy_install spyda==dev


For further information see the `spyda documentation <http://spyda.readthedocs.org/>`_.


Supported Platforms
-------------------

- Linux, FreeBSD, Mac OS X
- Python 2.6, 2.7

**Windows**: We acknowledge that Windows exists and make reasonable efforts
             to maintain compatibility. Unfortunately we cannot guarantee
             support at this time.
