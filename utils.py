#!/usr/bin/env python

from heapq import nlargest
from difflib import SequenceMatcher
from csv import DictReader, Sniffer


def csv_to_dictlist(csvfile):
    with open(csvfile, "rb") as f:
        dialect = Sniffer().sniff(f.read(1024))
        f.seek(0)
        return list(dict((k.strip(), v.strip()) for k, v in d.items()) for d in DictReader(f, dialect=dialect))


def get_close_matches(word, possibilities, n=3, cutoff=0.6):
    """Use SequenceMatcher to return list of close matches.

    word is a sequence for which close matches are desired (typically a string).

    possibilities is a list of sequences against which to match word (typically a list of strings).

    Optional arg n (default 3) is the maximum number of close matches to return. n must be > 0.

    Optional arg cutoff (default 0.6) is a float in [0.0, 1.0].
    Possibilities that don't score at least that similar to word are ignored.

    The best (no more than n) matches among the possibilities are returned
    in a list, sorted by similarity score, most similar first.

    >>> get_close_matches("appel", ["ape", "apple", "peach", "puppy"])
    ['apple', 'ape']
    >>> import keyword as _keyword
    >>> get_close_matches("wheel", _keyword.kwlist)
    ['while']
    >>> get_close_matches("apple", _keyword.kwlist)
    []
    >>> get_close_matches("accept", _keyword.kwlist)
    ['except']
    """

    if not n > 0:
        raise ValueError("n must be > 0: %r" % (n,))
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))

    result = []
    s = SequenceMatcher()
    s.set_seq2(word)
    for x in possibilities:
        s.set_seq1(x)
        if s.real_quick_ratio() >= cutoff and s.quick_ratio() >= cutoff and s.ratio() >= cutoff:
            result.append((x, s.ratio()))

    # Return n largest best scorers and their matches.
    return nlargest(n, result)


def _test():
    import doctest
    return doctest.testmod()


if __name__ == "__main__":
    _test()
