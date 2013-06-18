#!/usr/bin/env python

from glob import glob

from setuptools import setup, find_packages

import spyda as pkg


setup(
    name=pkg.__name__,
    version=pkg.__version__,
    description=pkg.__doc__.split("\n")[0],
    long_description="{0:s}\n\n{1:s}".format(
        open("README.rst").read(), open("RELEASE.rst").read()
    ),
    author="James Mills",
    author_email="James Mills, j dot mills at griffith dot edu dot au",
    url="https://bitbucket.org/prologic/spyda",
    download_url="https://bitbucket.org/prologic/spyda/downloads/get/tip.zip"
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    license="MIT",
    keywords="Python Spider Web Crawling and Extraction Tool and Library",
    platforms="POSIX",
    packages=find_packages("."),
    scripts=glob("scripts/*"),
    dependency_links=[
        "https://bitbucket.org/prologic/calais/get/tip.zip#egg=calais-dev"
    ],
    install_requires=[
        "url",
        "lxml",
        "nltk",
        "calais",
        "cssselect",
        "restclient",
        "BeautifulSoup"
    ],
    entry_points={
        "console_scripts": [
            "crawl=spyda.crawler:main",
            "extract=spyda.extractor:main",
            "match=spyda.matcher:main"
        ]
    },
    zip_safe=False,
    test_suite="tests.main.runtests",
)
