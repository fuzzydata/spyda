#!/usr/bin/env python

import sys
from pprint import pprint

from calais import Calais

API_KEY = "xgaxkzq96ep5rfjsptg4h3fm"

calais = Calais(api_key=API_KEY)
response = calais.analyze(sys.stdin.read())
pprint(response.entities)
