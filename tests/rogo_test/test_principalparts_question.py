from pathlib import Path

import pytest
from src.core.accido.endings import Adjective, Noun, Pronoun, Verb
from src.core.accido.misc import Gender
from src.core.lego.misc import VocabList
from src.core.lego.reader import read_vocab_file
from src.core.rogo.asker import ask_question_without_sr
from src.core.rogo.question_classes import PrincipalPartsQuestion
from src.core.rogo.type_aliases import Settings
from src.pb.vocab_tuister.v1 import SessionConfig

# they're not needed
settings: Settings = Settings(**{"cache-vocab-lists": False, "include-synonyms": False, "include-similar-words": False})


session_config: SessionConfig = SessionConfig(
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
    include_principal_parts=True,
    include_multiplechoice_engtolat=False,
    include_multiplechoice_lattoeng=False,
    number_multiplechoice_options=3,
)


@pytest.mark.manual
def test_principalparts_question():
    vocab_list = read_vocab_file(Path("tests/lego_test/testdata/regular_list.txt"))
    amount = 50
    for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
        q = output.principal_parts
        assert type(q) is PrincipalPartsQuestion

        ic(q)  # ruff:ignore[undefined-name]


def test_principalparts_adjective():
    word = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
        q = output.principal_parts
        assert type(q) is PrincipalPartsQuestion

        assert q.prompt == "laetus"
        assert q.principal_parts == ["laetus", "laeta", "laetum"]

    word = Adjective("ingens", "ingentis", declension="3", termination=1, meaning="large")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
        q = output.principal_parts
        assert type(q) is PrincipalPartsQuestion

        assert q.prompt == "ingens"
        assert q.principal_parts == ["ingens", "ingentis"]


def test_principalparts_noun():
    word = Noun("puella", "puellae", gender=Gender.FEMININE, meaning="girl")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
        q = output.principal_parts
        assert type(q) is PrincipalPartsQuestion

        assert q.prompt == "puella"
        assert q.principal_parts == ["puella", "puellae"]


def test_principalparts_pronoun():
    word = Pronoun("hic", meaning="this")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
        q = output.principal_parts
        assert type(q) is PrincipalPartsQuestion

        assert q.prompt == "hic"
        assert q.principal_parts == ["hic", "haec", "hoc"]


def test_principalparts_verb():
    word = Verb("doceo", "docere", "docui", "doctus", meaning="teach")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
        q = output.principal_parts
        assert type(q) is PrincipalPartsQuestion

        assert q.prompt == "doceo"
        assert q.principal_parts == ["doceo", "docere", "docui", "doctus"]

    word = Verb("traho", "trahere", "traxi", "tractus", meaning="drag")
    vocab_list = VocabList([word], "")
    amount = 500

    for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
        q = output.principal_parts
        assert type(q) is PrincipalPartsQuestion

        assert q.prompt == "traho"
        assert q.principal_parts == ["traho", "trahere", "traxi", "tractus"]
