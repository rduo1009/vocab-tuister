import pytest
from src.core.accido.endings import Noun, Verb
from src.core.accido.exceptions import InvalidInputError
from src.core.accido.misc import Case, EndingComponents, Gender, Mood, MultipleMeanings, Number, Tense, Voice
from src.utils import compare


class TestVerbErrors:
    def test_errors_invalid_infinitive(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("celo", "error", "celavi", "celatus", meaning="hide")
        assert str(error.value) == "Invalid infinitive form: 'error'"

    def test_errors_invalid_present(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("errorr", "celare", "celavi", "celatus", meaning="hide")  # error ends in -or!
        assert str(error.value) == "Invalid present form: 'errorr' (must end in '-o')"

    def test_errors_invalid_perfect(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("celo", "celare", "error", "celatus", meaning="hide")
        assert str(error.value) == "Invalid perfect form: 'error' (must end in '-i')"

    def test_ppp_ends_in_um(self):
        word1 = Verb("celo", "celare", "celavi", "celatum", meaning="hide")
        assert word1.endings["Vperpasindsg1"] == "celatus sum"

    def test_errors_missing_infinitive(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("celo", meaning="hide")
        assert str(error.value) == "Verb 'celo' is not irregular, but no infinitive provided."

    def test_errors_deponent_missing_perfect(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("loquor", "loqui", meaning="say")
        assert str(error.value) == "Verb 'loquor' is not irregular, but no perfect provided."

    def test_errors_deponent_with_ppp(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("loquor", "loqui", "locutus sum", "locutus", meaning="say")
        assert str(error.value) == "Verb 'loquor' is deponent, but ppp provided."

    def test_errors_deponent_invalid_perfect(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("loquor", "loqui", "locutus", meaning="say")
        assert str(error.value) == "Invalid perfect form: 'locutus' (must have 'sum')"

    def test_errors_semideponent_with_ppp(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("fido", "fidere", "fisus sum", "fisus", meaning="trust")
        assert str(error.value) == "Verb 'fido' is semi-deponent, but ppp provided."

    def test_errors_semideponent_invalid_present(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("fidus", "fidere", "fisus sum", meaning="trust")
        assert str(error.value) == "Invalid present form: 'fidus' (must end in '-o')"

    def test_errors_semideponent_invalid_infinitive(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("fido", "fiderus", "fisus sum", meaning="trust")
        assert str(error.value) == "Invalid infinitive form for semi-deponent: 'fiderus'"

    def test_errors_invalid_ppp_not_us(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("celo", "celare", "celavi", "celatux", meaning="hide")
        assert str(error.value) == "Invalid perfect passive participle form: 'celatux' (must end in '-us')"

    def test_errors_invalid_fap(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("caleo", "calere", "calui", "caliturux", meaning="hide")
        assert str(error.value) == "Invalid future active participle form: 'caliturux' (must end in '-urus')"

    def test_errors_missing_perfect(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("amo", "amare", ppp="amatus", meaning="love")  # pyright: ignore[reportCallIssue]
        assert str(error.value) == "Verb 'amo' is not irregular, but no perfect provided."

    def test_errors_missing_ppp(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("amo", "amare", "amavi", meaning="love")
        assert str(error.value) == "Verb 'amo' is not irregular or deponent, but no ppp provided."


class TestVerbDunder:
    def test_getnone(self):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert not word.get(tense=Tense.FUTURE_PERFECT, voice=Voice.PASSIVE, mood=Mood.SUBJUNCTIVE, person=2, number=Number.PLURAL)

    def test_repr(self):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert repr(word) == "Verb(celo, celare, celavi, celatus, meaning=hide)"

    def test_repr_noppp(self):
        word = Verb("loquor", "loqui", "locutus sum", meaning="say")
        assert repr(word) == "Verb(loquor, loqui, locutus sum, meaning=say)"

    def test_repr_irregular(self):
        word = Verb("inquam", meaning="say")
        assert repr(word) == "Verb(inquam, meaning=say)"

    def test_str(self):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert str(word) == "hide: celo, celare, celavi, celatus"

    def test_str_noppp(self):
        word = Verb("loquor", "loqui", "locutus sum", meaning="say")
        assert str(word) == "say: loquor, loqui, locutus sum"

    def test_str_irregular(self):
        word = Verb("inquam", meaning="say")
        assert str(word) == "say: inquam"

    def test_eq(self):
        word1 = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        word2 = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert word1 == word2

    def test_lt(self):
        word1 = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        word2 = Verb("amo", "amare", "amavi", "amatus", meaning="love")
        # word2 must be smaller than word1 as word1.first = "test1" and word2.first = "aaatest1"
        assert word1 > word2

    def test_find(self):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert compare(word.find("celabam"), [EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1, string="imperfect active indicative singular 1st person")])

    def test_find_participle(self):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert compare(word.find("celatus"), [EndingComponents(tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR, string="perfect passive participle masculine nominative singular")])

    # def test_find_infinitive(self):
    #     word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
    #     assert compare(word.find("celare"), [EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INFINITIVE, string="present active infinitive")])

    def test_add_different_word(self):
        word1 = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        word2 = Verb("amo", "amare", "amavi", "amatus", meaning="love")
        with pytest.raises(TypeError):
            word1 + word2

    def test_add_different_pos(self):
        word1 = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        word2 = Noun("puella", "puellae", gender=Gender.FEMININE, meaning="girl")
        with pytest.raises(TypeError):
            word1 + word2

    def test_add(self):
        word1 = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        word2 = Verb("celo", "celare", "celavi", "celatus", meaning="conceal")
        assert word1 + word2 == Verb("celo", "celare", "celavi", "celatus", meaning=MultipleMeanings(("hide", "conceal")))

    def test_add_irregular(self):
        word1 = Verb("inquam", meaning="say")
        word2 = Verb("inquam", meaning="speak")
        assert word1 + word2 == Verb("inquam", meaning=MultipleMeanings(("say", "speak")))
