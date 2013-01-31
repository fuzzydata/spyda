import re
import htmlentitydefs

REPLACEMENTS = (
    (u"\xa0", u""),      # Unicide non-breaking space
    (u"\u2019", u"'"),   # Unicode right single quote
    (u"\u201c", u"\""),  # Unicode left double quote
    (u"\u201d", u"\"")   # Unicode right double quote
)


def unescape(text):
    """Removes HTML or XML character references and entities from a text string.

    :param text: The HTML (or XML) source text.

    :returns:   The plain text, as a Unicode string, if necessary.
    """

    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)


def cleanup(text):
    """Cleanup text abd replace commonly found entities such as smart quotes and non-breaking spaces"""

    for replacement in REPLACEMENTS:
        text = text.replace(*replacement)

    return text
