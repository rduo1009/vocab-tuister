import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from src.core.accido.endings import Noun, Pronoun, Verb
from src.core.accido.misc import Case, ComponentsSubtype, EndingComponents, Gender, Number


def test_eq():
    word1 = Verb("test1o", "testare", "test3i", "test4", meaning="test5")
    assert word1 != "error"


def test_eq_different_meaning():
    word1 = Verb("test1o", "testare", "test3i", "test4", meaning="test5")
    word2 = Verb("test1o", "testare", "test3i", "test4", meaning="something else")
    assert word1 != word2


def test_eq_different_endings():
    word1 = Verb("test1o", "testare", "test3i", "test4", meaning="test5")
    word2 = Verb("test1o", "testare", "test3i", "test4", meaning="test5")
    word2.endings["Vpreactindsg1"] = "error"
    assert word1 != word2


def test_lt():
    foo = Verb("test1o", "testare", "test3i", "test4", meaning="test5")
    with pytest.raises(TypeError) as error:
        _ = foo < "2"
    assert error


def test_getitem():
    word1 = Verb("test1o", "testare", "test3i", "test4", meaning="test5")
    assert word1["Vpreactindsg1"] == "test1o"


def test_find_same():
    word = Pronoun("ille", meaning="that")
    assert word.find("illa") == [
        EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.FEMININE, string="nominative singular feminine"),
        EndingComponents(case=Case.ABLATIVE, number=Number.SINGULAR, gender=Gender.FEMININE, string="ablative singular feminine"),
        EndingComponents(case=Case.NOMINATIVE, number=Number.PLURAL, gender=Gender.NEUTER, string="nominative plural neuter"),
        EndingComponents(case=Case.ACCUSATIVE, number=Number.PLURAL, gender=Gender.NEUTER, string="accusative plural neuter"),
    ]


def test_find_multipleendings():
    word = Noun("ego", meaning="I")
    a = EndingComponents(case=Case.GENITIVE, number=Number.PLURAL, string="genitive plural")
    a.subtype = ComponentsSubtype.PRONOUN
    assert word.find("nostrum") == [a]
