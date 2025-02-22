import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest

from src.core.accido.exceptions import InvalidInputError  # isort: skip
from src.core.accido.endings import Noun, Verb
from src.core.accido.misc import Case, EndingComponents, Gender, Mood, MultipleMeanings, Number, Tense, Voice
from src.utils import compare


class TestVerbErrors:
    def test_errors_invalid_infinitive(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("celo", "error", "celavi", "celatus", meaning="hide")
        assert str(error.value) == "Invalid infinitive form: 'error'"

    def test_errors_invalid_present(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("error", "celare", "celavi", "celatus", meaning="hide")
        assert str(error.value) == "Invalid present form: 'error' (must end in '-o')"

    def test_errors_invalid_perfect(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("celo", "celare", "error", "celatus", meaning="hide")
        assert str(error.value) == "Invalid perfect form: 'error' (must end in '-i')"


class TestVerbDunder:
    def test_getnone(self):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert not word.get(tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.INDICATIVE, person=2, number=Number.PLURAL)

    def test_repr(self):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert repr(word) == "Verb(celo, celare, celavi, celatus, hide)"

    def test_verb_str(self):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert str(word) == "hide: celo, celare, celavi, celatus"

    def test_verb_strnoppp(self):
        word = Verb("celo", "celare", "celavi", meaning="hide")
        assert str(word) == "hide: celo, celare, celavi"

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

    def test_find_infinitive(self):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert compare(word.find("celare"), [EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INFINITIVE, string="present active infinitive")])

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


VERB_COMBINATIONS = (
    (Tense.PRESENT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.INFINITIVE, None, None),
    (Tense.PRESENT, Voice.ACTIVE, Mood.IMPERATIVE, 2, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.IMPERATIVE, 2, Number.PLURAL),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 1, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 2, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 3, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 1, Number.PLURAL),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 2, Number.PLURAL),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 3, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 1, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 2, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 3, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 1, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 2, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 3, Number.PLURAL),
)


class TestVerbConjugation:
    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "celo", "celas", "celat", "celamus", "celatis", "celant",
        "celabam", "celabas", "celabat", "celabamus", "celabatis", "celabant",
        "celavi", "celavisti", "celavit", "celavimus", "celavistis", "celaverunt",
        "celaveram", "celaveras", "celaverat", "celaveramus", "celaveratis", "celaverant",

        "celare",
        "cela", "celate",

        "celarem", "celares", "celaret", "celaremus", "celaretis", "celarent",
        "celavissem", "celavisses", "celavisset", "celavissemus", "celavissetis", "celavissent",
    ])])  # fmt: skip
    def test_firstconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "pareo", "pares", "paret", "paremus", "paretis", "parent",
        "parebam", "parebas", "parebat", "parebamus", "parebatis", "parebant",
        "parui", "paruisti", "paruit", "paruimus", "paruistis", "paruerunt",
        "parueram", "parueras", "paruerat", "parueramus", "parueratis", "paruerant",

        "parere",
        "pare", "parete",

        "parerem", "pareres", "pareret", "pareremus", "pareretis", "parerent",
        "paruissem", "paruisses", "paruisset", "paruissemus", "paruissetis", "paruissent",
    ])])  # fmt: skip
    def test_secondconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("pareo", "parere", "parui", meaning="hide")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "desero", "deseris", "deserit", "deserimus", "deseritis", "deserunt",
        "deserebam", "deserebas", "deserebat", "deserebamus", "deserebatis", "deserebant",
        "deserui", "deseruisti", "deseruit", "deseruimus", "deseruistis", "deseruerunt",
        "deserueram", "deserueras", "deseruerat", "deserueramus", "deserueratis", "deseruerant",

        "deserere",
        "desere", "deserite",

        "desererem", "desereres", "desereret", "desereremus", "desereretis", "desererent",
        "deseruissem", "deseruisses", "deseruisset", "deseruissemus", "deseruissetis", "deseruissent",
    ])])  # fmt: skip
    def test_thirdconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("desero", "deserere", "deserui", "desertus", meaning="desert")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "facio", "facis", "facit", "facimus", "facitis", "faciunt",
        "faciebam", "faciebas", "faciebat", "faciebamus", "faciebatis", "faciebant",
        "feci", "fecisti", "fecit", "fecimus", "fecistis", "fecerunt",
        "feceram", "feceras", "fecerat", "feceramus", "feceratis", "fecerant",

        "facere",
        "face", "facite",
            
        "facerem", "faceres", "faceret", "faceremus", "faceretis", "facerent",
        "fecissem", "fecisses", "fecisset", "fecissemus", "fecissetis", "fecissent",
    ])])  # fmt: skip
    def test_thirdioconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("facio", "facere", "feci", "factus", meaning="make")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "aperio", "aperis", "aperit", "aperimus", "aperitis", "aperiunt",
        "aperiebam", "aperiebas", "aperiebat", "aperiebamus", "aperiebatis", "aperiebant",
        "aperui", "aperuisti", "aperuit", "aperuimus", "aperuistis", "aperuerunt",
        "aperueram", "aperueras", "aperuerat", "aperueramus", "aperueratis", "aperuerant",
            
        "aperire",
        "aperi", "aperite",

        "aperirem", "aperires", "aperiret", "aperiremus", "aperiretis", "aperirent",
        "aperuissem", "aperuisses", "aperuisset", "aperuissemus", "aperuissetis", "aperuissent",
    ])])  # fmt: skip
    def test_fourthconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("aperio", "aperire", "aperui", "apertus", meaning="open")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "abeo", "abis", "abit", "abimus", "abitis", "abeunt",
        "abibam", "abibas", "abibat", "abibamus", "abibatis", "abibant",
        "abii", "abisti", "abiit", "abiimus", "abistis", "abierunt",
        "abieram", "abieras", "abierat", "abieramus", "abieratis", "abierant",

        "abire",
        "abi", "abite",
            
        "abirem", "abires", "abiret", "abiremus", "abiretis", "abirent",
        "abissem", "abisses", "abisset", "abissemus", "abissetis", "abissent",
    ])])  # fmt: skip
    def test_irregularverb_eo(self, tense, voice, mood, person, number, expected):
        word = Verb("abeo", "abire", "abii", "abitum", meaning="depart")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected


class TestIrregularVerbInflection:
    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "sum", "es", "est", "sumus", "estis", "sunt",
        "eram", "eras", "erat", "eramus", "eratis", "erant",
        "fui", "fuisti", "fuit", "fuimus", "fuistis", "fuerunt",
        "fueram", "fueras", "fuerat", "fueramus", "fueratis", "fuerant",

        "esse",
        "es", "este",

        "essem", "esses", "esset", "essemus", "essetis", "essent",
        "fuissem", "fuisses", "fuisset", "fuissemus", "fuissetis", "fuissent",
    ])])  # fmt: skip
    def test_irregular_verb_normal(self, tense, voice, mood, person, number, expected):
        word = Verb("sum", "esse", "fui", meaning="be")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "adeo", "adis", "adit", "adimus", "aditis", "adeunt",
        "adibam", "adibas", "adibat", "adibamus", "adibatis", "adibant",
        "adii", "adisti", "adiit", "adiimus", "adistis", "adierunt",
        "adieram", "adieras", "adierat", "adieramus", "adieratis", "adierant",

        "adire",
        "adi", "adite",

        "adirem", "adires", "adiret", "adiremus", "adiretis", "adirent",
        "adissem", "adisses", "adisset", "adissemus", "adissetis", "adissent",
    ])])  # fmt: skip
    def test_irregular_verb_derived(self, tense, voice, mood, person, number, expected):
        word = Verb("adeo", "adire", "adii", "aditus", meaning="go to")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected


PARTICIPLE_COMBINATIONS = (
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.VOCATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.GENITIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.DATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ABLATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.NOMINATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.VOCATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.GENITIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.DATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ABLATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.VOCATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.GENITIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.DATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ABLATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.NOMINATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.VOCATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.GENITIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.DATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ABLATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.VOCATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.GENITIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.DATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ABLATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.NOMINATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.VOCATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.GENITIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.DATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ABLATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.VOCATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.GENITIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.DATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ABLATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.NOMINATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.VOCATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.GENITIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.DATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ABLATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.VOCATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.GENITIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.DATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ABLATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.NOMINATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.VOCATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.GENITIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.DATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ABLATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.VOCATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.GENITIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.DATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ABLATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.NOMINATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.VOCATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.GENITIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.DATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ABLATIVE, Number.PLURAL),
)


@pytest.mark.parametrize(("tense", "voice", "mood", "participle_gender", "participle_case", "number", "expected"), [PARTICIPLE_COMBINATIONS[i] + (form,) for i, form in enumerate([
    "portans", "portans", "portantem", "portantis", "portanti", "portante",
    "portantes", "portantes", "portantes", "portantium", "portantibus", "portantibus",
    "portans", "portans", "portantem", "portantis", "portanti", "portante",
    "portantes", "portantes", "portantes", "portantium", "portantibus", "portantibus",
    "portans", "portans", "portans", "portantis", "portanti", "portante",
    "portantia", "portantia", "portantia", "portantium", "portantibus", "portantibus",

    "portatus", "portate", "portatum", "portati", "portato", "portato",
    "portati", "portati", "portatos", "portatorum", "portatis", "portatis",
    "portata", "portata", "portatam", "portatae", "portatae", "portata",
    "portatae", "portatae", "portatas", "portatarum", "portatis", "portatis",
    "portatum", "portatum", "portatum", "portati", "portato", "portato",
    "portata", "portata", "portata", "portatorum", "portatis", "portatis",
])])  # fmt: skip
def test_participle_conjugation(tense, voice, mood, participle_gender, participle_case, number, expected):
    word = Verb("porto", "portare", "portavi", "portatus", meaning="carry")
    assert word.get(tense=tense, voice=voice, mood=mood, participle_gender=participle_gender, participle_case=participle_case, number=number) == expected
