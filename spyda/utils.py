import re
import htmlentitydefs


UNICHAR_REPLACEMENTS = (
    (u"\xa0",   u" "),      # non breaking space
    (u"\u2013", u"-"),      # en dash
    (u"\u2018", u"`"),      # left single quote
    (u"\u2019", u"'"),      # right single quote
    (u"\u2026", u"..."),    # horizontal ellipsis
    (u"\u201c", u"\""),     # left double quote
    (u"\u201d", u"\""),     # right double quote
)


def is_url(s):
    return s.find("://") > 0


def dict_to_text(d):
    return "\n".join("{0:s}: {1:s}".format(k, v) for k, v in d.items())


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


def unichar_to_text(text):
    """Convert some common unicode characters to their plain text equivilent.

    This includes for example left and right double quotes, left and right single quotes, etc.
    """

    for replacement in UNICHAR_REPLACEMENTS:
        text = text.replace(*replacement)

    return text
