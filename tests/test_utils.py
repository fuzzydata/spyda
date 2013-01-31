from spyda.utils import unichar_to_text, unescape, UNICHAR_REPLACEMENTS


TEST_ENTITIES = (
    ("&nbsp;",  u"\xa0"),
    ("&lsquo;", u"\u2018"),
    ("&rsquo;", u"\u2019"),
    ("&ldquo;", u"\u201c"),
    ("&rdquo;", u"\u201d"),
)


TEST_UNICHARS = UNICHAR_REPLACEMENTS


def pytest_generate_tests(metafunc):
    if "entity" in metafunc.fixturenames:
        metafunc.parametrize(["entity", "expected"], TEST_ENTITIES)
    elif "unichar" in metafunc.fixturenames:
        metafunc.parametrize(["unichar", "expected"], TEST_UNICHARS)


def test_unescape(entity, expected):
    actual = unescape(entity)
    assert actual == expected


def test_unichar_to_text(unichar, expected):
    actual = unichar_to_text(unichar)
    assert actual == expected
