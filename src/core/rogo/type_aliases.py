"""Contains type aliases used by rogo."""

# pyright: reportUnannotatedClassAttribute=false

from pydantic import BaseModel, ConfigDict, StrictBool, StrictInt

from src.core.accido.endings import Word

type Vocab = list[Word]


def _to_kebab(snake: str) -> str:
    return snake.replace("_", "-")


class Settings(BaseModel):
    """Global settings for vocab-tester."""

    model_config = ConfigDict(
        extra="forbid",
        validate_by_name=False,
        validate_by_alias=True,
        alias_generator=_to_kebab,
    )

    include_synonyms: StrictBool
    include_similar_words: StrictBool


class SessionConfig(BaseModel):
    """Config for a vocab-tester testing session."""

    model_config = ConfigDict(
        extra="forbid",
        validate_by_name=False,
        validate_by_alias=True,
        alias_generator=_to_kebab,
    )

    exclude_adjectives: StrictBool
    exclude_adjective_212_declension: StrictBool
    exclude_adjective_third_declension: StrictBool
    exclude_adjective_masculine: StrictBool
    exclude_adjective_feminine: StrictBool
    exclude_adjective_neuter: StrictBool
    exclude_adjective_nominative: StrictBool
    exclude_adjective_vocative: StrictBool
    exclude_adjective_accusative: StrictBool
    exclude_adjective_genitive: StrictBool
    exclude_adjective_dative: StrictBool
    exclude_adjective_ablative: StrictBool
    exclude_adjective_singular: StrictBool
    exclude_adjective_plural: StrictBool
    exclude_adjective_positive: StrictBool
    exclude_adjective_comparative: StrictBool
    exclude_adjective_superlative: StrictBool
    exclude_adverbs: StrictBool
    exclude_adverb_positive: StrictBool
    exclude_adverb_comparative: StrictBool
    exclude_adverb_superlative: StrictBool
    exclude_nouns: StrictBool
    exclude_noun_first_declension: StrictBool
    exclude_noun_second_declension: StrictBool
    exclude_noun_third_declension: StrictBool
    exclude_noun_fourth_declension: StrictBool
    exclude_noun_fifth_declension: StrictBool
    exclude_noun_irregular_declension: StrictBool
    exclude_noun_nominative: StrictBool
    exclude_noun_vocative: StrictBool
    exclude_noun_accusative: StrictBool
    exclude_noun_genitive: StrictBool
    exclude_noun_dative: StrictBool
    exclude_noun_ablative: StrictBool
    exclude_noun_singular: StrictBool
    exclude_noun_plural: StrictBool
    exclude_pronouns: StrictBool
    exclude_pronoun_masculine: StrictBool
    exclude_pronoun_feminine: StrictBool
    exclude_pronoun_neuter: StrictBool
    exclude_pronoun_nominative: StrictBool
    exclude_pronoun_vocative: StrictBool
    exclude_pronoun_accusative: StrictBool
    exclude_pronoun_genitive: StrictBool
    exclude_pronoun_dative: StrictBool
    exclude_pronoun_ablative: StrictBool
    exclude_pronoun_singular: StrictBool
    exclude_pronoun_plural: StrictBool
    exclude_regulars: StrictBool
    exclude_verbs: StrictBool
    exclude_deponents: StrictBool
    exclude_semi_deponents: StrictBool
    exclude_verb_first_conjugation: StrictBool
    exclude_verb_second_conjugation: StrictBool
    exclude_verb_third_conjugation: StrictBool
    exclude_verb_fourth_conjugation: StrictBool
    exclude_verb_mixed_conjugation: StrictBool
    exclude_verb_irregular_conjugation: StrictBool
    exclude_verb_present_active_indicative: StrictBool
    exclude_verb_imperfect_active_indicative: StrictBool
    exclude_verb_future_active_indicative: StrictBool
    exclude_verb_perfect_active_indicative: StrictBool
    exclude_verb_pluperfect_active_indicative: StrictBool
    exclude_verb_future_perfect_active_indicative: StrictBool
    exclude_verb_present_passive_indicative: StrictBool
    exclude_verb_imperfect_passive_indicative: StrictBool
    exclude_verb_future_passive_indicative: StrictBool
    exclude_verb_perfect_passive_indicative: StrictBool
    exclude_verb_pluperfect_passive_indicative: StrictBool
    exclude_verb_future_perfect_passive_indicative: StrictBool
    exclude_verb_present_active_subjunctive: StrictBool
    exclude_verb_imperfect_active_subjunctive: StrictBool
    exclude_verb_perfect_active_subjunctive: StrictBool
    exclude_verb_pluperfect_active_subjunctive: StrictBool
    exclude_verb_present_active_imperative: StrictBool
    exclude_verb_future_active_imperative: StrictBool
    exclude_verb_present_passive_imperative: StrictBool
    exclude_verb_future_passive_imperative: StrictBool
    exclude_verb_present_active_infinitive: StrictBool
    exclude_verb_future_active_infinitive: StrictBool
    exclude_verb_perfect_active_infinitive: StrictBool
    exclude_verb_present_passive_infinitive: StrictBool
    exclude_verb_future_passive_infinitive: StrictBool
    exclude_verb_perfect_passive_infinitive: StrictBool
    exclude_verb_singular: StrictBool
    exclude_verb_plural: StrictBool
    exclude_verb_1st_person: StrictBool
    exclude_verb_2nd_person: StrictBool
    exclude_verb_3rd_person: StrictBool
    exclude_participles: StrictBool
    exclude_participle_present_active: StrictBool
    exclude_participle_perfect_passive: StrictBool
    exclude_participle_future_active: StrictBool
    exclude_gerundives: StrictBool
    exclude_participle_masculine: StrictBool
    exclude_participle_feminine: StrictBool
    exclude_participle_neuter: StrictBool
    exclude_participle_nominative: StrictBool
    exclude_participle_vocative: StrictBool
    exclude_participle_accusative: StrictBool
    exclude_participle_genitive: StrictBool
    exclude_participle_dative: StrictBool
    exclude_participle_ablative: StrictBool
    exclude_participle_singular: StrictBool
    exclude_participle_plural: StrictBool
    exclude_gerunds: StrictBool
    exclude_supines: StrictBool
    english_subjunctives: StrictBool
    english_verbal_nouns: StrictBool
    include_typein_engtolat: StrictBool
    include_typein_lattoeng: StrictBool
    include_parse: StrictBool
    include_inflect: StrictBool
    include_principal_parts: StrictBool
    include_multiplechoice_engtolat: StrictBool
    include_multiplechoice_lattoeng: StrictBool
    number_multiplechoice_options: StrictInt
