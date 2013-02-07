#!/usr/bin/env python

from os import path
from glob import glob
from sys import stderr
from json import loads
from operator import itemgetter

from utils import csv_to_dictlist, get_close_matches


researchers = dict((" ".join([x.strip() for x in researcher["label"].split(" ") if x]), researcher["id"]) for researcher in csv_to_dictlist("researchers.csv"))
names = researchers.keys()
common_names = dict((" ".join(itemgetter(0, -1)(k.split(" "))), v) for k, v in researchers.items())

potential_mismatches = []

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

        import pudb; pudb.set_trace()

        for person in people:
            matches = get_close_matches(person, names, cutoff=0.80)
            match, score = matches[0] if matches else None, None
            if match is not None:
                matched_researchers.append((match, score, researchers[match]))
                continue

            matches = get_close_matches(person, common_names, cutoff=0.80)
            match, score = matches[0] if matches else None, None
            if match is not None:
                matched_researchers.append((match, score, common_names[match]))
                continue

            tokens = [x.strip() for x in person.split(" ") if x]
            if len(tokens) > 2:
                person = " ".join(itemgetter(0, -1)(tokens))

                matches = get_close_matches(person, names, cutoff=0.80)
                match, score = matches[0] if matches else None, None
                if match is not None:
                    matched_researchers.append((match, score, researchers[match]))
                    continue

                matches = get_close_matches(person, common_names, cutoff=0.80)
                match, score = matches[0] if matches else None, None
                if match is not None:
                    matched_researchers.append((match, score, common_names[match]))
                    continue

        if matched_researchers:
            print(" Researchers:")
            print("\n".join(["  {0:s} ({1:0.2f}%) ({1:s})".format(match, score, id) for match, score, id in matched_researchers]))
        else:
            matches = [(person, get_close_matches(person, names, cutoff=0.5)) for person in people]
            potential_mismatches.append((article_id, data["_source"], matches))
        print

print >> stderr, "Potential Mismatched Articles:"
for article_id, source, people in potential_mismatches:
    if people:
        print >> stderr, " Article ID: {0:s}".format(article_id)
        print >> stderr, " Source: {0:s}".format(source)
        print >> stderr, " People:"
        print >> stderr, "\n".join(["  {0:s} ({1:s})".format(person, repr(matches)) for person, matches in people])
