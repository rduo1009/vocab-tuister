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
    (Tense.PRESENT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PRESENT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PRESENT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PRESENT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PRESENT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PRESENT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.IMPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.IMPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.IMPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.FUTURE, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.FUTURE, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.FUTURE, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.FUTURE, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.FUTURE, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.FUTURE, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.PLURAL),
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
    (Tense.PRESENT, Voice.ACTIVE, Mood.IMPERATIVE, 2, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.IMPERATIVE, 2, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.INFINITIVE, None, None),
    (Tense.PRESENT, Voice.PASSIVE, Mood.INFINITIVE, None, None),
)


class TestVerbConjugation:
    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "celo", "celas", "celat", "celamus", "celatis", "celant",
        "celabam", "celabas", "celabat", "celabamus", "celabatis", "celabant",
        "celabo", "celabis", "celabit", "celabimus", "celabitis", "celabunt",
        "celavi", "celavisti", "celavit", "celavimus", "celavistis", "celaverunt",
        "celaveram", "celaveras", "celaverat", "celaveramus", "celaveratis", "celaverant",
        "celavero", "celaveris", "celaverit", "celaverimus", "celaveritis", "celaverint",

        "celor", "celaris", "celatur", "celamur", "celamini", "celantur",
        "celabar", "celabaris", "celabatur", "celabamur", "celabamini", "celabantur",
        "celabor", "celaberis", "celabitur", "celabimur", "celabimini", "celabuntur",
        "celatus sum", "celatus es", "celatus est", "celati sumus", "celati estis", "celati sunt",
        "celatus eram", "celatus eras", "celatus erat", "celati eramus", "celati eratis", "celati erant",
        "celatus ero", "celatus eris", "celatus erit", "celati erimus", "celati eritis", "celati erunt",

        "celarem", "celares", "celaret", "celaremus", "celaretis", "celarent",
        "celavissem", "celavisses", "celavisset", "celavissemus", "celavissetis", "celavissent",

        "cela", "celate",

        "celare", "celari",
    ])])  # fmt: skip
    def test_firstconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "maneo", "manes", "manet", "manemus", "manetis", "manent",
        "manebam", "manebas", "manebat", "manebamus", "manebatis", "manebant",
        "manebo", "manebis", "manebit", "manebimus", "manebitis", "manebunt",
        "mansi", "mansisti", "mansit", "mansimus", "mansistis", "manserunt",
        "manseram", "manseras", "manserat", "manseramus", "manseratis", "manserant",
        "mansero", "manseris", "manserit", "manserimus", "manseritis", "manserint",

        "maneor", "maneris", "manetur", "manemur", "manemini", "manentur",
        "manebar", "manebaris", "manebatur", "manebamur", "manebamini", "manebantur",
        "manebor", "maneberis", "manebitur", "manebimur", "manebimini", "manebuntur",
        "mansus sum", "mansus es", "mansus est", "mansi sumus", "mansi estis", "mansi sunt",
        "mansus eram", "mansus eras", "mansus erat", "mansi eramus", "mansi eratis", "mansi erant",
        "mansus ero", "mansus eris", "mansus erit", "mansi erimus", "mansi eritis", "mansi erunt",

        "manerem", "maneres", "maneret", "maneremus", "maneretis", "manerent",
        "mansissem", "mansisses", "mansisset", "mansissemus", "mansissetis", "mansissent",

        "mane", "manete",

        "manere", "maneri",
    ])])  # fmt: skip
    def test_secondconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("maneo", "manere", "mansi", "mansus", meaning="stay")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "desero", "deseris", "deserit", "deserimus", "deseritis", "deserunt",
        "deserebam", "deserebas", "deserebat", "deserebamus", "deserebatis", "deserebant",
        "deseram", "deseres", "deseret", "deseremus", "deseretis", "deserent",
        "deserui", "deseruisti", "deseruit", "deseruimus", "deseruistis", "deseruerunt",
        "deserueram", "deserueras", "deseruerat", "deserueramus", "deserueratis", "deseruerant",
        "deseruero", "deserueris", "deseruerit", "deseruerimus", "deserueritis", "deseruerint",

        "deseror", "desereris", "deseritur", "deserimur", "deserimini", "deseruntur",
        "deserebar", "deserebaris", "deserebatur", "deserebamur", "deserebamini", "deserebantur",
        "deserar", "desereris", "deseretur", "deseremur", "deseremini", "deserentur",
        "desertus sum", "desertus es", "desertus est", "deserti sumus", "deserti estis", "deserti sunt",
        "desertus eram", "desertus eras", "desertus erat", "deserti eramus", "deserti eratis", "deserti erant",
        "desertus ero", "desertus eris", "desertus erit", "deserti erimus", "deserti eritis", "deserti erunt",

        "desererem", "desereres", "desereret", "desereremus", "desereretis", "desererent",
        "deseruissem", "deseruisses", "deseruisset", "deseruissemus", "deseruissetis", "deseruissent",

        "desere", "deserite",

        "deserere", "deseri",
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

        "capior", "caperis", "capitur", "capimur", "capimini", "capiuntur",
        "capiebar", "capiebaris", "capiebatur", "capiebamur", "capiebamini", "capiebantur",
        "capiar", "capieris", "capietur", "capiemur", "capiemini", "capientur",
        "captus sum", "captus es", "captus est", "capti sumus", "capti estis", "capti sunt",
        "captus eram", "captus eras", "captus erat", "capti eramus", "capti eratis", "capti erant",
        "captus ero", "captus eris", "captus erit", "capti erimus", "capti eritis", "capti erunt",

        "caperem", "caperes", "caperet", "caperemus", "caperetis", "caperent",
        "cepissem", "cepisses", "cepisset", "cepissemus", "cepissetis", "cepissent",

        "cape", "capite",

        "capere", "capi",
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

        "aperior", "aperiris", "aperitur", "aperimur", "aperimini", "aperiuntur",
        "aperiebar", "aperiebaris", "aperiebatur", "aperiebamur", "aperiebamini", "aperiebantur",
        "aperiar", "aperieris", "aperietur", "aperiemur", "aperiemini", "aperientur",
        "apertus sum", "apertus es", "apertus est", "aperti sumus", "aperti estis", "aperti sunt",
        "apertus eram", "apertus eras", "apertus erat", "aperti eramus", "aperti eratis", "aperti erant",
        "apertus ero", "apertus eris", "apertus erit", "aperti erimus", "aperti eritis", "aperti erunt",
            
        "aperirem", "aperires", "aperiret", "aperiremus", "aperiretis", "aperirent",
        "aperuissem", "aperuisses", "aperuisset", "aperuissemus", "aperuissetis", "aperuissent",

        "aperi", "aperite",

        "aperire", "aperiri",
    ])])  # fmt: skip
    def test_fourthconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("aperio", "aperire", "aperui", "apertus", meaning="open")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "veneo", "venis", "venit", "venimus", "venitis", "veneunt",
        "venibam", "venibas", "venibat", "venibamus", "venibatis", "venibant",
        "venibo", "venibis", "venibit", "venibimus", "venibitis", "venibunt",
        "venii", "venisti", "veniit", "veniimus", "venistis", "venierunt",
        "venieram", "venieras", "venierat", "venieramus", "venieratis", "venierant",
        "veniero", "venieris", "venierit", "venierimus", "venieritis", "venierint",

        "veneor", "veniris", "venitur", "venimur", "venimini", "veneuntur",
        "venibar", "venibaris", "venibatur", "venibamur", "venibamini", "venibantur",
        "venibor", "veniberis", "venibitur", "venibimur", "venibimini", "venibuntur",
        "venitus sum", "venitus es", "venitus est", "veniti sumus", "veniti estis", "veniti sunt",
        "venitus eram", "venitus eras", "venitus erat", "veniti eramus", "veniti eratis", "veniti erant",
        "venitus ero", "venitus eris", "venitus erit", "veniti erimus", "veniti eritis", "veniti erunt",

        "venirem", "venires", "veniret", "veniremus", "veniretis", "venirent",
        "venissem", "venisses", "venisset", "venissemus", "venissetis", "venissent",

        "veni", "venite",

        "venire", "veniri",
    ])])  # fmt: skip
    def test_irregularverb_eo(self, tense, voice, mood, person, number, expected):
        word = Verb("veneo", "venire", "venii", "venitus", meaning="be sold")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("word"), IRREGULAR_VERBS.keys())
    def test_irregularverb(self, word):
        assert Verb(word, meaning="placeholder").endings == IRREGULAR_VERBS[word]


# TODO: Rework this to be more like pronouns
class TestIrregularVerbConjugation:
    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "sum", "es", "est", "sumus", "estis", "sunt",
        "eram", "eras", "erat", "eramus", "eratis", "erant",
        "ero", "eris", "erit", "erimus", "eritis", "erunt",
        "fui", "fuisti", "fuit", "fuimus", "fuistis", "fuerunt",
        "fueram", "fueras", "fuerat", "fueramus", "fueratis", "fuerant",
        "fuero", "fueris", "fuerit", "fuerimus", "fueritis", "fuerint",

        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,

        "essem", "esses", "esset", "essemus", "essetis", "essent",
        "fuissem", "fuisses", "fuisset", "fuissemus", "fuissetis", "fuissent",

        "es", "este",

        "esse", None,
    ])])  # fmt: skip
    def test_irregular_verb_normal(self, tense, voice, mood, person, number, expected):
        word = Verb("sum", "esse", "fui", meaning="be")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "elego", "elegas", "elegat", "elegamus", "elegatis", "elegant",
        "elegabam", "elegabas", "elegabat", "elegabamus", "elegabatis", "elegabant",
        "elegabo", "elegabis", "elegabit", "elegabimus", "elegabitis", "elegabunt",
        "elegavi", "elegavisti", "elegavit", "elegavimus", "elegavistis", "elegaverunt",
        "elegaveram", "elegaveras", "elegaverat", "elegaveramus", "elegaveratis", "elegaverant",
        "elegavero", "elegaveris", "elegaverit", "elegaverimus", "elegaveritis", "elegaverint",

        "elegor", "elegaris", "elegatur", "elegamur", "elegamini", "elegantur",
        "elegabar", "elegabaris", "elegabatur", "elegabamur", "elegabamini", "elegabantur",
        "elegabor", "elegaberis", "elegabitur", "elegabimur", "elegabimini", "elegabuntur",
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,

        "elegarem", "elegares", "elegaret", "elegaremus", "elegaretis", "elegarent",
        "elegavissem", "elegavisses", "elegavisset", "elegavissemus", "elegavissetis", "elegavissent",

        "elega", "elegate",

        "elegare", "elegari",
    ])])  # fmt: skip
    def test_irregular_verb_no_ppp(self, tense, voice, mood, person, number, expected):
        word = Verb("elego", "elegare", "elegavi", meaning="bequeath away")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected


DEPONENT_COMBINATIONS = (
    (Tense.PRESENT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PRESENT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PRESENT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PRESENT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PRESENT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PRESENT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.IMPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.IMPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.IMPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.FUTURE, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.FUTURE, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.FUTURE, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.FUTURE, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.FUTURE, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.FUTURE, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PRESENT, Voice.DEPONENT, Mood.INFINITIVE, None, None),
)


class TestDeponentConjugation:
    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [DEPONENT_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "conor", "conaris", "conatur", "conamur", "conamini", "conantur",
        "conabar", "conabaris", "conabatur", "conabamur", "conabamini", "conabantur",
        "conabor", "conaberis", "conabitur", "conabimur", "conabimini", "conabuntur",
        "conatus sum", "conatus es", "conatus est", "conati sumus", "conati estis", "conati sunt",
        "conatus eram", "conatus eras", "conatus erat", "conati eramus", "conati eratis", "conati erant",
        "conatus ero", "conatus eris", "conatus erit", "conati erimus", "conati eritis", "conati erunt",
        "conari",
    ])])  # fmt: skip
    def test_firstconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("conor", "conari", "conatus sum", meaning="try")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [DEPONENT_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "vereor", "vereris", "veretur", "veremur", "veremini", "verentur",
        "verebar", "verebaris", "verebatur", "verebamur", "verebamini", "verebantur",
        "verebor", "vereberis", "verebitur", "verebimur", "verebimini", "verebuntur",
        "veritus sum", "veritus es", "veritus est", "veriti sumus", "veriti estis", "veriti sunt",
        "veritus eram", "veritus eras", "veritus erat", "veriti eramus", "veriti eratis", "veriti erant",
        "veritus ero", "veritus eris", "veritus erit", "veriti erimus", "veriti eritis", "veriti erunt",
        "vereri",
    ])])  # fmt: skip
    def test_secondconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("vereor", "vereri", "veritus sum", meaning="fear")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [DEPONENT_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "sequor", "sequeris", "sequitur", "sequimur", "sequimini", "sequuntur",
        "sequebar", "sequebaris", "sequebatur", "sequebamur", "sequebamini", "sequebantur",
        "sequar", "sequeris", "sequetur", "sequemur", "sequemini", "sequentur",
        "secutus sum", "secutus es", "secutus est", "secuti sumus", "secuti estis", "secuti sunt",
        "secutus eram", "secutus eras", "secutus erat", "secuti eramus", "secuti eratis", "secuti erant",
        "secutus ero", "secutus eris", "secutus erit", "secuti erimus", "secuti eritis", "secuti erunt",
        "sequi",
    ])])  # fmt: skip
    def test_thirdconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("sequor", "sequi", "secutus sum", meaning="follow")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [DEPONENT_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "ingredior", "ingrederis", "ingreditur", "ingredimur", "ingredimini", "ingrediuntur",
        "ingrediebar", "ingrediebaris", "ingrediebatur", "ingrediebamur", "ingrediebamini", "ingrediebantur",
        "ingrediar", "ingredieris", "ingredietur", "ingrediemur", "ingrediemini", "ingredientur",
        "ingressus sum", "ingressus es", "ingressus est", "ingressi sumus", "ingressi estis", "ingressi sunt",
        "ingressus eram", "ingressus eras", "ingressus erat", "ingressi eramus", "ingressi eratis", "ingressi erant",
        "ingressus ero", "ingressus eris", "ingressus erit", "ingressi erimus", "ingressi eritis", "ingressi erunt",
        "ingredi",
    ])])  # fmt: skip
    def test_thirdioconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("ingredior", "ingredi", "ingressus sum", meaning="enter")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [DEPONENT_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "orior", "oriris", "oritur", "orimur", "orimini", "oriuntur",
        "oriebar", "oriebaris", "oriebatur", "oriebamur", "oriebamini", "oriebantur",
        "oriar", "orieris", "orietur", "oriemur", "oriemini", "orientur",
        "orsus sum", "orsus es", "orsus est", "orsi sumus", "orsi estis", "orsi sunt",
        "orsus eram", "orsus eras", "orsus erat", "orsi eramus", "orsi eratis", "orsi erant",
        "orsus ero", "orsus eris", "orsus erit", "orsi erimus", "orsi eritis", "orsi erunt",
        "oriri",
    ])])  # fmt: skip
    def test_fourthconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("orior", "oriri", "orsus sum", meaning="rise")
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
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.VOCATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.GENITIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.DATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ABLATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.NOMINATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.VOCATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.GENITIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.DATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ABLATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.VOCATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.GENITIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.DATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ABLATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.NOMINATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.VOCATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.GENITIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.DATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ABLATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.VOCATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.GENITIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.DATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ABLATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.NOMINATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.VOCATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.GENITIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.DATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ABLATIVE, Number.PLURAL),
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

        "portaturus", "portature", "portaturum", "portaturi", "portaturo", "portaturo",
        "portaturi", "portaturi", "portaturos", "portaturorum", "portaturis", "portaturis",
        "portatura", "portatura", "portaturam", "portaturae", "portaturae", "portatura",
        "portaturae", "portaturae", "portaturas", "portaturarum", "portaturis", "portaturis",
        "portaturum", "portaturum", "portaturum", "portaturi", "portaturo", "portaturo",
        "portatura", "portatura", "portatura", "portaturorum", "portaturis", "portaturis",
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

        "docturus", "docture", "docturum", "docturi", "docturo", "docturo",
        "docturi", "docturi", "docturos", "docturorum", "docturis", "docturis",
        "doctura", "doctura", "docturam", "docturae", "docturae", "doctura",
        "docturae", "docturae", "docturas", "docturarum", "docturis", "docturis",
        "docturum", "docturum", "docturum", "docturi", "docturo", "docturo",
        "doctura", "doctura", "doctura", "docturorum", "docturis", "docturis",
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

        "tracturus", "tracture", "tracturum", "tracturi", "tracturo", "tracturo",
        "tracturi", "tracturi", "tracturos", "tracturorum", "tracturis", "tracturis",
        "tractura", "tractura", "tracturam", "tracturae", "tracturae", "tractura",
        "tracturae", "tracturae", "tracturas", "tracturarum", "tracturis", "tracturis",
        "tracturum", "tracturum", "tracturum", "tracturi", "tracturo", "tracturo",
        "tractura", "tractura", "tractura", "tracturorum", "tracturis", "tracturis",
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

        "occepturus", "occepture", "occepturum", "occepturi", "occepturo", "occepturo",
        "occepturi", "occepturi", "occepturos", "occepturorum", "occepturis", "occepturis",
        "occeptura", "occeptura", "occepturam", "occepturae", "occepturae", "occeptura",
        "occepturae", "occepturae", "occepturas", "occepturarum", "occepturis", "occepturis",
        "occepturum", "occepturum", "occepturum", "occepturi", "occepturo", "occepturo",
        "occeptura", "occeptura", "occeptura", "occepturorum", "occepturis", "occepturis",
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

        "auditurus", "auditure", "auditurum", "audituri", "audituro", "audituro",
        "audituri", "audituri", "audituros", "auditurorum", "audituris", "audituris",
        "auditura", "auditura", "audituram", "auditurae", "auditurae", "auditura",
        "auditurae", "auditurae", "audituras", "auditurarum", "audituris", "audituris",
        "auditurum", "auditurum", "auditurum", "audituri", "audituro", "audituro",
        "auditura", "auditura", "auditura", "auditurorum", "audituris", "audituris",
    ])])  # fmt: skip
    def test_participle_fourthconjugation(self, tense, voice, mood, participle_gender, participle_case, number, expected):
        word = Verb("audio", "audire", "audivi", "auditus", meaning="hear")
        assert word.get(tense=tense, voice=voice, mood=mood, participle_gender=participle_gender, participle_case=participle_case, number=number) == expected


class TestIrregularParticipleConjugation:
    @pytest.mark.parametrize(("tense", "voice", "mood", "participle_gender", "participle_case", "number", "expected"), [PARTICIPLE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "elegans", "elegans", "elegantem", "elegantis", "eleganti", MultipleEndings(regular="eleganti", absolute="elegante"),
        "elegantes", "elegantes", "elegantes", "elegantium", "elegantibus", "elegantibus",
        "elegans", "elegans", "elegantem", "elegantis", "eleganti", MultipleEndings(regular="eleganti", absolute="elegante"),
        "elegantes", "elegantes", "elegantes", "elegantium", "elegantibus", "elegantibus",
        "elegans", "elegans", "elegans", "elegantis", "eleganti", MultipleEndings(regular="eleganti", absolute="elegante"),
        "elegantia", "elegantia", "elegantia", "elegantium", "elegantibus", "elegantibus",

        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,

        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
    ])])  # fmt: skip
    def test_irregular_participle_no_ppp(self, tense, voice, mood, participle_gender, participle_case, number, expected):
        word = Verb("elego", "elegare", "elegavi", meaning="bequeath away")
        assert word.get(tense=tense, voice=voice, mood=mood, participle_gender=participle_gender, participle_case=participle_case, number=number) == expected
