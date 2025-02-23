import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from src.core.accido.endings import Adjective, Noun
from src.core.accido.exceptions import InvalidInputError
from src.core.accido.misc import Case, EndingComponents, Gender, MultipleMeanings, Number
from src.utils import compare


class TestNounErrors:
    def test_errors_invalid_genitive(self):
        with pytest.raises(InvalidInputError) as error:
            Noun("puer", "error", gender=Gender.MASCULINE, meaning="boy")
        assert str(error.value) == "Invalid genitive form: 'error'"

    def test_errors_fifth_declension_neuter(self):
        with pytest.raises(InvalidInputError) as error:
            Noun("puer", "puerei", gender=Gender.NEUTER, meaning="boy")
        assert str(error.value) == "Fifth declension nouns cannot be neuter (noun 'puer' given)"


class TestNounDunder:
    def test_repr(self):
        word = Noun("puer", "pueri", gender=Gender.MASCULINE, meaning="boy")
        assert repr(word) == "Noun(puer, pueri, masculine, boy)"

    def test_eq(self):
        word1 = Noun("puer", "pueri", gender=Gender.MASCULINE, meaning="boy")
        word2 = Noun("puer", "pueri", gender=Gender.MASCULINE, meaning="boy")
        assert word1 == word2

    def test_lt(self):
        word1 = Noun("puer", "pueri", gender=Gender.MASCULINE, meaning="boy")
        word2 = Noun("apuer", "pueri", gender=Gender.MASCULINE, meaning="boy")
        # word2 must be smaller than word1 as word1.first = "puer" and word2.first = "apuer"
        assert word1 > word2

    def test_find(self):
        word = Noun("ancilla", "ancillae", gender=Gender.FEMININE, meaning="slavegirl")
        assert compare(word.find("ancilla"),
            [EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, string="nominative singular"),
                EndingComponents(case=Case.VOCATIVE, number=Number.SINGULAR, string="vocative singular"),
                    EndingComponents(case=Case.ABLATIVE, number=Number.SINGULAR, string="ablative singular")])  # fmt: skip

    def test_str_masculine(self):
        word = Noun("servus", "servi", gender=Gender.MASCULINE, meaning="slave")
        assert str(word) == "slave: servus, servi, (m)"

    def test_str_feminine(self):
        word = Noun("ancilla", "ancillae", gender=Gender.FEMININE, meaning="slavegirl")
        assert str(word) == "slavegirl: ancilla, ancillae, (f)"

    def test_str_neuter(self):
        word = Noun("templum", "templi", gender=Gender.NEUTER, meaning="temple")
        assert str(word) == "temple: templum, templi, (n)"

    def test_add_different_word(self):
        word1 = Noun("puella", "puellae", gender=Gender.FEMININE, meaning="girl")
        word2 = Noun("puer", "pueri", gender=Gender.MASCULINE, meaning="boy")
        with pytest.raises(TypeError):
            word1 + word2

    def test_add_different_pos(self):
        word1 = Noun("puella", "puellae", gender=Gender.FEMININE, meaning="girl")
        word2 = Adjective("celer", "celeris", "celere", termination=3, declension="3", meaning="quick")
        with pytest.raises(TypeError):
            word1 + word2

    def test_add(self):
        word1 = Noun("puella", "puellae", gender=Gender.FEMININE, meaning="girl")
        word2 = Noun("puella", "puellae", gender=Gender.FEMININE, meaning="maiden")
        assert word1 + word2 == Noun("puella", "puellae", gender=Gender.FEMININE, meaning=MultipleMeanings(("girl", "maiden")))
