# pyright: reportGeneralTypeIssues=false

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from src.core.accido.endings import Adjective, Noun, Pronoun, Verb
from src.core.accido.misc import ComponentsSubtype, Gender, Mood, MultipleEndings
from src.core.lego.misc import VocabList
from src.core.lego.reader import read_vocab_file
from src.core.rogo.asker import ask_question_without_sr
from src.core.rogo.question_classes import ParseWordLatToCompQuestion

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
    "include-parse": True,
    "include-inflect": False,
    "include-principal-parts": False,
    "include-multiplechoice-engtolat": False,
    "include-multiplechoice-lattoeng": False,
    "number-multiplechoice-options": 3,
}


@pytest.mark.manual
def test_parse_question():
    vocab_list = read_vocab_file(Path("tests/lego_test/testdata/regular_list.txt"))
    amount = 50
    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is ParseWordLatToCompQuestion

        assert output.check(output.main_answer)
        ic(output)  # noqa: F821


def test_parse_question_adjective():
    word = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is ParseWordLatToCompQuestion
        assert output.check(output.main_answer)

        assert output.main_answer in output.answers
        for answer in output.answers:
            if answer.subtype == ComponentsSubtype.ADVERB:
                assert word.get(degree=answer.degree, adverb=True) == output.prompt
            else:
                assert word.get(degree=answer.degree, gender=answer.gender, case=answer.case, number=answer.number) == output.prompt


def test_parse_question_noun():
    word = Noun("puella", "puellae", gender=Gender.FEMININE, meaning="girl")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is ParseWordLatToCompQuestion
        assert output.check(output.main_answer)

        assert output.main_answer in output.answers
        for answer in output.answers:
            assert word.get(case=answer.case, number=answer.number) == output.prompt


def test_parse_question_pronoun():
    word = Pronoun("hic", meaning="this")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is ParseWordLatToCompQuestion
        assert output.check(output.main_answer)

        assert output.main_answer in output.answers
        for answer in output.answers:
            assert word.get(gender=answer.gender, case=answer.case, number=answer.number) == output.prompt


def test_parse_question_verb():
    word = Verb("doceo", "docere", "docui", "doctus", meaning="teach")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is ParseWordLatToCompQuestion
        assert output.check(output.main_answer)

        assert output.main_answer in output.answers
        for answer in output.answers:
            if answer.subtype == ComponentsSubtype.PARTICIPLE:
                assert answer.mood == Mood.PARTICIPLE
                if isinstance((true_prompt := word.get(tense=answer.tense, voice=answer.voice, mood=answer.mood, participle_case=answer.case, participle_gender=answer.gender, number=answer.number)), str):
                    assert true_prompt == output.prompt
                elif isinstance(true_prompt, MultipleEndings):
                    assert output.prompt in true_prompt.get_all()
                else:
                    pytest.fail(f"Did not expect true_prompt to be {type(true_prompt)}")
            elif answer.subtype == ComponentsSubtype.VERBAL_NOUN:
                assert answer.mood in {Mood.GERUND, Mood.SUPINE}
                assert word.get(mood=answer.mood, participle_case=answer.case) == output.prompt
            elif answer.subtype == ComponentsSubtype.INFINITIVE:
                assert answer.mood == Mood.INFINITIVE
                assert word.get(tense=answer.tense, voice=answer.voice, mood=answer.mood) == output.prompt
            else:
                assert word.get(tense=answer.tense, voice=answer.voice, mood=answer.mood, person=answer.person, number=answer.number) == output.prompt
