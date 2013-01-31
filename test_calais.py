#!/usr/bin/env python

import sys

from calais import Calais

API_KEY = "xgaxkzq96ep5rfjsptg4h3fm"

calais = Calais(api_key=API_KEY)
print(calais.analyze(sys.stdin.read()))
