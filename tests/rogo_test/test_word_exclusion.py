# pyright: reportTypedDictNotRequiredAccess=false, reportArgumentType=false, reportAttributeAccessIssue=false

from dataclasses import replace
from typing import TYPE_CHECKING

from src.core.accido.endings import Adjective, Noun, Verb
from src.core.accido.misc import Gender
from src.core.lego.misc import VocabList
from src.core.rogo.rules import filter_words
from src.pb.vocab_tuister.v1 import SessionConfig

if TYPE_CHECKING:
    from collections.abc import Sequence


default_session_config: SessionConfig = SessionConfig(
    exclude_verb_present_active_indicative=False,
    exclude_verb_imperfect_active_indicative=False,
    exclude_verb_future_active_indicative=False,
    exclude_verb_perfect_active_indicative=False,
    exclude_verb_pluperfect_active_indicative=False,
    exclude_verb_future_perfect_active_indicative=False,
    exclude_verb_present_active_infinitive=False,
    exclude_verb_future_active_infinitive=False,
    exclude_verb_perfect_active_infinitive=False,
    exclude_verb_present_passive_infinitive=False,
    exclude_verb_future_passive_infinitive=False,
    exclude_verb_perfect_passive_infinitive=False,
    exclude_verb_present_active_imperative=False,
    exclude_verb_future_active_imperative=False,
    exclude_verb_present_passive_imperative=False,
    exclude_verb_future_passive_imperative=False,
    exclude_verb_present_active_subjunctive=False,
    exclude_verb_imperfect_active_subjunctive=False,
    exclude_verb_perfect_active_subjunctive=False,
    exclude_verb_pluperfect_active_subjunctive=False,
    exclude_verb_present_passive_indicative=False,
    exclude_verb_imperfect_passive_indicative=False,
    exclude_verb_future_passive_indicative=False,
    exclude_verb_perfect_passive_indicative=False,
    exclude_verb_pluperfect_passive_indicative=False,
    exclude_verb_future_perfect_passive_indicative=False,
    exclude_verb_singular=False,
    exclude_verb_plural=False,
    exclude_verb_first_person=False,
    exclude_verb_second_person=False,
    exclude_verb_third_person=False,
    exclude_participles=False,
    exclude_participle_present_active=False,
    exclude_participle_perfect_passive=False,
    exclude_participle_future_active=False,
    exclude_gerundives=False,
    exclude_participle_masculine=False,
    exclude_participle_feminine=False,
    exclude_participle_neuter=False,
    exclude_participle_nominative=False,
    exclude_participle_vocative=False,
    exclude_participle_accusative=False,
    exclude_participle_genitive=False,
    exclude_participle_dative=False,
    exclude_participle_ablative=False,
    exclude_participle_singular=False,
    exclude_participle_plural=False,
    exclude_gerunds=False,
    exclude_supines=False,
    exclude_noun_nominative=False,
    exclude_noun_vocative=False,
    exclude_noun_accusative=False,
    exclude_noun_genitive=False,
    exclude_noun_dative=False,
    exclude_noun_ablative=False,
    exclude_noun_singular=False,
    exclude_noun_plural=False,
    exclude_adjective_masculine=False,
    exclude_adjective_feminine=False,
    exclude_adjective_neuter=False,
    exclude_adjective_nominative=False,
    exclude_adjective_vocative=False,
    exclude_adjective_accusative=False,
    exclude_adjective_genitive=False,
    exclude_adjective_dative=False,
    exclude_adjective_ablative=False,
    exclude_adjective_singular=False,
    exclude_adjective_plural=False,
    exclude_adjective_positive=False,
    exclude_adjective_comparative=False,
    exclude_adjective_superlative=False,
    exclude_adverbs=False,
    exclude_adverb_positive=False,
    exclude_adverb_comparative=False,
    exclude_adverb_superlative=False,
    exclude_pronoun_masculine=False,
    exclude_pronoun_feminine=False,
    exclude_pronoun_neuter=False,
    exclude_pronoun_nominative=False,
    exclude_pronoun_vocative=False,
    exclude_pronoun_accusative=False,
    exclude_pronoun_genitive=False,
    exclude_pronoun_dative=False,
    exclude_pronoun_ablative=False,
    exclude_pronoun_singular=False,
    exclude_pronoun_plural=False,
    exclude_nouns=False,
    exclude_verbs=False,
    exclude_deponents=False,
    exclude_semi_deponents=False,
    exclude_adjectives=False,
    exclude_pronouns=False,
    exclude_regulars=False,
    exclude_verb_first_conjugation=False,
    exclude_verb_second_conjugation=False,
    exclude_verb_third_conjugation=False,
    exclude_verb_fourth_conjugation=False,
    exclude_verb_mixed_conjugation=False,
    exclude_verb_irregular_conjugation=False,
    exclude_noun_first_declension=False,
    exclude_noun_second_declension=False,
    exclude_noun_third_declension=False,
    exclude_noun_fourth_declension=False,
    exclude_noun_fifth_declension=False,
    exclude_noun_irregular_declension=False,
    exclude_adjective_212_declension=False,
    exclude_adjective_third_declension=False,
    english_subjunctives=True,
    english_verbal_nouns=True,
    include_typein_engtolat=False,
    include_typein_lattoeng=False,
    include_parse=False,
    include_inflect=False,
    include_principal_parts=False,
    include_multiplechoice_engtolat=False,
    include_multiplechoice_lattoeng=False,
    number_multiplechoice_options=3,
)


def test_word_exclusion_adjective():
    words: list[Adjective] = [Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy"), Adjective("ingens", "ingentis", declension="3", termination=1, meaning="large")]
    vocab_list = VocabList(words, "")
    settings = replace(default_session_config)

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

    settings = replace(default_session_config)

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

    settings = replace(default_session_config)

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
