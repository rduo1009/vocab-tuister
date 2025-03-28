import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from src.core.accido.edge_cases import IRREGULAR_VERBS
from src.core.accido.endings import Verb
from src.core.accido.misc import Case, Gender, Mood, MultipleEndings, Number, Tense, Voice

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
    (Tense.FUTURE, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.PLURAL),
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
    (Tense.FUTURE_PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.PLURAL),
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
        "celabo", "celabis", "celabit", "celabimus", "celabitis", "celabunt",
        "celavi", "celavisti", "celavit", "celavimus", "celavistis", "celaverunt",
        "celaveram", "celaveras", "celaverat", "celaveramus", "celaveratis", "celaverant",
        "celavero", "celaveris", "celaverit", "celaverimus", "celaveritis", "celaverint",

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
        "parebo", "parebis", "parebit", "parebimus", "parebitis", "parebunt",
        "parui", "paruisti", "paruit", "paruimus", "paruistis", "paruerunt",
        "parueram", "parueras", "paruerat", "parueramus", "parueratis", "paruerant",
        "paruero", "parueris", "paruerit", "paruerimus", "parueritis", "paruerint",

        "parere",
        "pare", "parete",

        "parerem", "pareres", "pareret", "pareremus", "pareretis", "parerent",
        "paruissem", "paruisses", "paruisset", "paruissemus", "paruissetis", "paruissent",
    ])])  # fmt: skip
    def test_secondconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("pareo", "parere", "parui", "paritus", meaning="appear")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "desero", "deseris", "deserit", "deserimus", "deseritis", "deserunt",
        "deserebam", "deserebas", "deserebat", "deserebamus", "deserebatis", "deserebant",
        "deseram", "deseres", "deseret", "deseremus", "deseretis", "deserent",
        "deserui", "deseruisti", "deseruit", "deseruimus", "deseruistis", "deseruerunt",
        "deserueram", "deserueras", "deseruerat", "deserueramus", "deserueratis", "deseruerant",
        "deseruero", "deserueris", "deseruerit", "deseruerimus", "deserueritis", "deseruerint",

        "deserere",
        "desere", "deserite",

        "desererem", "desereres", "desereret", "desereremus", "desereretis", "desererent",
        "deseruissem", "deseruisses", "deseruisset", "deseruissemus", "deseruissetis", "deseruissent",
    ])])  # fmt: skip
    def test_thirdconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("desero", "deserere", "deserui", "desertus", meaning="desert")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "capio", "capis", "capit", "capimus", "capitis", "capiunt",
        "capiebam", "capiebas", "capiebat", "capiebamus", "capiebatis", "capiebant",
        "capiam", "capies", "capiet", "capiemus", "capietis", "capient",
        "cepi", "cepisti", "cepit", "cepimus", "cepistis", "ceperunt",
        "ceperam", "ceperas", "ceperat", "ceperamus", "ceperatis", "ceperant",
        "cepero", "ceperis", "ceperit", "ceperimus", "ceperitis", "ceperint",

        "capere",
        "cape", "capite",
            
        "caperem", "caperes", "caperet", "caperemus", "caperetis", "caperent",
        "cepissem", "cepisses", "cepisset", "cepissemus", "cepissetis", "cepissent",
    ])])  # fmt: skip
    def test_thirdioconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("capio", "capere", "cepi", "captus", meaning="take")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "aperio", "aperis", "aperit", "aperimus", "aperitis", "aperiunt",
        "aperiebam", "aperiebas", "aperiebat", "aperiebamus", "aperiebatis", "aperiebant",
        "aperiam", "aperies", "aperiet", "aperiemus", "aperietis", "aperient",
        "aperui", "aperuisti", "aperuit", "aperuimus", "aperuistis", "aperuerunt",
        "aperueram", "aperueras", "aperuerat", "aperueramus", "aperueratis", "aperuerant",
        "aperuero", "aperueris", "aperuerit", "aperuerimus", "aperueritis", "aperuerint",
            
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
        "abibo", "abibis", "abibit", "abibimus", "abibitis", "abibunt",
        "abii", "abisti", "abiit", "abiimus", "abistis", "abierunt",
        "abieram", "abieras", "abierat", "abieramus", "abieratis", "abierant",
        "abiero", "abieris", "abierit", "abierimus", "abieritis", "abierint",

        "abire",
        "abi", "abite",
            
        "abirem", "abires", "abiret", "abiremus", "abiretis", "abirent",
        "abissem", "abisses", "abisset", "abissemus", "abissetis", "abissent",
    ])])  # fmt: skip
    def test_irregularverb_eo(self, tense, voice, mood, person, number, expected):
        word = Verb("abeo", "abire", "abii", "abitum", meaning="depart")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("word"), IRREGULAR_VERBS.keys())
    def test_irregularverb(self, word):
        assert Verb(word, meaning="placeholder").endings == IRREGULAR_VERBS[word]


# TODO: Rework this to be more like pronouns
class TestIrregularVerbInflection:
    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "sum", "es", "est", "sumus", "estis", "sunt",
        "eram", "eras", "erat", "eramus", "eratis", "erant",
        "ero", "eris", "erit", "erimus", "eritis", "erunt",
        "fui", "fuisti", "fuit", "fuimus", "fuistis", "fuerunt",
        "fueram", "fueras", "fuerat", "fueramus", "fueratis", "fuerant",
        "fuero", "fueris", "fuerit", "fuerimus", "fueritis", "fuerint",

        "esse",
        "es", "este",

        "essem", "esses", "esset", "essemus", "essetis", "essent",
        "fuissem", "fuisses", "fuisset", "fuissemus", "fuissetis", "fuissent",
    ])])  # fmt: skip
    def test_irregular_verb_normal(self, tense, voice, mood, person, number, expected):
        word = Verb("sum", "esse", "fui", meaning="be")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    # NOTE: Already covered!
    # @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
    #     "adeo", "adis", "adit", "adimus", "aditis", "adeunt",
    #     "adibam", "adibas", "adibat", "adibamus", "adibatis", "adibant",
    #     "adii", "adisti", "adiit", "adiimus", "adistis", "adierunt",
    #     "adieram", "adieras", "adierat", "adieramus", "adieratis", "adierant",

    #     "adire",
    #     "adi", "adite",

    #     "adirem", "adires", "adiret", "adiremus", "adiretis", "adirent",
    #     "adissem", "adisses", "adisset", "adissemus", "adissetis", "adissent",
    # ])])
    # def test_irregular_verb_derived(self, tense, voice, mood, person, number, expected):
    #     word = Verb("adeo", "adire", "adii", "aditus", meaning="go to")
    #     assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected


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


class TestParticipleConjugation:
    @pytest.mark.parametrize(("tense", "voice", "mood", "participle_gender", "participle_case", "number", "expected"), [PARTICIPLE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "portans", "portans", "portantem", "portantis", "portanti", MultipleEndings(regular="portanti", absolute="portante"),
        "portantes", "portantes", "portantes", "portantium", "portantibus", "portantibus",
        "portans", "portans", "portantem", "portantis", "portanti", MultipleEndings(regular="portanti", absolute="portante"),
        "portantes", "portantes", "portantes", "portantium", "portantibus", "portantibus",
        "portans", "portans", "portans", "portantis", "portanti", MultipleEndings(regular="portanti", absolute="portante"),
        "portantia", "portantia", "portantia", "portantium", "portantibus", "portantibus",

        "portatus", "portate", "portatum", "portati", "portato", "portato",
        "portati", "portati", "portatos", "portatorum", "portatis", "portatis",
        "portata", "portata", "portatam", "portatae", "portatae", "portata",
        "portatae", "portatae", "portatas", "portatarum", "portatis", "portatis",
        "portatum", "portatum", "portatum", "portati", "portato", "portato",
        "portata", "portata", "portata", "portatorum", "portatis", "portatis",
    ])])  # fmt: skip
    def test_participle_firstconjugation(self, tense, voice, mood, participle_gender, participle_case, number, expected):
        word = Verb("porto", "portare", "portavi", "portatus", meaning="carry")
        assert word.get(tense=tense, voice=voice, mood=mood, participle_gender=participle_gender, participle_case=participle_case, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "participle_gender", "participle_case", "number", "expected"), [PARTICIPLE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "docens", "docens", "docentem", "docentis", "docenti", MultipleEndings(regular="docenti", absolute="docente"),
        "docentes", "docentes", "docentes", "docentium", "docentibus", "docentibus",
        "docens", "docens", "docentem", "docentis", "docenti", MultipleEndings(regular="docenti", absolute="docente"),
        "docentes", "docentes", "docentes", "docentium", "docentibus", "docentibus",
        "docens", "docens", "docens", "docentis", "docenti", MultipleEndings(regular="docenti", absolute="docente"),
        "docentia", "docentia", "docentia", "docentium", "docentibus", "docentibus",

        "doctus", "docte", "doctum", "docti", "docto", "docto",
        "docti", "docti", "doctos", "doctorum", "doctis", "doctis",
        "docta", "docta", "doctam", "doctae", "doctae", "docta",
        "doctae", "doctae", "doctas", "doctarum", "doctis", "doctis",
        "doctum", "doctum", "doctum", "docti", "docto", "docto",
        "docta", "docta", "docta", "doctorum", "doctis", "doctis",
    ])])  # fmt: skip
    def test_participle_secondconjugation(self, tense, voice, mood, participle_gender, participle_case, number, expected):
        word = Verb("doceo", "docere", "docui", "doctus", meaning="teach")
        assert word.get(tense=tense, voice=voice, mood=mood, participle_gender=participle_gender, participle_case=participle_case, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "participle_gender", "participle_case", "number", "expected"), [PARTICIPLE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "trahens", "trahens", "trahentem", "trahentis", "trahenti", MultipleEndings(regular="trahenti", absolute="trahente"),
        "trahentes", "trahentes", "trahentes", "trahentium", "trahentibus", "trahentibus",
        "trahens", "trahens", "trahentem", "trahentis", "trahenti", MultipleEndings(regular="trahenti", absolute="trahente"),
        "trahentes", "trahentes", "trahentes", "trahentium", "trahentibus", "trahentibus",
        "trahens", "trahens", "trahens", "trahentis", "trahenti", MultipleEndings(regular="trahenti", absolute="trahente"),
        "trahentia", "trahentia", "trahentia", "trahentium", "trahentibus", "trahentibus",

        "tractus", "tracte", "tractum", "tracti", "tracto", "tracto",
        "tracti", "tracti", "tractos", "tractorum", "tractis", "tractis",
        "tracta", "tracta", "tractam", "tractae", "tractae", "tracta",
        "tractae", "tractae", "tractas", "tractarum", "tractis", "tractis",
        "tractum", "tractum", "tractum", "tracti", "tracto", "tracto",
        "tracta", "tracta", "tracta", "tractorum", "tractis", "tractis",
    ])])  # fmt: skip
    def test_participle_thirdconjugation(self, tense, voice, mood, participle_gender, participle_case, number, expected):
        word = Verb("traho", "trahere", "traxi", "tractus", meaning="begin")
        assert word.get(tense=tense, voice=voice, mood=mood, participle_gender=participle_gender, participle_case=participle_case, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "participle_gender", "participle_case", "number", "expected"), [PARTICIPLE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "occipiens", "occipiens", "occipientem", "occipientis", "occipienti", MultipleEndings(regular="occipienti", absolute="occipiente"),
        "occipientes", "occipientes", "occipientes", "occipientium", "occipientibus", "occipientibus",
        "occipiens", "occipiens", "occipientem", "occipientis", "occipienti", MultipleEndings(regular="occipienti", absolute="occipiente"),
        "occipientes", "occipientes", "occipientes", "occipientium", "occipientibus", "occipientibus",
        "occipiens", "occipiens", "occipiens", "occipientis", "occipienti", MultipleEndings(regular="occipienti", absolute="occipiente"),
        "occipientia", "occipientia", "occipientia", "occipientium", "occipientibus", "occipientibus",

        "occeptus", "occepte", "occeptum", "occepti", "occepto", "occepto",
        "occepti", "occepti", "occeptos", "occeptorum", "occeptis", "occeptis",
        "occepta", "occepta", "occeptam", "occeptae", "occeptae", "occepta",
        "occeptae", "occeptae", "occeptas", "occeptarum", "occeptis", "occeptis",
        "occeptum", "occeptum", "occeptum", "occepti", "occepto", "occepto",
        "occepta", "occepta", "occepta", "occeptorum", "occeptis", "occeptis",
    ])])  # fmt: skip
    def test_participle_mixedconjugation(self, tense, voice, mood, participle_gender, participle_case, number, expected):
        word = Verb("occipio", "occipere", "occepi", "occeptus", meaning="begin")
        assert word.get(tense=tense, voice=voice, mood=mood, participle_gender=participle_gender, participle_case=participle_case, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "participle_gender", "participle_case", "number", "expected"), [PARTICIPLE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "audiens", "audiens", "audientem", "audientis", "audienti", MultipleEndings(regular="audienti", absolute="audiente"),
        "audientes", "audientes", "audientes", "audientium", "audientibus", "audientibus",
        "audiens", "audiens", "audientem", "audientis", "audienti", MultipleEndings(regular="audienti", absolute="audiente"),
        "audientes", "audientes", "audientes", "audientium", "audientibus", "audientibus",
        "audiens", "audiens", "audiens", "audientis", "audienti", MultipleEndings(regular="audienti", absolute="audiente"),
        "audientia", "audientia", "audientia", "audientium", "audientibus", "audientibus",

        "auditus", "audite", "auditum", "auditi", "audito", "audito",
        "auditi", "auditi", "auditos", "auditorum", "auditis", "auditis",
        "audita", "audita", "auditam", "auditae", "auditae", "audita",
        "auditae", "auditae", "auditas", "auditarum", "auditis", "auditis",
        "auditum", "auditum", "auditum", "auditi", "audito", "audito",
        "audita", "audita", "audita", "auditorum", "auditis", "auditis",
    ])])  # fmt: skip
    def test_participle_fourthconjugation(self, tense, voice, mood, participle_gender, participle_case, number, expected):
        word = Verb("audio", "audire", "audivi", "auditus", meaning="hear")
        assert word.get(tense=tense, voice=voice, mood=mood, participle_gender=participle_gender, participle_case=participle_case, number=number) == expected
