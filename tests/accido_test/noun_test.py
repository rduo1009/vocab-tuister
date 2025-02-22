import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


import pytest

from src.core.accido.exceptions import InvalidInputError  # isort: skip
from src.core.accido.endings import Adjective, Noun
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


@pytest.fixture
def noun_firstdeclension():
    return Noun("ancilla", "ancillae", gender=Gender.FEMININE, meaning="slavegirl")


@pytest.fixture
def noun_firstdeclension_plonly():
    return Noun("divitae", "divitiarum", gender=Gender.FEMININE, meaning="riches")


@pytest.fixture
def noun_seconddeclension():
    return Noun("servus", "servi", gender=Gender.MASCULINE, meaning="slave")


@pytest.fixture
def noun_seconddeclension_neuter():
    return Noun("templum", "templi", gender=Gender.NEUTER, meaning="templ")


@pytest.fixture
def noun_seconddeclension_irregular():
    return Noun("puer", "pueri", gender=Gender.MASCULINE, meaning="boy")


@pytest.fixture
def noun_seconddeclension_plonly():
    return Noun("castra", "castrorum", gender=Gender.NEUTER, meaning="camp")


@pytest.fixture
def noun_thirddeclension():
    return Noun("carcer", "carceris", gender=Gender.MASCULINE, meaning="prison")


@pytest.fixture
def noun_thirddeclension_neuter():
    return Noun("litus", "litoris", gender=Gender.NEUTER, meaning="beach")


@pytest.fixture
def noun_thirddeclension_plonly():
    return Noun("opes", "opum", gender=Gender.FEMININE, meaning="wealth")


@pytest.fixture
def noun_fourthdeclension():
    return Noun("manus", "manus", gender=Gender.FEMININE, meaning="hand")


@pytest.fixture
def noun_fourthdeclension_neuter():
    return Noun("cornu", "cornus", gender=Gender.NEUTER, meaning="horn")


@pytest.fixture
def noun_fourthdeclension_plonly():
    return Noun("Quinquatrus", "Quinquatruum", gender=Gender.FEMININE, meaning="Minerva festival")


@pytest.fixture
def noun_fifthdeclension():
    return Noun("res", "rei", gender=Gender.FEMININE, meaning="thing")


NOUN_COMBINATIONS = (
    (Case.NOMINATIVE, Number.SINGULAR),
    (Case.VOCATIVE, Number.SINGULAR),
    (Case.ACCUSATIVE, Number.SINGULAR),
    (Case.GENITIVE, Number.SINGULAR),
    (Case.DATIVE, Number.SINGULAR),
    (Case.ABLATIVE, Number.SINGULAR),
    (Case.NOMINATIVE, Number.PLURAL),
    (Case.VOCATIVE, Number.PLURAL),
    (Case.ACCUSATIVE, Number.PLURAL),
    (Case.GENITIVE, Number.PLURAL),
    (Case.DATIVE, Number.PLURAL),
    (Case.ABLATIVE, Number.PLURAL),
)


class TestNounDeclension:
    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "ancilla", "ancilla", "ancillam", "ancillae", "ancillae", "ancilla",
        "ancillae", "ancillae", "ancillas", "ancillarum", "ancillis", "ancillis",
    ])])  # fmt: skip
    def test_firstdeclension(self, noun_firstdeclension, case, number, expected):
        assert noun_firstdeclension.get(case=case, number=number) == expected

    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "servus", "serve", "servum", "servi", "servo", "servo",
        "servi", "servi", "servos", "servorum", "servis", "servis",
    ])])  # fmt: skip
    def test_seconddeclension_regular(self, noun_seconddeclension, case, number, expected):
        assert noun_seconddeclension.get(case=case, number=number) == expected

    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "puer", "puer", "puerum", "pueri", "puero", "puero",
        "pueri", "pueri", "pueros", "puerorum", "pueris", "pueris",
    ])])  # fmt: skip
    def test_seconddeclension_endinginr(self, noun_seconddeclension_irregular, case, number, expected):
        assert noun_seconddeclension_irregular.get(case=case, number=number) == expected

    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "carcer", "carcer", "carcerem", "carceris", "carceri", "carcere",
        "carceres", "carceres", "carceres", "carcerum", "carceribus", "carceribus",
    ])])  # fmt: skip
    def test_thirddeclension(self, noun_thirddeclension, case, number, expected):
        assert noun_thirddeclension.get(case=case, number=number) == expected

    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "manus", "manus", "manum", "manus", "manui", "manu", "manus",
        "manus", "manus", "manuum", "manibus", "manibus",
    ])])  # fmt: skip
    def test_fourthdeclension(self, noun_fourthdeclension, case, number, expected):
        assert noun_fourthdeclension.get(case=case, number=number) == expected

    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "res", "res", "rem", "rei", "rei", "re",
        "res", "res", "res", "rerum", "rebus", "rebus",
    ])])  # fmt: skip
    def test_fifthdeclension(self, noun_fifthdeclension, case, number, expected):
        assert noun_fifthdeclension.get(case=case, number=number) == expected


class TestNounNeuter:
    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "templum", "templum", "templum", "templi", "templo", "templo",
        "templa", "templa", "templa", "templorum", "templis", "templis",
    ])])  # fmt: skip
    def test_seconddeclension(self, noun_seconddeclension_neuter, case, number, expected):
        assert noun_seconddeclension_neuter.get(case=case, number=number) == expected

    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "litus", "litus", "litus", "litoris", "litori", "litore",
        "litora", "litora", "litora", "litorum", "litoribus", "litoribus",
    ])])  # fmt: skip
    def test_thirddeclension(self, noun_thirddeclension_neuter, case, number, expected):
        assert noun_thirddeclension_neuter.get(case=case, number=number) == expected

    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "cornu", "cornu", "cornu", "cornus", "cornu", "cornu",
        "cornua", "cornua", "cornua", "cornuum", "cornibus", "cornibus",
    ])])  # fmt: skip
    def test_fourthdeclension(self, noun_fourthdeclension_neuter, case, number, expected):
        assert noun_fourthdeclension_neuter.get(case=case, number=number) == expected


class TestNounPluraleTantum:
    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[len(NOUN_COMBINATIONS) // 2 :][i] + (form,) for i, form in enumerate([
        "divitiae", "divitiae", "divitias", "divitiarum", "divitiis", "divitiis",
    ])])  # fmt: skip
    def test_firstdeclension(self, noun_firstdeclension_plonly, case, number, expected):
        assert noun_firstdeclension_plonly.get(case=case, number=number) == expected

    @pytest.mark.parametrize(("case", "number", "expected"),  [NOUN_COMBINATIONS[len(NOUN_COMBINATIONS) // 2 :][i] + (form,) for i, form in enumerate([
        "castra", "castra", "castra", "castrorum", "castris", "castris",
    ])])  # fmt: skip
    def test_seconddeclension(self, noun_seconddeclension_plonly, case, number, expected):
        assert noun_seconddeclension_plonly.get(case=case, number=number) == expected

    @pytest.mark.parametrize(("case", "number", "expected"),  [NOUN_COMBINATIONS[len(NOUN_COMBINATIONS) // 2 :][i] + (form,) for i, form in enumerate([
        "opes", "opes", "opes", "opum", "opibus", "opibus",
    ])])  # fmt: skip
    def test_thirddeclension(self, noun_thirddeclension_plonly, case, number, expected):
        assert noun_thirddeclension_plonly.get(case=case, number=number) == expected

    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[len(NOUN_COMBINATIONS) // 2 :][i] + (form,) for i, form in enumerate([
        "Quinquatrus", "Quinquatrus", "Quinquatrus", "Quinquatruum", "Quinquatribus", "Quinquatribus",
    ])])  # fmt: skip
    def test_fourthdeclension(self, noun_fourthdeclension_plonly, case, number, expected):
        assert noun_fourthdeclension_plonly.get(case=case, number=number) == expected
