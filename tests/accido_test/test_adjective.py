import pytest
from src.core.accido.endings import Adjective, Noun
from src.core.accido.exceptions import InvalidInputError
from src.core.accido.misc import Case, Degree, EndingComponents, Gender, MultipleMeanings, Number
from src.utils import compare


class TestAdjectiveErrors:
    def test_errors_wrong_number_principal_parts_212(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("laetus", "laeta", declension="212", meaning="happy")
        assert str(error.value) == "2-1-2 adjectives must have 3 principal parts. (adjective 'laetus' given)"

    def test_errors_wrong_number_principal_parts_31(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("laetus", "laeta", "laetum", declension="3", meaning="happy", termination=1)
        assert str(error.value) == "First-termination adjectives must have 2 principal parts. (adjective 'laetus' given)"

    def test_errors_invalid_genitive(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("laetus", "laeta", declension="3", meaning="happy", termination=1)
        assert str(error.value) == "Invalid genitive form: 'laeta' (must end in '-is')"

    def test_errors_wrong_number_principal_parts_32(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("laetus", "laeta", "laetum", declension="3", meaning="happy", termination=2)
        assert str(error.value) == "Second-termination adjectives must have 2 principal parts. (adjective 'laetus' given)"

    def test_errors_wrong_number_principal_parts_33(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("laetus", "laeta", declension="3", meaning="happy", termination=3)
        assert str(error.value) == "Third-termination adjectives must have 3 principal parts. (adjective 'laetus' given)"

    # Tests for 2-1-2 adjective principal parts validation
    def test_errors_invalid_masculine_212(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("laeta", "laeta", "laetum", declension="212", meaning="happy")
        assert str(error.value) == "Invalid masculine form: 'laeta' (must end in '-us' or '-er')"

    def test_errors_invalid_feminine_212(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("laetus", "laetus", "laetum", declension="212", meaning="happy")
        assert str(error.value) == "Invalid feminine form: 'laetus' (must end in '-a')"

    def test_errors_invalid_neuter_212(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("laetus", "laeta", "laetus", declension="212", meaning="happy")
        assert str(error.value) == "Invalid neuter form: 'laetus' (must end in '-um')"

    # Tests for 3-2 adjective principal parts validation
    def test_errors_invalid_masculine_32(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("facile", "facile", declension="3", meaning="easy", termination=2)
        assert str(error.value) == "Invalid masculine form: 'facile' (must end in '-is')"

    def test_errors_invalid_neuter_32(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("facilis", "facilis", declension="3", meaning="easy", termination=2)
        assert str(error.value) == "Invalid neuter form: 'facilis' (must end in '-e')"

    # Tests for 3-3 adjective principal parts validation
    def test_errors_invalid_masculine_33(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("celeris", "celeris", "celere", declension="3", meaning="quick", termination=3)
        assert str(error.value) == "Invalid masculine form: 'celeris' (must end in '-er')"

    def test_errors_invalid_feminine_33(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("celer", "celere", "celere", declension="3", meaning="quick", termination=3)
        assert str(error.value) == "Invalid feminine form: 'celere' (must end in '-is')"

    def test_errors_invalid_neuter_33(self):
        with pytest.raises(InvalidInputError) as error:
            Adjective("celer", "celeris", "celeris", declension="3", meaning="quick", termination=3)
        assert str(error.value) == "Invalid neuter form: 'celeris' (must end in '-e')"


class TestAdjectiveDunder:
    def test_repr(self):
        word = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")
        assert repr(word) == "Adjective(laetus, laeta, laetum, termination=None, declension=212, meaning=happy)"

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

        assert compare(word.find("laete"), [EndingComponents(degree=Degree.POSITIVE, gender=Gender.MASCULINE, case=Case.VOCATIVE, number=Number.SINGULAR, string="positive vocative singular masculine"), EndingComponents(degree=Degree.POSITIVE, string="positive (adverb)")])

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
