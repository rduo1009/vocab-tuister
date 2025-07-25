from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from src.core.accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb
from src.core.accido.misc import Gender
from src.core.lego.misc import VocabList
from src.core.lego.reader import read_vocab_file
from src.core.rogo.asker import ask_question_without_sr
from src.core.rogo.question_classes import MultipleChoiceLatToEngQuestion
from src.utils import contains_duplicates

if TYPE_CHECKING:
    from src.core.rogo.type_aliases import Settings

settings: Settings = {
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
    "include-inflect": False,
    "include-principal-parts": False,
    "include-multiplechoice-engtolat": False,
    "include-multiplechoice-lattoeng": True,
    "number-multiplechoice-options": 3,
}


@pytest.mark.manual
def test_multiplechoice_lattoeng():
    vocab_list = read_vocab_file(Path("tests/lego_test/testdata/regular_list.txt"))
    amount = 50
    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is MultipleChoiceLatToEngQuestion
        assert output.check(output.answer)

        assert not contains_duplicates(output.choices)
        assert output.answer in output.choices
        assert len(output.choices) == 3

        ic(output)  # noqa: F821


def test_multiplechoice_engtolat_adjective():
    word1 = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")
    word2 = Adjective("ingens", "ingentis", declension="3", termination=1, meaning="large")
    word3 = Adjective("fortis", "forte", declension="3", termination=2, meaning="strong")
    vocab_list = VocabList([word1, word2, word3], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is MultipleChoiceLatToEngQuestion
        assert output.check(output.answer)

        assert not contains_duplicates(output.choices)
        assert output.answer in output.choices
        assert len(output.choices) == 3
        assert set(output.choices) == {"happy", "large", "strong"}
        assert (output.prompt, output.answer) in {("laetus", "happy"), ("ingens", "large"), ("fortis", "strong")}


def test_multiplechoice_engtolat_noun():
    word1 = Noun("puella", "puellae", gender=Gender.FEMININE, meaning="girl")
    word2 = Noun("servus", "servi", gender=Gender.MASCULINE, meaning="slave")
    word3 = Noun("canis", "canis", gender=Gender.MASCULINE, meaning="dog")
    vocab_list = VocabList([word1, word2, word3], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is MultipleChoiceLatToEngQuestion
        assert output.check(output.answer)

        assert not contains_duplicates(output.choices)
        assert output.answer in output.choices
        assert len(output.choices) == 3
        assert set(output.choices) == {"girl", "slave", "dog"}
        assert (output.prompt, output.answer) in {("puella", "girl"), ("servus", "slave"), ("canis", "dog")}


def test_multiplechoice_engtolat_pronoun():
    word1 = Pronoun("hic", meaning="this")
    word2 = Pronoun("ille", meaning="that")
    word3 = Pronoun("qui", meaning="who")
    vocab_list = VocabList([word1, word2, word3], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is MultipleChoiceLatToEngQuestion
        assert output.check(output.answer)

        assert not contains_duplicates(output.choices)
        assert output.answer in output.choices
        assert len(output.choices) == 3
        assert set(output.choices) == {"this", "that", "who"}
        assert (output.prompt, output.answer) in {("hic", "this"), ("ille", "that"), ("qui", "who")}


def test_multiplechoice_engtolat_verb():
    word1 = Verb("doceo", "docere", "docui", "doctus", meaning="teach")
    word2 = Verb("traho", "trahere", "traxi", "tractus", meaning="drag")
    word3 = Verb("audio", "audire", "audivi", "auditus", meaning="hear")
    vocab_list = VocabList([word1, word2, word3], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is MultipleChoiceLatToEngQuestion
        assert output.check(output.answer)

        assert not contains_duplicates(output.choices)
        assert output.answer in output.choices
        assert len(output.choices) == 3
        assert set(output.choices) == {"teach", "drag", "hear"}
        assert (output.prompt, output.answer) in {("doceo", "teach"), ("traho", "drag"), ("audio", "hear")}


def test_multiplechoice_engtolat_regularword():
    word1 = RegularWord("in", meaning="in")
    word2 = RegularWord("e", meaning="out of")
    word3 = RegularWord("post", meaning="after")
    vocab_list = VocabList([word1, word2, word3], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is MultipleChoiceLatToEngQuestion
        assert output.check(output.answer)

        assert not contains_duplicates(output.choices)
        assert output.answer in output.choices
        assert len(output.choices) == 3
        assert set(output.choices) == {"in", "out of", "after"}
        assert (output.prompt, output.answer) in {("in", "in"), ("e", "out of"), ("post", "after")}
