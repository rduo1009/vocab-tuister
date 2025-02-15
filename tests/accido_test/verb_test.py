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


class TestVerbConjugation:
    def test_firstconjugation(self):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celo"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celas"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celamus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celatis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celant"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celabam"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celabas"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celabat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celabamus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celabatis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celabant"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celavi"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celavisti"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celavit"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celavimus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celavistis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celaverunt"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celaveram"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celaveras"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celaverat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celaveramus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celaveratis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "celaverant"

        assert word.get(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INFINITIVE) == "celare"

        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "cela"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "celate"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "celarem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "celares"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "celaret"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "celaremus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "celaretis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "celarent"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "celavissem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "celavisses"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "celavisset"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "celavissemus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "celavissetis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "celavissent"

    def test_secondconjugation(self):
        word = Verb("pareo", "parere", "parui", meaning="hide")

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "pareo"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "pares"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "paret"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "paremus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "paretis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "parent"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "parebam"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "parebas"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "parebat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "parebamus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "parebatis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "parebant"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "parui"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "paruisti"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "paruit"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "paruimus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "paruistis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "paruerunt"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "parueram"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "parueras"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "paruerat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "parueramus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "parueratis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "paruerant"

        assert word.get(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INFINITIVE) == "parere"

        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "pare"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "parete"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "parerem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "pareres"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "pareret"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "pareremus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "pareretis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "parerent"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "paruissem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "paruisses"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "paruisset"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "paruissemus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "paruissetis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "paruissent"

    def test_thirdconjugation(self):
        word = Verb("desero", "deserere", "deserui", "desertus", meaning="desert")

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "desero"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deseris"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deserit"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deserimus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deseritis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deserunt"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deserebam"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deserebas"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deserebat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deserebamus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deserebatis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deserebant"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deserui"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deseruisti"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deseruit"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deseruimus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deseruistis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deseruerunt"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deserueram"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deserueras"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deseruerat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deserueramus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deserueratis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "deseruerant"

        assert word.get(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INFINITIVE) == "deserere"

        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "desere"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "deserite"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "desererem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "desereres"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "desereret"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "desereremus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "desereretis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "desererent"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "deseruissem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "deseruisses"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "deseruisset"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "deseruissemus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "deseruissetis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "deseruissent"

    def test_thirdioconjugation(self):
        word = Verb("patefacio", "patefacere", "patefeci", "patefactus", meaning="reveal")

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefacio"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefacis"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefacit"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefacimus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefacitis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefaciunt"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefaciebam"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefaciebas"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefaciebat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefaciebamus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefaciebatis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefaciebant"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefeci"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefecisti"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefecit"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefecimus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefecistis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefecerunt"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefeceram"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefeceras"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefecerat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefeceramus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefeceratis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "patefecerant"

        assert word.get(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INFINITIVE) == "patefacere"

        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "pateface"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "patefacite"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "patefacerem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "patefaceres"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "patefaceret"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "patefaceremus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "patefaceretis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "patefacerent"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "patefecissem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "patefecisses"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "patefecisset"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "patefecissemus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "patefecissetis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "patefecissent"

    def test_fourthconjugation(self):
        word = Verb("aperio", "aperire", "aperui", "apertus", meaning="open")

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperio"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperis"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperit"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperimus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperitis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperiunt"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperiebam"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperiebas"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperiebat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperiebamus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperiebatis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperiebant"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperui"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperuisti"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperuit"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperuimus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperuistis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperuerunt"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperueram"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperueras"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperuerat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperueramus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperueratis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aperuerant"

        assert word.get(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INFINITIVE) == "aperire"

        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "aperi"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "aperite"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "aperirem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "aperires"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "aperiret"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "aperiremus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "aperiretis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "aperirent"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "aperuissem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "aperuisses"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "aperuisset"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "aperuissemus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "aperuissetis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "aperuissent"

    def test_irregularverb_eo(self):
        word = Verb("abeo", "abire", "abii", "abitum", meaning="depart")

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abeo"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abis"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abit"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abimus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abitis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abeunt"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abibam"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abibas"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abibat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abibamus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abibatis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abibant"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abii"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abisti"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abiit"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abiimus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abistis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abierunt"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abieram"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abieras"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abierat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abieramus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abieratis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "abierant"

        assert word.get(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INFINITIVE) == "abire"

        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "abi"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "abite"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "abirem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "abires"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "abiret"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "abiremus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "abiretis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "abirent"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "abissem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "abisses"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "abisset"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "abissemus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "abissetis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "abissent"


class TestParticipleConjugation:
    def test_present_participle(self):
        word = Verb("porto", "portare", "portavi", "portatus", meaning="carry")

        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.NOMINATIVE) == "portans"
        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.VOCATIVE) == "portans"
        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.ACCUSATIVE) == "portantem"
        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.GENITIVE) == "portantis"
        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.DATIVE) == "portanti"
        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.ABLATIVE) == "portante"

        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.NOMINATIVE) == "portantes"
        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.VOCATIVE) == "portantes"
        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.ACCUSATIVE) == "portantes"
        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.GENITIVE) == "portantium"
        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.DATIVE) == "portantibus"
        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.ABLATIVE) == "portantibus"

        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.NOMINATIVE) == "portans"
        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.VOCATIVE) == "portans"
        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.ACCUSATIVE) == "portantem"
        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.GENITIVE) == "portantis"
        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.DATIVE) == "portanti"
        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.ABLATIVE) == "portante"

        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.NOMINATIVE) == "portantes"
        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.VOCATIVE) == "portantes"
        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.ACCUSATIVE) == "portantes"
        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.GENITIVE) == "portantium"
        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.DATIVE) == "portantibus"
        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.ABLATIVE) == "portantibus"

        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.NOMINATIVE) == "portans"
        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.VOCATIVE) == "portans"
        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.ACCUSATIVE) == "portans"
        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.GENITIVE) == "portantis"
        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.DATIVE) == "portanti"
        assert word.get(number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.ABLATIVE) == "portante"

        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.NOMINATIVE) == "portantia"
        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.VOCATIVE) == "portantia"
        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.ACCUSATIVE) == "portantia"
        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.GENITIVE) == "portantium"
        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.DATIVE) == "portantibus"
        assert word.get(number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.ABLATIVE) == "portantibus"

    def test_ppp(self):
        word = Verb("porto", "portare", "portavi", "portatus", meaning="carry")

        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.NOMINATIVE) == "portatus"
        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.VOCATIVE) == "portate"
        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.ACCUSATIVE) == "portatum"
        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.GENITIVE) == "portati"
        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.DATIVE) == "portato"
        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.ABLATIVE) == "portato"

        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.NOMINATIVE) == "portati"
        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.VOCATIVE) == "portati"
        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.ACCUSATIVE) == "portatos"
        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.GENITIVE) == "portatorum"
        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.DATIVE) == "portatis"
        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.ABLATIVE) == "portatis"

        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.NOMINATIVE) == "portata"
        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.VOCATIVE) == "portata"
        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.ACCUSATIVE) == "portatam"
        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.GENITIVE) == "portatae"
        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.DATIVE) == "portatae"
        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.ABLATIVE) == "portata"

        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.NOMINATIVE) == "portatae"
        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.VOCATIVE) == "portatae"
        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.ACCUSATIVE) == "portatas"
        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.GENITIVE) == "portatarum"
        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.DATIVE) == "portatis"
        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.FEMININE, participle_case=Case.ABLATIVE) == "portatis"

        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.NOMINATIVE) == "portatum"
        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.VOCATIVE) == "portatum"
        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.ACCUSATIVE) == "portatum"
        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.GENITIVE) == "portati"
        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.DATIVE) == "portato"
        assert word.get(number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.ABLATIVE) == "portato"

        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.NOMINATIVE) == "portata"
        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.VOCATIVE) == "portata"
        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.ACCUSATIVE) == "portata"
        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.GENITIVE) == "portatorum"
        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.DATIVE) == "portatis"
        assert word.get(number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.NEUTER, participle_case=Case.ABLATIVE) == "portatis"


class TestIrregularVerbInflection:
    def test_irregular_verb_normal(self):
        word = Verb("sum", "esse", "fui", meaning="be")

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "sum"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "es"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "est"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "sumus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "estis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "sunt"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "eram"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "eras"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "erat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "eramus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "eratis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "erant"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "fui"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "fuisti"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "fuit"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "fuimus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "fuistis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "fuerunt"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "fueram"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "fueras"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "fuerat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "fueramus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "fueratis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "fuerant"

        assert word.get(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INFINITIVE) == "esse"

        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "es"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "este"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "essem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "esses"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "esset"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "essemus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "essetis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "essent"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "fuissem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "fuisses"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "fuisset"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "fuissemus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "fuissetis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "fuissent"

    def test_irregular_verb_derived(self):
        word = Verb("adeo", "adire", "adii", "aditus", meaning="go to")

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adeo"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adis"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adit"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adimus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "aditis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adeunt"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adibam"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adibas"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adibat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adibamus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adibatis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adibant"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adii"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adisti"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adiit"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adiimus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adistis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adierunt"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adieram"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adieras"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adierat"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adieramus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adieratis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE) == "adierant"

        assert word.get(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INFINITIVE) == "adire"

        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "adi"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE) == "adite"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "adirem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "adires"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "adiret"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "adiremus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "adiretis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "adirent"

        assert word.get(person=1, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "adissem"
        assert word.get(person=2, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "adisses"
        assert word.get(person=3, number=Number.SINGULAR, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "adisset"
        assert word.get(person=1, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "adissemus"
        assert word.get(person=2, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "adissetis"
        assert word.get(person=3, number=Number.PLURAL, tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.SUBJUNCTIVE) == "adissent"
