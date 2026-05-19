import contextlib
from dataclasses import replace
from itertools import combinations

from src.core.accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb
from src.core.accido.misc import Case, Degree, Gender, Mood, Number, Tense, Voice
from src.core.lego.misc import VocabList
from src.core.rogo.asker import ask_question_without_sr
from src.core.rogo.question_classes import ParseWordCompToLatQuestion
from src.core.rogo.type_aliases import Settings
from src.pb.vocab_tuister.v1 import SessionConfig


def _to_snake(kebab: str) -> str:
    return kebab.replace("-", "_")


settings: Settings = Settings(**{"cache-vocab-lists": False, "include-synonyms": False, "include-similar-words": False})  # they're not needed

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
    include_inflect=True,
    include_principal_parts=False,
    include_multiplechoice_engtolat=False,
    include_multiplechoice_lattoeng=False,
    number_multiplechoice_options=3,
)

# NOTE: These are incomplete but should be enough to test the functionality.
exclude_components_adjective = {
    "exclude_adjective_masculine": lambda components: components.gender == Gender.MASCULINE,
    "exclude_adjective_feminine": lambda components: components.gender == Gender.FEMININE,
    "exclude_adjective_neuter": lambda components: components.gender == Gender.NEUTER,
    "exclude_adjective_nominative": lambda components: components.case == Case.NOMINATIVE,
    "exclude_adjective_vocative": lambda components: components.case == Case.VOCATIVE,
    "exclude_adjective_accusative": lambda components: components.case == Case.ACCUSATIVE,
    "exclude_adjective_genitive": lambda components: components.case == Case.GENITIVE,
    "exclude_adjective_dative": lambda components: components.case == Case.DATIVE,
    "exclude_adjective_ablative": lambda components: components.case == Case.ABLATIVE,
    "exclude_adjective_singular": lambda components: components.number == Number.SINGULAR,
    "exclude_adjective_plural": lambda components: components.number == Number.PLURAL,
    "exclude_adjective_positive": lambda components: components.degree == Degree.POSITIVE,
    "exclude_adjective_comparative": lambda components: components.degree == Degree.COMPARATIVE,
    "exclude_adjective_superlative": lambda components: components.degree == Degree.SUPERLATIVE,
}

exclude_components_noun = {
    "exclude_noun_nominative": lambda components: components.case == Case.NOMINATIVE,
    "exclude_noun_vocative": lambda components: components.case == Case.VOCATIVE,
    "exclude_noun_accusative": lambda components: components.case == Case.ACCUSATIVE,
    "exclude_noun_genitive": lambda components: components.case == Case.GENITIVE,
    "exclude_noun_dative": lambda components: components.case == Case.DATIVE,
    "exclude_noun_ablative": lambda components: components.case == Case.ABLATIVE,
    "exclude_noun_singular": lambda components: components.number == Number.SINGULAR,
    "exclude_noun_plural": lambda components: components.number == Number.PLURAL,
}

exclude_components_pronoun = {
    "exclude_pronoun_masculine": lambda components: components.gender == Gender.MASCULINE,
    "exclude_pronoun_feminine": lambda components: components.gender == Gender.FEMININE,
    "exclude_pronoun_neuter": lambda components: components.gender == Gender.NEUTER,
    "exclude_pronoun_nominative": lambda components: components.case == Case.NOMINATIVE,
    "exclude_pronoun_vocative": lambda components: components.case == Case.VOCATIVE,
    "exclude_pronoun_accusative": lambda components: components.case == Case.ACCUSATIVE,
    "exclude_pronoun_genitive": lambda components: components.case == Case.GENITIVE,
    "exclude_pronoun_dative": lambda components: components.case == Case.DATIVE,
    "exclude_pronoun_ablative": lambda components: components.case == Case.ABLATIVE,
    "exclude_pronoun_singular": lambda components: components.number == Number.SINGULAR,
    "exclude_pronoun_plural": lambda components: components.number == Number.PLURAL,
}

exclude_components_verb = {
    "exclude_verb_present_active_indicative": lambda components: components.tense == Tense.PRESENT and components.voice == Voice.ACTIVE and components.mood == Mood.INDICATIVE,
    "exclude_verb_imperfect_active_indicative": lambda components: components.tense == Tense.IMPERFECT and components.voice == Voice.ACTIVE and components.mood == Mood.INDICATIVE,
    "exclude_verb_perfect_active_indicative": lambda components: components.tense == Tense.PERFECT and components.voice == Voice.ACTIVE and components.mood == Mood.INDICATIVE,
    "exclude_verb_pluperfect_active_indicative": lambda components: components.tense == Tense.PLUPERFECT and components.voice == Voice.ACTIVE and components.mood == Mood.INDICATIVE,
    "exclude_verb_imperfect_active_subjunctive": lambda components: components.tense == Tense.IMPERFECT and components.voice == Voice.ACTIVE and components.mood == Mood.SUBJUNCTIVE,
    "exclude_verb_pluperfect_active_subjunctive": lambda components: components.tense == Tense.PLUPERFECT and components.voice == Voice.ACTIVE and components.mood == Mood.SUBJUNCTIVE,
    "exclude_verb_present_active_imperative": lambda components: components.tense == Tense.PRESENT and components.voice == Voice.ACTIVE and components.mood == Mood.IMPERATIVE,
    "exclude_verb_present_active_infinitive": lambda components: components.tense == Tense.PRESENT and components.voice == Voice.ACTIVE and components.mood == Mood.INFINITIVE,
    "exclude_verb_singular": lambda components: components.number == Number.SINGULAR,
    "exclude_verb_plural": lambda components: components.number == Number.PLURAL,
    "exclude_verb_first_person": lambda components: components.person == 1,
    "exclude_verb_second_person": lambda components: components.person == 2,
    "exclude_verb_third_person": lambda components: components.person == 3,
}


def test_ending_exclusion_adjective():
    word = Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")
    vocab_list = VocabList([word], "")
    amount = 50

    keys = tuple(exclude_components_adjective.keys())
    all_key_combinations = [combo for r in range(2, 5) for combo in combinations(keys, r)]
    for key_combination in all_key_combinations:
        session_config = replace(default_session_config)

        for key in key_combination:
            setattr(session_config, _to_snake(key), True)
        session_config.exclude_adverbs = True

        try:
            for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
                q = output.parse_comp_to_lat
                assert type(q) is ParseWordCompToLatQuestion
                for key in key_combination:
                    with contextlib.suppress(AttributeError):
                        assert not exclude_components_adjective[key](q.components)
        except RuntimeError:
            pass


def test_ending_exclusion_noun():
    word = Noun("puella", "puellae", gender=Gender.FEMININE, meaning="girl")
    vocab_list = VocabList([word], "")
    amount = 50

    keys = tuple(exclude_components_noun.keys())
    all_key_combinations = [combo for r in range(2, 5) for combo in combinations(keys, r)]
    for key_combination in all_key_combinations:
        session_config = replace(default_session_config)

        for key in key_combination:
            setattr(session_config, _to_snake(key), True)

        try:
            for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
                q = output.parse_comp_to_lat
                assert type(q) is ParseWordCompToLatQuestion
                for key in key_combination:
                    with contextlib.suppress(AttributeError):
                        assert not exclude_components_noun[key](q.components)
        except RuntimeError:
            pass


def test_ending_exclusion_pronoun():
    word = Pronoun("hic", meaning="this")
    vocab_list = VocabList([word], "")
    amount = 50

    keys = tuple(exclude_components_pronoun.keys())
    all_key_combinations = [combo for r in range(2, 5) for combo in combinations(keys, r)]
    for key_combination in all_key_combinations:
        session_config = replace(default_session_config)

        for key in key_combination:
            setattr(session_config, _to_snake(key), True)

        try:
            for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
                q = output.parse_comp_to_lat
                assert type(q) is ParseWordCompToLatQuestion
                for key in key_combination:
                    with contextlib.suppress(AttributeError):
                        assert not exclude_components_pronoun[key](q.components)
        except RuntimeError:
            pass


def test_ending_exclusion_verb():
    word = Verb("doceo", "docere", "docui", "doctus", meaning="teach")
    vocab_list = VocabList([word], "")
    amount = 50

    keys = tuple(exclude_components_verb.keys())
    all_key_combinations = [combo for r in range(2, 5) for combo in combinations(keys, r)]
    for key_combination in all_key_combinations:
        session_config = replace(default_session_config)

        for key in key_combination:
            setattr(session_config, _to_snake(key), True)
        session_config.exclude_participles = True

        try:
            for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
                q = output.parse_comp_to_lat
                assert type(q) is ParseWordCompToLatQuestion
                for key in key_combination:
                    with contextlib.suppress(AttributeError):
                        assert not exclude_components_verb[key](q.components)
        except RuntimeError:
            pass


# Just model_copying the above test, as regular words should not cause any issues
def test_ending_exclusion_regularword():
    word = RegularWord("sed", meaning="but")
    vocab_list = VocabList([word], "")
    amount = 50

    keys = tuple(exclude_components_verb.keys())
    all_key_combinations = [combo for r in range(2, 5) for combo in combinations(keys, r)]
    for key_combination in all_key_combinations:
        session_config = replace(default_session_config)

        for key in key_combination:
            setattr(session_config, _to_snake(key), True)

        try:
            for output in ask_question_without_sr(vocab_list, amount, session_config, settings):
                q = output.parse_comp_to_lat
                assert type(q) is ParseWordCompToLatQuestion
                for key in key_combination:
                    with contextlib.suppress(AttributeError):
                        assert not exclude_components_verb[key](q.components)
        except RuntimeError:
            pass
