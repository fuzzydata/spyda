#!/usr/bin/env python

from spyda import parse_html


html = open("index.html", "r").read()
doc = parse_html(html)
