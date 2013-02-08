#!/usr/bin/env python

from glob import glob
from json import loads


datum = (loads(open(f, "rB").read()) for f in glob("tmp/*.json"))
articles = [d["_source"] for d in datum if not d["people"]]
print(len(articles))
