from dataclasses import replace
from itertools import combinations
from pathlib import Path

from src.core.accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb
from src.core.lego.reader import read_vocab_file
from src.core.rogo.rules import filter_words
from src.pb.vocab_tuister.v1 import SessionConfig


def _to_snake(kebab: str) -> str:
    return kebab.replace("-", "_")


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

exclude_classes = {"exclude_adjectives": Adjective, "exclude_nouns": Noun, "exclude_pronouns": Pronoun, "exclude_verbs": Verb, "exclude_regulars": RegularWord}


def test_class_exclusion():
    vocab_list = read_vocab_file(Path("tests/lego_test/testdata/regular_list.txt"))
    keys = tuple(exclude_classes.keys())
    all_key_combinations = [combo for r in range(2, 5) for combo in combinations(keys, r)]

    for key_combination in all_key_combinations:
        session_config = replace(default_session_config)

        for key in key_combination:
            setattr(session_config, _to_snake(key), True)

        vocab = filter_words(vocab_list, session_config)
        for word in vocab:
            assert not any(isinstance(word, exclude_classes[key]) for key in key_combination)
