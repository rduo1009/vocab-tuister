# pyright: reportTypedDictNotRequiredAccess=false

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import contextlib
from itertools import combinations
from typing import TYPE_CHECKING

from src.core.accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb
from src.core.accido.misc import Case, Degree, Gender, Mood, Number, Tense, Voice
from src.core.lego.misc import VocabList
from src.core.rogo.asker import ask_question_without_sr
from src.core.rogo.question_classes import ParseWordCompToLatQuestion

if TYPE_CHECKING:
    from src.core.rogo.type_aliases import Settings

default_settings: Settings = {
    "exclude-verb-present-active-indicative": False,
    "exclude-verb-imperfect-active-indicative": False,
    "exclude-verb-future-active-indicative": False,
    "exclude-verb-perfect-active-indicative": False,
    "exclude-verb-pluperfect-active-indicative": False,
    "exclude-verb-future-perfect-active-indicative": False,
    "exclude-verb-present-active-infinitive": False,
    "exclude-verb-future-active-infinitive": False,
    "exclude-verb-perfect-active-infinitive": False,
    "exclude-verb-present-passive-infinitive": False,
    "exclude-verb-future-passive-infinitive": False,
    "exclude-verb-perfect-passive-infinitive": False,
    "exclude-verb-present-active-imperative": False,
    "exclude-verb-future-active-imperative": False,
    "exclude-verb-present-passive-imperative": False,
    "exclude-verb-future-passive-imperative": False,
    "exclude-verb-present-active-subjunctive": False,
    "exclude-verb-imperfect-active-subjunctive": False,
    "exclude-verb-perfect-active-subjunctive": False,
    "exclude-verb-pluperfect-active-subjunctive": False,
    "exclude-verb-present-passive-indicative": False,
    "exclude-verb-imperfect-passive-indicative": False,
    "exclude-verb-future-passive-indicative": False,
    "exclude-verb-perfect-passive-indicative": False,
    "exclude-verb-pluperfect-passive-indicative": False,
    "exclude-verb-future-perfect-passive-indicative": False,
    "exclude-verb-singular": False,
    "exclude-verb-plural": False,
    "exclude-verb-1st-person": False,
    "exclude-verb-2nd-person": False,
    "exclude-verb-3rd-person": False,
    "exclude-participles": False,
    "exclude-participle-present-active": False,
    "exclude-participle-perfect-passive": False,
    "exclude-participle-future-active": False,
    "exclude-gerundives": False,
    "exclude-participle-masculine": False,
    "exclude-participle-feminine": False,
    "exclude-participle-neuter": False,
    "exclude-participle-nominative": False,
    "exclude-participle-vocative": False,
    "exclude-participle-accusative": False,
    "exclude-participle-genitive": False,
    "exclude-participle-dative": False,
    "exclude-participle-ablative": False,
    "exclude-participle-singular": False,
    "exclude-participle-plural": False,
    "exclude-gerunds": False,
    "exclude-supines": False,
    "exclude-noun-nominative": False,
    "exclude-noun-vocative": False,
    "exclude-noun-accusative": False,
    "exclude-noun-genitive": False,
    "exclude-noun-dative": False,
    "exclude-noun-ablative": False,
    "exclude-noun-singular": False,
    "exclude-noun-plural": False,
    "exclude-adjective-masculine": False,
    "exclude-adjective-feminine": False,
    "exclude-adjective-neuter": False,
    "exclude-adjective-nominative": False,
    "exclude-adjective-vocative": False,
    "exclude-adjective-accusative": False,
    "exclude-adjective-genitive": False,
    "exclude-adjective-dative": False,
    "exclude-adjective-ablative": False,
    "exclude-adjective-singular": False,
    "exclude-adjective-plural": False,
    "exclude-adjective-positive": False,
    "exclude-adjective-comparative": False,
    "exclude-adjective-superlative": False,
    "exclude-adverbs": False,
    "exclude-adverb-positive": False,
    "exclude-adverb-comparative": False,
    "exclude-adverb-superlative": False,
    "exclude-pronoun-masculine": False,
    "exclude-pronoun-feminine": False,
    "exclude-pronoun-neuter": False,
    "exclude-pronoun-nominative": False,
    "exclude-pronoun-vocative": False,
    "exclude-pronoun-accusative": False,
    "exclude-pronoun-genitive": False,
    "exclude-pronoun-dative": False,
    "exclude-pronoun-ablative": False,
    "exclude-pronoun-singular": False,
    "exclude-pronoun-plural": False,
    "exclude-nouns": False,
    "exclude-verbs": False,
    "exclude-deponents": False,
    "exclude-adjectives": False,
    "exclude-pronouns": False,
    "exclude-regulars": False,
    "exclude-verb-first-conjugation": False,
    "exclude-verb-second-conjugation": False,
    "exclude-verb-third-conjugation": False,
    "exclude-verb-fourth-conjugation": False,
    "exclude-verb-mixed-conjugation": False,
    "exclude-verb-irregular-conjugation": False,
    "exclude-noun-first-declension": False,
    "exclude-noun-second-declension": False,
    "exclude-noun-third-declension": False,
    "exclude-noun-fourth-declension": False,
    "exclude-noun-fifth-declension": False,
    "exclude-noun-irregular-declension": False,
    "exclude-adjective-212-declension": False,
    "exclude-adjective-third-declension": False,
    "english-subjunctives": True,
    "english-verbal-nouns": True,
    "include-typein-engtolat": False,
    "include-typein-lattoeng": False,
    "include-parse": False,
    "include-inflect": True,
    "include-principal-parts": False,
    "include-multiplechoice-engtolat": False,
    "include-multiplechoice-lattoeng": False,
    "number-multiplechoice-options": 3,
}

# NOTE: These are incomplete but should be enough to test the functionality.
exclude_components_adjective = {
    "exclude-adjective-masculine": lambda components: components.gender == Gender.MASCULINE,
    "exclude-adjective-feminine": lambda components: components.gender == Gender.FEMININE,
    "exclude-adjective-neuter": lambda components: components.gender == Gender.NEUTER,
    "exclude-adjective-nominative": lambda components: components.case == Case.NOMINATIVE,
    "exclude-adjective-vocative": lambda components: components.case == Case.VOCATIVE,
    "exclude-adjective-accusative": lambda components: components.case == Case.ACCUSATIVE,
    "exclude-adjective-genitive": lambda components: components.case == Case.GENITIVE,
    "exclude-adjective-dative": lambda components: components.case == Case.DATIVE,
    "exclude-adjective-ablative": lambda components: components.case == Case.ABLATIVE,
    "exclude-adjective-singular": lambda components: components.number == Number.SINGULAR,
    "exclude-adjective-plural": lambda components: components.number == Number.PLURAL,
    "exclude-adjective-positive": lambda components: components.degree == Degree.POSITIVE,
    "exclude-adjective-comparative": lambda components: components.degree == Degree.COMPARATIVE,
    "exclude-adjective-superlative": lambda components: components.degree == Degree.SUPERLATIVE,
}

exclude_components_noun = {
    "exclude-noun-nominative": lambda components: components.case == Case.NOMINATIVE,
    "exclude-noun-vocative": lambda components: components.case == Case.VOCATIVE,
    "exclude-noun-accusative": lambda components: components.case == Case.ACCUSATIVE,
    "exclude-noun-genitive": lambda components: components.case == Case.GENITIVE,
    "exclude-noun-dative": lambda components: components.case == Case.DATIVE,
    "exclude-noun-ablative": lambda components: components.case == Case.ABLATIVE,
    "exclude-noun-singular": lambda components: components.number == Number.SINGULAR,
    "exclude-noun-plural": lambda components: components.number == Number.PLURAL,
}

exclude_components_pronoun = {
    "exclude-pronoun-masculine": lambda components: components.gender == Gender.MASCULINE,
    "exclude-pronoun-feminine": lambda components: components.gender == Gender.FEMININE,
    "exclude-pronoun-neuter": lambda components: components.gender == Gender.NEUTER,
    "exclude-pronoun-nominative": lambda components: components.case == Case.NOMINATIVE,
    "exclude-pronoun-vocative": lambda components: components.case == Case.VOCATIVE,
    "exclude-pronoun-accusative": lambda components: components.case == Case.ACCUSATIVE,
    "exclude-pronoun-genitive": lambda components: components.case == Case.GENITIVE,
    "exclude-pronoun-dative": lambda components: components.case == Case.DATIVE,
    "exclude-pronoun-ablative": lambda components: components.case == Case.ABLATIVE,
    "exclude-pronoun-singular": lambda components: components.number == Number.SINGULAR,
    "exclude-pronoun-plural": lambda components: components.number == Number.PLURAL,
}

exclude_components_verb = {
    "exclude-verb-present-active-indicative": lambda components: components.tense == Tense.PRESENT and components.voice == Voice.ACTIVE and components.mood == Mood.INDICATIVE,
    "exclude-verb-imperfect-active-indicative": lambda components: components.tense == Tense.IMPERFECT and components.voice == Voice.ACTIVE and components.mood == Mood.INDICATIVE,
    "exclude-verb-perfect-active-indicative": lambda components: components.tense == Tense.PERFECT and components.voice == Voice.ACTIVE and components.mood == Mood.INDICATIVE,
    "exclude-verb-pluperfect-active-indicative": lambda components: components.tense == Tense.PLUPERFECT and components.voice == Voice.ACTIVE and components.mood == Mood.INDICATIVE,
    "exclude-verb-imperfect-active-subjunctive": lambda components: components.tense == Tense.IMPERFECT and components.voice == Voice.ACTIVE and components.mood == Mood.SUBJUNCTIVE,
    "exclude-verb-pluperfect-active-subjunctive": lambda components: components.tense == Tense.PLUPERFECT and components.voice == Voice.ACTIVE and components.mood == Mood.SUBJUNCTIVE,
    "exclude-verb-present-active-imperative": lambda components: components.tense == Tense.PRESENT and components.voice == Voice.ACTIVE and components.mood == Mood.IMPERATIVE,
    "exclude-verb-present-active-infinitive": lambda components: components.tense == Tense.PRESENT and components.voice == Voice.ACTIVE and components.mood == Mood.INFINITIVE,
    "exclude-verb-singular": lambda components: components.number == Number.SINGULAR,
    "exclude-verb-plural": lambda components: components.number == Number.PLURAL,
    "exclude-verb-1st-person": lambda components: components.person == 1,
    "exclude-verb-2nd-person": lambda components: components.person == 2,
    "exclude-verb-3rd-person": lambda components: components.person == 3,
}


def test_ending_exclusion_adjective():
    word = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")
    vocab_list = VocabList([word], "")
    amount = 50

    keys = tuple(exclude_components_adjective.keys())
    all_key_combinations = [combo for r in range(2, 5) for combo in combinations(keys, r)]
    for key_combination in all_key_combinations:
        settings = default_settings.copy()

        for key in key_combination:
            settings[key] = True
        settings["exclude-adverbs"] = True

        try:
            for output in ask_question_without_sr(vocab_list, amount, settings):
                assert type(output) is ParseWordCompToLatQuestion
                for key in key_combination:
                    with contextlib.suppress(AttributeError):
                        assert not exclude_components_adjective[key](output.components)
        except RuntimeError:
            pass


def test_ending_exclusion_noun():
    word = Noun("puella", "puellae", gender=Gender.FEMININE, meaning="girl")
    vocab_list = VocabList([word], "")
    amount = 50

    keys = tuple(exclude_components_noun.keys())
    all_key_combinations = [combo for r in range(2, 5) for combo in combinations(keys, r)]
    for key_combination in all_key_combinations:
        settings = default_settings.copy()

        for key in key_combination:
            settings[key] = True

        try:
            for output in ask_question_without_sr(vocab_list, amount, settings):
                assert type(output) is ParseWordCompToLatQuestion
                for key in key_combination:
                    with contextlib.suppress(AttributeError):
                        assert not exclude_components_noun[key](output.components)
        except RuntimeError:
            pass


def test_ending_exclusion_pronoun():
    word = Pronoun("hic", meaning="this")
    vocab_list = VocabList([word], "")
    amount = 50

    keys = tuple(exclude_components_pronoun.keys())
    all_key_combinations = [combo for r in range(2, 5) for combo in combinations(keys, r)]
    for key_combination in all_key_combinations:
        settings = default_settings.copy()

        for key in key_combination:
            settings[key] = True

        try:
            for output in ask_question_without_sr(vocab_list, amount, settings):
                assert type(output) is ParseWordCompToLatQuestion
                for key in key_combination:
                    with contextlib.suppress(AttributeError):
                        assert not exclude_components_pronoun[key](output.components)
        except RuntimeError:
            pass


def test_ending_exclusion_verb():
    word = Verb("doceo", "docere", "docui", "doctus", meaning="teach")
    vocab_list = VocabList([word], "")
    amount = 50

    keys = tuple(exclude_components_verb.keys())
    all_key_combinations = [combo for r in range(2, 5) for combo in combinations(keys, r)]
    for key_combination in all_key_combinations:
        settings = default_settings.copy()

        for key in key_combination:
            settings[key] = True
        settings["exclude-participles"] = True

        try:
            for output in ask_question_without_sr(vocab_list, amount, settings):
                assert type(output) is ParseWordCompToLatQuestion
                for key in key_combination:
                    with contextlib.suppress(AttributeError):
                        assert not exclude_components_verb[key](output.components)
        except RuntimeError:
            pass


# Just copying the above test, as regular words should not cause any issues
def test_ending_exclusion_regularword():
    word = RegularWord("sed", meaning="but")
    vocab_list = VocabList([word], "")
    amount = 50

    keys = tuple(exclude_components_verb.keys())
    all_key_combinations = [combo for r in range(2, 5) for combo in combinations(keys, r)]
    for key_combination in all_key_combinations:
        settings = default_settings.copy()

        for key in key_combination:
            settings[key] = True

        try:
            for output in ask_question_without_sr(vocab_list, amount, settings):
                assert type(output) is ParseWordCompToLatQuestion
                for key in key_combination:
                    with contextlib.suppress(AttributeError):
                        assert not exclude_components_verb[key](output.components)
        except RuntimeError:
            pass
