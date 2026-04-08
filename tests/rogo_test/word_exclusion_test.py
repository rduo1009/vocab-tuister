# pyright: reportTypedDictNotRequiredAccess=false, reportArgumentType=false, reportAttributeAccessIssue=false


from typing import TYPE_CHECKING

from src.core.accido.endings import Adjective, Noun, Verb
from src.core.accido.misc import Gender
from src.core.lego.misc import VocabList
from src.core.rogo.rules import filter_words
from src.core.rogo.type_aliases import SessionConfig

if TYPE_CHECKING:
    from collections.abc import Sequence


default_session_config: SessionConfig = SessionConfig(**{
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
    "exclude-semi-deponents": False,
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
    "include-multiplechoice-lattoeng": False,
    "number-multiplechoice-options": 3,
})


def test_word_exclusion_adjective():
    words: list[Adjective] = [Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy"), Adjective("ingens", "ingentis", declension="3", termination=1, meaning="large")]
    vocab_list = VocabList(words, "")
    settings = default_session_config.model_copy()

    settings.exclude_adjective_212_declension = True
    settings.exclude_adjective_212_declension = True
    assert filter_words(vocab_list, settings) == [Adjective("ingens", "ingentis", declension="3", termination=1, meaning="large")]
    settings.exclude_adjective_212_declension = False
    settings.exclude_adjective_212_declension = False

    settings.exclude_adjective_third_declension = True
    settings.exclude_adjective_third_declension = True
    assert filter_words(vocab_list, settings) == [Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")]
    settings.exclude_adjective_third_declension = False
    settings.exclude_adjective_third_declension = False


def test_word_exclusion_noun():
    words: list[Noun] = [
        Noun("ancilla", "ancillae", gender=Gender.FEMININE, meaning="slavegirl"),
        Noun("servus", "servi", gender=Gender.MASCULINE, meaning="slave"),
        Noun("carcer", "carceris", gender=Gender.MASCULINE, meaning="prison"),
        Noun("manus", "manus", gender=Gender.FEMININE, meaning="hand"),
        Noun("res", "rei", gender=Gender.FEMININE, meaning="thing"),
        Noun("ego", meaning="I"),
    ]
    vocab_list = VocabList(words, "")
    vocab_list = VocabList(words, "")

    settings = default_session_config.model_copy()

    settings.exclude_noun_first_declension = True
    assert any(word.declension != 1 for word in filter_words(vocab_list, settings))
    settings.exclude_noun_first_declension = False
    settings.exclude_noun_first_declension = True
    assert any(word.declension != 1 for word in filter_words(vocab_list, settings))
    settings.exclude_noun_first_declension = False

    settings.exclude_noun_second_declension = True
    assert any(word.declension != 2 for word in filter_words(vocab_list, settings))
    settings.exclude_noun_second_declension = False
    settings.exclude_noun_second_declension = True
    assert any(word.declension != 2 for word in filter_words(vocab_list, settings))
    settings.exclude_noun_second_declension = False

    settings.exclude_noun_third_declension = True
    assert any(word.declension != 3 for word in filter_words(vocab_list, settings))
    settings.exclude_noun_third_declension = False
    settings.exclude_noun_third_declension = True
    assert any(word.declension != 3 for word in filter_words(vocab_list, settings))
    settings.exclude_noun_third_declension = False

    settings.exclude_noun_fourth_declension = True
    assert any(word.declension != 4 for word in filter_words(vocab_list, settings))
    settings.exclude_noun_fourth_declension = False
    settings.exclude_noun_fourth_declension = True
    assert any(word.declension != 4 for word in filter_words(vocab_list, settings))
    settings.exclude_noun_fourth_declension = False

    settings.exclude_noun_fifth_declension = True
    assert any(word.declension != 5 for word in filter_words(vocab_list, settings))
    settings.exclude_noun_fifth_declension = False
    settings.exclude_noun_fifth_declension = True
    assert any(word.declension != 5 for word in filter_words(vocab_list, settings))
    settings.exclude_noun_fifth_declension = False

    settings.exclude_noun_irregular_declension = True
    assert any(word.declension != 0 for word in filter_words(vocab_list, settings))
    settings.exclude_noun_irregular_declension = False
    settings.exclude_noun_irregular_declension = True
    assert any(word.declension != 0 for word in filter_words(vocab_list, settings))
    settings.exclude_noun_irregular_declension = False


def test_word_exclusion_verb():
    words: Sequence[Verb] = [
        Verb("celo", "celare", "celavi", "celatus", meaning="hide"),
        Verb("pareo", "parere", "parui", "paritum", meaning="hide"),
        Verb("desero", "deserere", "deserui", "desertus", meaning="desert"),
        Verb("patefacio", "patefacere", "patefeci", "patefactus", meaning="reveal"),
        Verb("aperio", "aperire", "aperui", "apertus", meaning="open"),
        Verb("abeo", "abire", "abii", "abitum", meaning="depart"),
    ]
    vocab_list = VocabList(words, "")
    vocab_list = VocabList(words, "")

    settings = default_session_config.model_copy()

    settings.exclude_verb_first_conjugation = True
    assert any(word.conjugation != 1 for word in filter_words(vocab_list, settings))
    settings.exclude_verb_first_conjugation = False
    settings.exclude_verb_first_conjugation = True
    assert any(word.conjugation != 1 for word in filter_words(vocab_list, settings))
    settings.exclude_verb_first_conjugation = False

    settings.exclude_verb_second_conjugation = True
    assert any(word.conjugation != 2 for word in filter_words(vocab_list, settings))
    settings.exclude_verb_second_conjugation = False
    settings.exclude_verb_second_conjugation = True
    assert any(word.conjugation != 2 for word in filter_words(vocab_list, settings))
    settings.exclude_verb_second_conjugation = False

    settings.exclude_verb_third_conjugation = True
    assert any(word.conjugation != 3 for word in filter_words(vocab_list, settings))
    settings.exclude_verb_third_conjugation = False
    settings.exclude_verb_third_conjugation = True
    assert any(word.conjugation != 3 for word in filter_words(vocab_list, settings))
    settings.exclude_verb_third_conjugation = False

    settings.exclude_verb_fourth_conjugation = True
    assert any(word.conjugation != 4 for word in filter_words(vocab_list, settings))
    settings.exclude_verb_fourth_conjugation = False
    settings.exclude_verb_fourth_conjugation = True
    assert any(word.conjugation != 4 for word in filter_words(vocab_list, settings))
    settings.exclude_verb_fourth_conjugation = False

    settings.exclude_verb_mixed_conjugation = True
    assert any(word.conjugation != 5 for word in filter_words(vocab_list, settings))
    settings.exclude_verb_mixed_conjugation = False
    settings.exclude_verb_mixed_conjugation = True
    assert any(word.conjugation != 5 for word in filter_words(vocab_list, settings))
    settings.exclude_verb_mixed_conjugation = False

    settings.exclude_verb_irregular_conjugation = True
    assert any(word.conjugation != 0 for word in filter_words(vocab_list, settings))
    settings.exclude_verb_irregular_conjugation = False
