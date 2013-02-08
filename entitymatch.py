#!/usr/bin/env python

from glob import glob
from json import dumps, loads
from operator import itemgetter
from multiprocessing.pool import Pool

from utils import get_close_matches


records = loads(open("data.json", "rb").read())


cutoff = 0.85

id = "uri"
keys = [("preferred_name", "family_name"), ("given_name", "family_name")]
namesets = list(dict(("{0:s} {1:s}".format(*itemgetter(*k)(record)), record[id]) for record in records) for k in keys)


def job(filename):
    data = loads(open(filename, "rb").read())
    people = data.get("people", [])

    researchers = []

    for person in people:
        for nameset in namesets:
            matches = get_close_matches(person, nameset.keys(), cutoff=cutoff)
            match, score = matches[0] if matches else (None, None)
            if match is not None:
                researchers.append((match, score, nameset[match]))
                break

    data["researchers"] = list({"name": match, "score": score, "uri": uri} for match, score, uri in researchers)

    open(filename, "wb").write(dumps(data))


pool = Pool()
pool.map(job, glob("./tmp/*.json"))
