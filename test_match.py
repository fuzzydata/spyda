#!/usr/bin/env python

from operator import itemgetter

from fuzzywuzzy.process import extract
from nltk.metrics import edit_distance, masi_distance

from utils import csv_to_dictlist, get_close_matches

researchers = dict((" ".join([x.strip() for x in researcher["label"].split(" ") if x]), researcher["id"]) for researcher in csv_to_dictlist("researchers.csv"))
names = researchers.keys()
common_names = dict((" ".join(itemgetter(0, -1)(k.split(" "))), v) for k, v in researchers.items())
