import os
import sys  # noqa: E401

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from pathlib import Path

import pytest
from python_src.accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb
from python_src.accido.misc import Gender
from python_src.lego.misc import VocabList
from python_src.lego.reader import read_vocab_file
from python_src.rogo.asker import ask_question_without_sr
from python_src.rogo.question_classes import MultipleChoiceEngToLatQuestion
from python_src.rogo.type_aliases import Settings
from python_src.utils import contains_duplicates

settings: Settings = {
    "exclude-verb-present-active-indicative": False,
    "exclude-verb-imperfect-active-indicative": False,
    "exclude-verb-perfect-active-indicative": False,
    "exclude-verb-pluperfect-active-indicative": False,
    "exclude-verb-present-active-infinitive": False,
    "exclude-verb-present-active-imperative": False,
    "exclude-verb-imperfect-active-subjunctive": False,
    "exclude-verb-pluperfect-active-subjunctive": False,
    "exclude-verb-singular": False,
    "exclude-verb-plural": False,
    "exclude-verb-1st-person": False,
    "exclude-verb-2nd-person": False,
    "exclude-verb-3rd-person": False,
    "exclude-participles": False,
    "exclude-participle-present-active": False,
    "exclude-participle-perfect-passive": False,
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
    "exclude-adjectives": False,
    "exclude-pronouns": False,
    "exclude-regulars": False,
    "exclude-verb-first-conjugation": False,
    "exclude-verb-second-conjugation": False,
    "exclude-verb-third-conjugation": False,
    "exclude-verb-fourth-conjugation": False,
    "exclude-verb-thirdio-conjugation": False,
    "exclude-verb-irregular-conjugation": False,
    "exclude-noun-first-declension": False,
    "exclude-noun-second-declension": False,
    "exclude-noun-third-declension": False,
    "exclude-noun-fourth-declension": False,
    "exclude-noun-fifth-declension": False,
    "exclude-noun-irregular-declension": False,
    "exclude-adjective-212-declension": False,
    "exclude-adjective-third-declension": False,
    "include-typein-engtolat": False,
    "include-typein-lattoeng": False,
    "include-parse": False,
    "include-inflect": False,
    "include-principal-parts": False,
    "include-multiplechoice-engtolat": True,
    "include-multiplechoice-lattoeng": False,
    "number-multiplechoice-options": 3,
}


@pytest.mark.manual
def test_multiplechoice_engtolat():
    vocab_list = read_vocab_file(Path("tests/python_src_lego/test_vocab_files/regular_list.txt"))
    amount = 50

    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is MultipleChoiceEngToLatQuestion
        assert output.check(output.answer)

        assert not contains_duplicates(output.choices)
        assert output.answer in output.choices
        assert len(output.choices) == 3

        ic(output)  # type: ignore[name-defined] # noqa: F821


def test_multiplechoice_engtolat_adjective():
    word1 = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")
    word2 = Adjective("ingens", "ingentis", declension="3", termination=1, meaning="large")
    word3 = Adjective("fortis", "forte", declension="3", termination=2, meaning="strong")
    vocab_list = VocabList([word1, word2, word3])
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is MultipleChoiceEngToLatQuestion
        assert output.check(output.answer)

        assert not contains_duplicates(output.choices)
        assert output.answer in output.choices
        assert len(output.choices) == 3
        assert set(output.choices) == {"laetus", "ingens", "fortis"}
        assert (output.prompt, output.answer) in {("happy", "laetus"), ("large", "ingens"), ("strong", "fortis")}


def test_multiplechoice_engtolat_noun():
    word1 = Noun(nominative="puella", genitive="puellae", gender=Gender.FEMININE, meaning="girl")
    word2 = Noun(nominative="servus", genitive="servi", gender=Gender.MASCULINE, meaning="slave")
    word3 = Noun(nominative="canis", genitive="canis", gender=Gender.MASCULINE, meaning="dog")
    vocab_list = VocabList([word1, word2, word3])
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is MultipleChoiceEngToLatQuestion
        assert output.check(output.answer)

        assert not contains_duplicates(output.choices)
        assert output.answer in output.choices
        assert len(output.choices) == 3
        assert set(output.choices) == {"puella", "servus", "canis"}
        assert (output.prompt, output.answer) in {("girl", "puella"), ("slave", "servus"), ("dog", "canis")}


def test_multiplechoice_engtolat_pronoun():
    word1 = Pronoun(pronoun="hic", meaning="this")
    word2 = Pronoun(pronoun="ille", meaning="that")
    word3 = Pronoun(pronoun="qui", meaning="who")
    vocab_list = VocabList([word1, word2, word3])
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is MultipleChoiceEngToLatQuestion
        assert output.check(output.answer)

        assert not contains_duplicates(output.choices)
        assert output.answer in output.choices
        assert len(output.choices) == 3
        assert set(output.choices) == {"hic", "ille", "qui"}
        assert (output.prompt, output.answer) in {("this", "hic"), ("that", "ille"), ("who", "qui")}


def test_multiplechoice_engtolat_verb():
    word1 = Verb(present="doceo", infinitive="docere", perfect="docui", ppp="doctus", meaning="teach")
    word2 = Verb(present="traho", infinitive="trahere", perfect="traxi", ppp="tractus", meaning="drag")
    word3 = Verb(present="audio", infinitive="audire", perfect="audivi", ppp="auditus", meaning="hear")
    vocab_list = VocabList([word1, word2, word3])
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is MultipleChoiceEngToLatQuestion
        assert output.check(output.answer)

        assert not contains_duplicates(output.choices)
        assert output.answer in output.choices
        assert len(output.choices) == 3
        assert set(output.choices) == {"doceo", "traho", "audio"}
        assert (output.prompt, output.answer) in {("teach", "doceo"), ("drag", "traho"), ("hear", "audio")}


def test_multiplechoice_engtolat_regularword():
    word1 = RegularWord(word="in", meaning="in")
    word2 = RegularWord(word="e", meaning="out of")
    word3 = RegularWord(word="post", meaning="after")
    vocab_list = VocabList([word1, word2, word3])
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, settings):
        assert type(output) is MultipleChoiceEngToLatQuestion
        assert output.check(output.answer)

        assert not contains_duplicates(output.choices)
        assert output.answer in output.choices
        assert len(output.choices) == 3
        assert set(output.choices) == {"in", "e", "post"}
        assert (output.prompt, output.answer) in {("in", "in"), ("out of", "e"), ("after", "post")}