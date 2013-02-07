#!/usr/bin/env python

from os import path
from glob import glob
from json import loads
from operator import itemgetter

from utils import get_close_matches


records = loads(open("data.json", "rb").read())


cutoff = 0.85

id = "uri"
keys = [("preferred_name", "family_name"), ("given_name", "family_name")]
namesets = list(dict(("{0:s} {1:s}".format(*itemgetter(*k)(record)), record[id]) for record in records) for k in keys)


for filename in glob("./tmp/*.json"):
    with open(filename, "r") as f:
        data = loads(f.read())

    article_id, _ = path.splitext(path.basename(filename))
    print("Article ID: {0:s}".format(article_id))
    print(" Source: {0:s}".format(data["_source"]))
    print(" Title: {0:s}".format(data["title"].encode("utf-8")))

    people = data.get("people", [])

    if people:
        print(" People:")
        print("\n".join(["  {0:s}".format(person) for person in people]))

        matched_researchers = []

        for person in people:
            for nameset in namesets:
                matches = get_close_matches(person, nameset.keys(), cutoff=cutoff)
                match, score = matches[0] if matches else (None, None)
                if match is not None:
                    matched_researchers.append((match, score, nameset[match]))
                    break

        if matched_researchers:
            print(" Researchers:")
            print("\n".join(["  {0:s} ({1:0.2f}%) ({2:s})".format(match, (score * 100.0), id) for match, score, id in matched_researchers]))
    print
