import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


import pytest

from src.core.accido.exceptions import InvalidInputError  # isort: skip
from src.core.accido.endings import Adjective, Noun
from src.core.accido.misc import Case, Degree, EndingComponents, Gender, MultipleMeanings, Number
from src.utils import compare


class TestAdjectiveErrors:
    def test_errors_wrong_number_principal_parts_212(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("laetus", "laeta", declension="212", meaning="happy")
        assert str(error.value) == "2-1-2 adjectives must have 3 principal parts (adjective 'laetus' given)"

    def test_errors_wrong_number_principal_parts_31(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("laetus", "laeta", "laetum", declension="3", meaning="happy", termination=1)
        assert str(error.value) == "First-termination adjectives must have 2 principal parts (adjective 'laetus' given)"

    def test_errors_invalid_genitive(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("laetus", "laeta", declension="3", meaning="happy", termination=1)
        assert str(error.value) == "Invalid genitive form: 'laeta' (must end in '-is')"

    def test_errors_wrong_number_principal_parts_32(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("laetus", "laeta", "laetum", declension="3", meaning="happy", termination=2)
        assert str(error.value) == "Second-termination adjectives must have 2 principal parts (adjective 'laetus' given)"

    def test_errors_wrong_number_principal_parts_33(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("laetus", "laeta", declension="3", meaning="happy", termination=3)
        assert str(error.value) == "Third-termination adjectives must have 3 principal parts (adjective 'laetus' given)"


class TestAdjectiveDunder:
    def test_repr(self):
        word = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")
        assert repr(word) == "Adjective(laetus, laeta, laetum, None, 212, happy)"

    def test_eq(self):
        word1 = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")
        word2 = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")
        assert word1 == word2

    def test_lt(self):
        word1 = Adjective("aalaetus", "laeta", "laetum", declension="212", meaning="happy")
        word2 = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")
        assert word1 < word2

    def test_find(self):
        word = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")

        assert compare(
            word.find("laeta"),
            [
                EndingComponents(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR, string="positive nominative singular feminine"),
                EndingComponents(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR, string="positive vocative singular feminine"),
                EndingComponents(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR, string="positive ablative singular feminine"),
                EndingComponents(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL, string="positive nominative plural neuter"),
                EndingComponents(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL, string="positive vocative plural neuter"),
                EndingComponents(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL, string="positive accusative plural neuter"),
            ],
        )

        assert compare(word.find("laete"), [EndingComponents(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR, string="positive vocative singular masculine"), EndingComponents(degree=Degree.POSITIVE, string="positive")])

    def test_str_212(self):
        word = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")
        assert str(word) == "happy: laetus, laeta, laetum, (2-1-2)"

    def test_str_31(self):
        word = Adjective("egens", "egentis", termination=1, declension="3", meaning="poor")
        assert str(word) == "poor: egens, egentis, (3-1)"

    def test_str_32(self):
        word = Adjective("facilis", "facile", termination=2, declension="3", meaning="easy")
        assert str(word) == "easy: facilis, facile, (3-2)"

    def test_str_33(self):
        word = Adjective("celer", "celeris", "celere", termination=3, declension="3", meaning="quick")
        assert str(word) == "quick: celer, celeris, celere, (3-3)"

    def test_add_different_word(self):
        word1 = Adjective("celer", "celeris", "celere", termination=3, declension="3", meaning="quick")
        word2 = Adjective("ingens", "ingentis", termination=1, declension="3", meaning="huge")
        with pytest.raises(TypeError):
            word1 + word2

    def test_add_different_pos(self):
        word1 = Adjective("celer", "celeris", "celere", termination=3, declension="3", meaning="quick")
        word2 = Noun("puella", "puellae", gender=Gender.FEMININE, meaning="girl")
        with pytest.raises(TypeError):
            word1 + word2

    def test_add(self):
        word1 = Adjective("celer", "celeris", "celere", termination=3, declension="3", meaning="quick")
        word2 = Adjective("celer", "celeris", "celere", termination=3, declension="3", meaning="fast")
        assert word1 + word2 == Adjective("celer", "celeris", "celere", termination=3, declension="3", meaning=MultipleMeanings(("quick", "fast")))


class TestAdjectiveDeclension:
    def test_declension212(self):
        word = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "laetus"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "laete"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "laetum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "laeti"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "laeto"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "laeto"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "laeti"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "laeti"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "laetos"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "laetorum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "laetis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "laetis"

        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "laeta"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "laeta"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "laetam"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "laetae"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "laetae"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "laeta"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "laetae"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "laetae"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "laetas"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "laetarum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "laetis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "laetis"

        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "laetum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "laetum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "laetum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "laeti"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "laeto"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "laeto"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "laeta"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "laeta"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "laeta"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "laetorum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "laetis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "laetis"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "laetior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "laetior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "laetiorem"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "laetioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "laetiori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "laetiore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "laetiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "laetiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "laetiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "laetiorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "laetioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "laetioribus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "laetior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "laetior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "laetiorem"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "laetioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "laetiori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "laetiore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "laetiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "laetiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "laetiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "laetiorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "laetioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "laetioribus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "laetius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "laetius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "laetius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "laetioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "laetiori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "laetiore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "laetiora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "laetiora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "laetiora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "laetiorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "laetioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "laetioribus"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "laetissimus"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "laetissime"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "laetissimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "laetissimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "laetissimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "laetissimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "laetissimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "laetissimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "laetissimos"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "laetissimorum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "laetissimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "laetissimis"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "laetissima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "laetissima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "laetissimam"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "laetissimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "laetissimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "laetissima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "laetissimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "laetissimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "laetissimas"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "laetissimarum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "laetissimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "laetissimis"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "laetissimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "laetissimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "laetissimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "laetissimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "laetissimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "laetissimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "laetissima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "laetissima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "laetissima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "laetissimorum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "laetissimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "laetissimis"

    def test_declension212_er(self):
        word = Adjective("miser", "misera", "miserum", declension="212", meaning="happy")
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "miser"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "miser"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "miserum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "miseri"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "misero"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "misero"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "miseri"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "miseri"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "miseros"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "miserorum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "miseris"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "miseris"

        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "misera"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "misera"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "miseram"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "miserae"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "miserae"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "misera"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "miserae"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "miserae"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "miseras"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "miserarum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "miseris"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "miseris"

        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "miserum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "miserum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "miserum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "miseri"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "misero"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "misero"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "misera"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "misera"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "misera"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "miserorum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "miseris"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "miseris"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "miserior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "miserior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "miseriorem"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "miserioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "miseriori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "miseriore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "miseriores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "miseriores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "miseriores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "miseriorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "miserioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "miserioribus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "miserior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "miserior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "miseriorem"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "miserioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "miseriori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "miseriore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "miseriores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "miseriores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "miseriores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "miseriorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "miserioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "miserioribus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "miserius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "miserius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "miserius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "miserioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "miseriori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "miseriore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "miseriora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "miseriora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "miseriora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "miseriorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "miserioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "miserioribus"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "miserrimus"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "miserrime"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "miserrimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "miserrimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "miserrimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "miserrimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "miserrimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "miserrimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "miserrimos"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "miserrimorum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "miserrimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "miserrimis"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "miserrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "miserrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "miserrimam"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "miserrimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "miserrimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "miserrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "miserrimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "miserrimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "miserrimas"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "miserrimarum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "miserrimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "miserrimis"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "miserrimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "miserrimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "miserrimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "miserrimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "miserrimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "miserrimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "miserrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "miserrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "miserrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "miserrimorum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "miserrimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "miserrimis"

    def test_declension212_irregular(self):
        word = Adjective("bonus", "bona", "bonum", declension="212", meaning="happy")
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "bonus"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "bone"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "bonum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "boni"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "bono"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "bono"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "boni"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "boni"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "bonos"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "bonorum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "bonis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "bonis"

        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "bona"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "bona"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "bonam"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "bonae"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "bonae"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "bona"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "bonae"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "bonae"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "bonas"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "bonarum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "bonis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "bonis"

        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "bonum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "bonum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "bonum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "boni"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "bono"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "bono"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "bona"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "bona"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "bona"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "bonorum"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "bonis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "bonis"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "melior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "melior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "meliorem"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "melioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "meliori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "meliore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "meliores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "meliores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "meliores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "meliorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "melioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "melioribus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "melior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "melior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "meliorem"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "melioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "meliori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "meliore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "meliores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "meliores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "meliores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "meliorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "melioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "melioribus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "melius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "melius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "melius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "melioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "meliori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "meliore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "meliora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "meliora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "meliora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "meliorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "melioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "melioribus"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "optimus"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "optime"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "optimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "optimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "optimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "optimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "optimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "optimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "optimos"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "optimorum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "optimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "optimis"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "optima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "optima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "optimam"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "optimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "optimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "optima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "optimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "optimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "optimas"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "optimarum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "optimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "optimis"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "optimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "optimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "optimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "optimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "optimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "optimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "optima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "optima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "optima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "optimorum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "optimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "optimis"

    def test_declension3_1_regular(self):
        word = Adjective("egens", "egentis", termination=1, declension="3", meaning="poor")
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "egens"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "egens"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "egentem"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "egentis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "egenti"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "egenti"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "egentes"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "egentes"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "egentes"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "egentium"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "egentibus"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "egentibus"

        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "egens"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "egens"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "egentem"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "egentis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "egenti"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "egenti"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "egentes"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "egentes"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "egentes"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "egentium"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "egentibus"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "egentibus"

        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "egens"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "egens"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "egens"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "egentis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "egenti"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "egenti"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "egentia"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "egentia"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "egentia"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "egentium"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "egentibus"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "egentibus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "egentior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "egentior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "egentiorem"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "egentioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "egentiori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "egentiore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "egentiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "egentiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "egentiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "egentiorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "egentioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "egentioribus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "egentior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "egentior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "egentiorem"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "egentioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "egentiori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "egentiore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "egentiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "egentiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "egentiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "egentiorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "egentioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "egentioribus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "egentius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "egentius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "egentius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "egentioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "egentiori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "egentiore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "egentiora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "egentiora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "egentiora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "egentiorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "egentioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "egentioribus"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "egentissimus"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "egentissime"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "egentissimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "egentissimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "egentissimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "egentissimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "egentissimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "egentissimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "egentissimos"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "egentissimorum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "egentissimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "egentissimis"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "egentissima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "egentissima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "egentissimam"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "egentissimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "egentissimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "egentissima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "egentissimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "egentissimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "egentissimas"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "egentissimarum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "egentissimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "egentissimis"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "egentissimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "egentissimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "egentissimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "egentissimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "egentissimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "egentissimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "egentissima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "egentissima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "egentissima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "egentissimorum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "egentissimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "egentissimis"

    def test_declension3_1_with_rr(self):
        word = Adjective("uber", "uberis", termination=1, declension="3", meaning="fruitful")

        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "uber"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "uber"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "uberem"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "uberis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "uberi"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "uberi"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "uberes"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "uberes"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "uberes"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "uberium"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "uberibus"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "uberibus"

        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "uber"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "uber"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "uberem"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "uberis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "uberi"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "uberi"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "uberes"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "uberes"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "uberes"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "uberium"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "uberibus"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "uberibus"

        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "uber"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "uber"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "uber"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "uberis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "uberi"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "uberi"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "uberia"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "uberia"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "uberia"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "uberium"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "uberibus"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "uberibus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "uberior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "uberior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "uberiorem"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "uberioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "uberiori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "uberiore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "uberiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "uberiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "uberiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "uberiorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "uberioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "uberioribus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "uberior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "uberior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "uberiorem"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "uberioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "uberiori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "uberiore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "uberiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "uberiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "uberiores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "uberiorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "uberioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "uberioribus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "uberius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "uberius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "uberius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "uberioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "uberiori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "uberiore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "uberiora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "uberiora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "uberiora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "uberiorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "uberioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "uberioribus"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "uberrimus"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "uberrime"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "uberrimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "uberrimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "uberrimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "uberrimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "uberrimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "uberrimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "uberrimos"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "uberrimorum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "uberrimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "uberrimis"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "uberrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "uberrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "uberrimam"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "uberrimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "uberrimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "uberrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "uberrimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "uberrimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "uberrimas"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "uberrimarum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "uberrimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "uberrimis"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "uberrimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "uberrimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "uberrimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "uberrimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "uberrimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "uberrimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "uberrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "uberrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "uberrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "uberrimorum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "uberrimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "uberrimis"

    def test_declension3_2(self):
        word = Adjective("facilis", "facile", termination=2, declension="3", meaning="easy")
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "facilis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "facilis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "facilem"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "facilis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "facili"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "facili"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "faciles"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "faciles"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "faciles"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "facilium"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "facilibus"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "facilibus"

        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "facilis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "facilis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "facilem"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "facilis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "facili"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "facili"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "faciles"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "faciles"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "faciles"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "facilium"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "facilibus"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "facilibus"

        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "facile"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "facile"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "facile"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "facilis"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "facili"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "facili"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "facilia"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "facilia"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "facilia"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "facilium"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "facilibus"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "facilibus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "facilior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "facilior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "faciliorem"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "facilioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "faciliori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "faciliore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "faciliores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "faciliores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "faciliores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "faciliorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "facilioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "facilioribus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "facilior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "facilior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "faciliorem"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "facilioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "faciliori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "faciliore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "faciliores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "faciliores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "faciliores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "faciliorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "facilioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "facilioribus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "facilius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "facilius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "facilius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "facilioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "faciliori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "faciliore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "faciliora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "faciliora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "faciliora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "faciliorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "facilioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "facilioribus"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "facillimus"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "facillime"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "facillimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "facillimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "facillimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "facillimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "facillimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "facillimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "facillimos"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "facillimorum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "facillimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "facillimis"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "facillima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "facillima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "facillimam"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "facillimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "facillimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "facillima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "facillimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "facillimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "facillimas"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "facillimarum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "facillimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "facillimis"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "facillimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "facillimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "facillimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "facillimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "facillimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "facillimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "facillima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "facillima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "facillima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "facillimorum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "facillimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "facillimis"

    def test_declension3_3(self):
        word = Adjective("celer", "celeris", "celere", termination=3, declension="3", meaning="quick")
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "celer"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "celer"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "celerem"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "celeris"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "celeri"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "celeri"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "celeres"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "celeres"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "celeres"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "celerium"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "celeribus"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "celeribus"

        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "celeris"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "celeris"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "celerem"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "celeris"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "celeri"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "celeri"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "celeres"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "celeres"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "celeres"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "celerium"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "celeribus"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "celeribus"

        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "celere"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "celere"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "celere"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "celeris"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "celeri"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "celeri"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "celeria"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "celeria"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "celeria"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "celerium"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "celeribus"
        assert word.get(degree=Degree.POSITIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "celeribus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "celerior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "celerior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "celeriorem"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "celerioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "celeriori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "celeriore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "celeriores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "celeriores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "celeriores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "celeriorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "celerioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "celerioribus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "celerior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "celerior"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "celeriorem"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "celerioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "celeriori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "celeriore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "celeriores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "celeriores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "celeriores"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "celeriorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "celerioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "celerioribus"

        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "celerius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "celerius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "celerius"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "celerioris"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "celeriori"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "celeriore"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "celeriora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "celeriora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "celeriora"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "celeriorum"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "celerioribus"
        assert word.get(degree=Degree.COMPARATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "celerioribus"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "celerrimus"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR) == "celerrime"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "celerrimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.SINGULAR) == "celerrimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.SINGULAR) == "celerrimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.SINGULAR) == "celerrimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.PLURAL) == "celerrimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.PLURAL) == "celerrimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "celerrimos"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.GENITIVE, number=Number.PLURAL) == "celerrimorum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.DATIVE, number=Number.PLURAL) == "celerrimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.MASCULINE, case=Case.ABLATIVE, number=Number.PLURAL) == "celerrimis"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.SINGULAR) == "celerrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.SINGULAR) == "celerrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "celerrimam"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.SINGULAR) == "celerrimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.SINGULAR) == "celerrimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.SINGULAR) == "celerrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.NOMINATIVE, number=Number.PLURAL) == "celerrimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.VOCATIVE, number=Number.PLURAL) == "celerrimae"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ACCUSATIVE, number=Number.PLURAL) == "celerrimas"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.GENITIVE, number=Number.PLURAL) == "celerrimarum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.DATIVE, number=Number.PLURAL) == "celerrimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.FEMININE, case=Case.ABLATIVE, number=Number.PLURAL) == "celerrimis"

        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.SINGULAR) == "celerrimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.SINGULAR) == "celerrimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.SINGULAR) == "celerrimum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.SINGULAR) == "celerrimi"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.SINGULAR) == "celerrimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.SINGULAR) == "celerrimo"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.NOMINATIVE, number=Number.PLURAL) == "celerrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.VOCATIVE, number=Number.PLURAL) == "celerrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ACCUSATIVE, number=Number.PLURAL) == "celerrima"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.GENITIVE, number=Number.PLURAL) == "celerrimorum"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.DATIVE, number=Number.PLURAL) == "celerrimis"
        assert word.get(degree=Degree.SUPERLATIVE, gender=Gender.NEUTER, case=Case.ABLATIVE, number=Number.PLURAL) == "celerrimis"


class TestAdverb:
    def test_adverb_212(self):
        word = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")
        assert word.get(degree=Degree.POSITIVE, adverb=True) == "laete"
        assert word.get(degree=Degree.COMPARATIVE, adverb=True) == "laetius"
        assert word.get(degree=Degree.SUPERLATIVE, adverb=True) == "laetissime"

    def test_adverb_31(self):
        word = Adjective("prudens", "prudentis", termination=1, declension="3", meaning="wise")
        assert word.get(degree=Degree.POSITIVE, adverb=True) == "prudenter"
        assert word.get(degree=Degree.COMPARATIVE, adverb=True) == "prudentius"
        assert word.get(degree=Degree.SUPERLATIVE, adverb=True) == "prudentissime"

    def test_adverb_32(self):
        word = Adjective("fortis", "forte", termination=2, declension="3", meaning="strong")
        assert word.get(degree=Degree.POSITIVE, adverb=True) == "fortiter"
        assert word.get(degree=Degree.COMPARATIVE, adverb=True) == "fortius"
        assert word.get(degree=Degree.SUPERLATIVE, adverb=True) == "fortissime"

    def test_adverb_33(self):
        word = Adjective("celer", "celeris", "celere", termination=3, declension="3", meaning="quick")
        assert word.get(degree=Degree.POSITIVE, adverb=True) == "celeriter"
        assert word.get(degree=Degree.COMPARATIVE, adverb=True) == "celerius"
        assert word.get(degree=Degree.SUPERLATIVE, adverb=True) == "celerrime"

    def test_irregularadverb1(self):
        word = Adjective("bonus", "bona", "bonum", declension="212", meaning="happy")
        assert word.get(degree=Degree.POSITIVE, adverb=True) == "bene"
        assert word.get(degree=Degree.COMPARATIVE, adverb=True) == "melius"
        assert word.get(degree=Degree.SUPERLATIVE, adverb=True) == "optime"

    def test_irregularadverb2(self):
        word = Adjective("bonus", "bonis", declension="3", termination=1, meaning="happy")
        assert word.get(degree=Degree.POSITIVE, adverb=True) == "bene"
        assert word.get(degree=Degree.COMPARATIVE, adverb=True) == "melius"
        assert word.get(degree=Degree.SUPERLATIVE, adverb=True) == "optime"

    def test_irregularadverb3(self):
        word = Adjective("bonus", "bona", declension="3", termination=2, meaning="happy")
        assert word.get(degree=Degree.POSITIVE, adverb=True) == "bene"
        assert word.get(degree=Degree.COMPARATIVE, adverb=True) == "melius"
        assert word.get(degree=Degree.SUPERLATIVE, adverb=True) == "optime"

    def test_irregularadverb4(self):
        word = Adjective("bonus", "bona", "bonum", declension="3", termination=3, meaning="happy")
        assert word.get(degree=Degree.POSITIVE, adverb=True) == "bene"
        assert word.get(degree=Degree.COMPARATIVE, adverb=True) == "melius"
        assert word.get(degree=Degree.SUPERLATIVE, adverb=True) == "optime"

    def test_irregularadverb_noadverb(self):
        word = Adjective("magnus", "magna", "magnum", declension="212", meaning="big")
        a = word.get(degree=Degree.POSITIVE, adverb=True)
        assert a is None
