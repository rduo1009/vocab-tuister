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
