from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from src.core.accido.endings import Adjective, Noun, Pronoun, Verb
from src.core.accido.misc import Gender
from src.core.lego.misc import VocabList
from src.core.lego.reader import read_vocab_file
from src.core.rogo.asker import ask_question_without_sr
from src.core.rogo.question_classes import PrincipalPartsQuestion

if TYPE_CHECKING:
    from src.core.rogo.type_aliases import SessionConfig, Settings

settings: Settings = {"include-synonyms": False, "include-similar-words": False}  # they're not needed

session_config: SessionConfig = {
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
    "include-principal-parts": True,
    "include-multiplechoice-engtolat": False,
    "include-multiplechoice-lattoeng": False,
    "number-multiplechoice-options": 3,
}


@pytest.mark.manual
def test_principalparts_question():
    vocab_list = read_vocab_file(Path("tests/lego_test/testdata/regular_list.txt"))
    amount = 50
    for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
        assert type(output) is PrincipalPartsQuestion

        assert output.check(output.principal_parts)
        ic(output)  # noqa: F821


def test_principalparts_adjective():
    word = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
        assert type(output) is PrincipalPartsQuestion
        assert output.check(output.principal_parts)

        assert output.prompt == "laetus"
        assert output.principal_parts == ("laetus", "laeta", "laetum")

    word = Adjective("ingens", "ingentis", declension="3", termination=1, meaning="large")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
        assert type(output) is PrincipalPartsQuestion
        assert output.check(output.principal_parts)

        assert output.prompt == "ingens"
        assert output.principal_parts == ("ingens", "ingentis")


def test_principalparts_noun():
    word = Noun("puella", "puellae", gender=Gender.FEMININE, meaning="girl")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
        assert type(output) is PrincipalPartsQuestion
        assert output.check(output.principal_parts)

        assert output.prompt == "puella"
        assert output.principal_parts == ("puella", "puellae")


def test_principalparts_pronoun():
    word = Pronoun("hic", meaning="this")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
        assert type(output) is PrincipalPartsQuestion
        assert output.check(output.principal_parts)

        assert output.prompt == "hic"
        assert output.principal_parts == ("hic", "haec", "hoc")


def test_principalparts_verb():
    word = Verb("doceo", "docere", "docui", "doctus", meaning="teach")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
        assert type(output) is PrincipalPartsQuestion
        assert output.check(output.principal_parts)

        assert output.prompt == "doceo"
        assert output.principal_parts == ("doceo", "docere", "docui", "doctus")

    word = Verb("traho", "trahere", "traxi", "tractus", meaning="drag")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
        assert type(output) is PrincipalPartsQuestion
        assert output.check(output.principal_parts)

        assert output.prompt == "traho"
        assert output.principal_parts == ("traho", "trahere", "traxi", "tractus")
