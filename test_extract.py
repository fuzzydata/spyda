#!/usr/bin/env python

import sys

from spyda import parse_html


html = open(sys.argv[1], "r").read()
doc = parse_html(html)
