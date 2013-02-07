#!/usr/bin/env python

from json import loads
from operator import itemgetter

from fuzzywuzzy.process import extract
from nltk.metrics import edit_distance, masi_distance

from utils import csv_to_dictlist, get_close_matches

records = loads(open("data.json", "rb").read())
keys = [("preferred_name", "family_name"), ("given_name", "family_name")]
namesets = list(dict(("{0:s} {1:s}".format(*itemgetter(*k)(record)), record["uri"]) for record in records) for k in keys)
