# pyright: basic

import pytest
from src.core.accido.misc import MultipleEndings


def test_multiple_endings():
    multiple_endings = MultipleEndings(regular="a", foo="b", bar="c")
    assert multiple_endings.regular == "a"
    assert multiple_endings.foo == "b"
    assert multiple_endings.bar == "c"


def test_getall():
    multiple_endings = MultipleEndings(regular="a", foo="b", bar="c")
    assert multiple_endings.get_all() == ("a", "b", "c")


def test_prefix():
    multiple_endings = MultipleEndings(regular="a", foo="b", bar="c")
    assert multiple_endings + "d" == MultipleEndings(regular="ad", foo="bd", bar="cd")
    assert "d" + multiple_endings == MultipleEndings(regular="da", foo="db", bar="dc")


def test_error():
    with pytest.raises(ValueError, match=r"MultipleEndings must have a 'regular' attribute."):
        MultipleEndings(baz="a", foo="b", bar="c")
