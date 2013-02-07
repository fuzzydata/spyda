#!/usr/bin/env python

from glob import glob
from json import dumps, loads


files = glob("tmp/*.json")

with open("data.json", "wb") as f:
    f.write("[{0:s}]".format(",".join([dumps({"result": loads(open(file, "rb").read())}) for file in files])))
