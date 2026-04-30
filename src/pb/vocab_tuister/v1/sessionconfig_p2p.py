# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.33.6
# Pydantic Version: 2.13.0
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic import Field


class SessionConfig(BaseModel):
    exclude_adjectives: bool = Field(default=False, alias="exclude-adjectives")
    exclude_adjective_212_declension: bool = Field(
        default=False, alias="exclude-adjective-212-declension"
    )
    exclude_adjective_third_declension: bool = Field(
        default=False, alias="exclude-adjective-third-declension"
    )
    exclude_adjective_masculine: bool = Field(
        default=False, alias="exclude-adjective-masculine"
    )
    exclude_adjective_feminine: bool = Field(
        default=False, alias="exclude-adjective-feminine"
    )
    exclude_adjective_neuter: bool = Field(
        default=False, alias="exclude-adjective-neuter"
    )
    exclude_adjective_nominative: bool = Field(
        default=False, alias="exclude-adjective-nominative"
    )
    exclude_adjective_vocative: bool = Field(
        default=False, alias="exclude-adjective-vocative"
    )
    exclude_adjective_accusative: bool = Field(
        default=False, alias="exclude-adjective-accusative"
    )
    exclude_adjective_genitive: bool = Field(
        default=False, alias="exclude-adjective-genitive"
    )
    exclude_adjective_dative: bool = Field(
        default=False, alias="exclude-adjective-dative"
    )
    exclude_adjective_ablative: bool = Field(
        default=False, alias="exclude-adjective-ablative"
    )
    exclude_adjective_singular: bool = Field(
        default=False, alias="exclude-adjective-singular"
    )
    exclude_adjective_plural: bool = Field(
        default=False, alias="exclude-adjective-plural"
    )
    exclude_adjective_positive: bool = Field(
        default=False, alias="exclude-adjective-positive"
    )
    exclude_adjective_comparative: bool = Field(
        default=False, alias="exclude-adjective-comparative"
    )
    exclude_adjective_superlative: bool = Field(
        default=False, alias="exclude-adjective-superlative"
    )
    exclude_adverbs: bool = Field(default=False, alias="exclude-adverbs")
    exclude_adverb_positive: bool = Field(
        default=False, alias="exclude-adverb-positive"
    )
    exclude_adverb_comparative: bool = Field(
        default=False, alias="exclude-adverb-comparative"
    )
    exclude_adverb_superlative: bool = Field(
        default=False, alias="exclude-adverb-superlative"
    )
    exclude_nouns: bool = Field(default=False, alias="exclude-nouns")
    exclude_noun_first_declension: bool = Field(
        default=False, alias="exclude-noun-first-declension"
    )
    exclude_noun_second_declension: bool = Field(
        default=False, alias="exclude-noun-second-declension"
    )
    exclude_noun_third_declension: bool = Field(
        default=False, alias="exclude-noun-third-declension"
    )
    exclude_noun_fourth_declension: bool = Field(
        default=False, alias="exclude-noun-fourth-declension"
    )
    exclude_noun_fifth_declension: bool = Field(
        default=False, alias="exclude-noun-fifth-declension"
    )
    exclude_noun_irregular_declension: bool = Field(
        default=False, alias="exclude-noun-irregular-declension"
    )
    exclude_noun_nominative: bool = Field(
        default=False, alias="exclude-noun-nominative"
    )
    exclude_noun_vocative: bool = Field(default=False, alias="exclude-noun-vocative")
    exclude_noun_accusative: bool = Field(
        default=False, alias="exclude-noun-accusative"
    )
    exclude_noun_genitive: bool = Field(default=False, alias="exclude-noun-genitive")
    exclude_noun_dative: bool = Field(default=False, alias="exclude-noun-dative")
    exclude_noun_ablative: bool = Field(default=False, alias="exclude-noun-ablative")
    exclude_noun_singular: bool = Field(default=False, alias="exclude-noun-singular")
    exclude_noun_plural: bool = Field(default=False, alias="exclude-noun-plural")
    exclude_pronouns: bool = Field(default=False, alias="exclude-pronouns")
    exclude_pronoun_masculine: bool = Field(
        default=False, alias="exclude-pronoun-masculine"
    )
    exclude_pronoun_feminine: bool = Field(
        default=False, alias="exclude-pronoun-feminine"
    )
    exclude_pronoun_neuter: bool = Field(default=False, alias="exclude-pronoun-neuter")
    exclude_pronoun_nominative: bool = Field(
        default=False, alias="exclude-pronoun-nominative"
    )
    exclude_pronoun_vocative: bool = Field(
        default=False, alias="exclude-pronoun-vocative"
    )
    exclude_pronoun_accusative: bool = Field(
        default=False, alias="exclude-pronoun-accusative"
    )
    exclude_pronoun_genitive: bool = Field(
        default=False, alias="exclude-pronoun-genitive"
    )
    exclude_pronoun_dative: bool = Field(default=False, alias="exclude-pronoun-dative")
    exclude_pronoun_ablative: bool = Field(
        default=False, alias="exclude-pronoun-ablative"
    )
    exclude_pronoun_singular: bool = Field(
        default=False, alias="exclude-pronoun-singular"
    )
    exclude_pronoun_plural: bool = Field(default=False, alias="exclude-pronoun-plural")
    exclude_regulars: bool = Field(default=False, alias="exclude-regulars")
    exclude_verbs: bool = Field(default=False, alias="exclude-verbs")
    exclude_deponents: bool = Field(default=False, alias="exclude-deponents")
    exclude_semi_deponents: bool = Field(default=False, alias="exclude-semi-deponents")
    exclude_verb_first_conjugation: bool = Field(
        default=False, alias="exclude-verb-first-conjugation"
    )
    exclude_verb_second_conjugation: bool = Field(
        default=False, alias="exclude-verb-second-conjugation"
    )
    exclude_verb_third_conjugation: bool = Field(
        default=False, alias="exclude-verb-third-conjugation"
    )
    exclude_verb_fourth_conjugation: bool = Field(
        default=False, alias="exclude-verb-fourth-conjugation"
    )
    exclude_verb_mixed_conjugation: bool = Field(
        default=False, alias="exclude-verb-mixed-conjugation"
    )
    exclude_verb_irregular_conjugation: bool = Field(
        default=False, alias="exclude-verb-irregular-conjugation"
    )
    exclude_verb_present_active_indicative: bool = Field(
        default=False, alias="exclude-verb-present-active-indicative"
    )
    exclude_verb_imperfect_active_indicative: bool = Field(
        default=False, alias="exclude-verb-imperfect-active-indicative"
    )
    exclude_verb_future_active_indicative: bool = Field(
        default=False, alias="exclude-verb-future-active-indicative"
    )
    exclude_verb_perfect_active_indicative: bool = Field(
        default=False, alias="exclude-verb-perfect-active-indicative"
    )
    exclude_verb_pluperfect_active_indicative: bool = Field(
        default=False, alias="exclude-verb-pluperfect-active-indicative"
    )
    exclude_verb_future_perfect_active_indicative: bool = Field(
        default=False, alias="exclude-verb-future-perfect-active-indicative"
    )
    exclude_verb_present_passive_indicative: bool = Field(
        default=False, alias="exclude-verb-present-passive-indicative"
    )
    exclude_verb_imperfect_passive_indicative: bool = Field(
        default=False, alias="exclude-verb-imperfect-passive-indicative"
    )
    exclude_verb_future_passive_indicative: bool = Field(
        default=False, alias="exclude-verb-future-passive-indicative"
    )
    exclude_verb_perfect_passive_indicative: bool = Field(
        default=False, alias="exclude-verb-perfect-passive-indicative"
    )
    exclude_verb_pluperfect_passive_indicative: bool = Field(
        default=False, alias="exclude-verb-pluperfect-passive-indicative"
    )
    exclude_verb_future_perfect_passive_indicative: bool = Field(
        default=False, alias="exclude-verb-future-perfect-passive-indicative"
    )
    exclude_verb_present_active_subjunctive: bool = Field(
        default=False, alias="exclude-verb-present-active-subjunctive"
    )
    exclude_verb_imperfect_active_subjunctive: bool = Field(
        default=False, alias="exclude-verb-imperfect-active-subjunctive"
    )
    exclude_verb_perfect_active_subjunctive: bool = Field(
        default=False, alias="exclude-verb-perfect-active-subjunctive"
    )
    exclude_verb_pluperfect_active_subjunctive: bool = Field(
        default=False, alias="exclude-verb-pluperfect-active-subjunctive"
    )
    exclude_verb_present_active_imperative: bool = Field(
        default=False, alias="exclude-verb-present-active-imperative"
    )
    exclude_verb_future_active_imperative: bool = Field(
        default=False, alias="exclude-verb-future-active-imperative"
    )
    exclude_verb_present_passive_imperative: bool = Field(
        default=False, alias="exclude-verb-present-passive-imperative"
    )
    exclude_verb_future_passive_imperative: bool = Field(
        default=False, alias="exclude-verb-future-passive-imperative"
    )
    exclude_verb_present_active_infinitive: bool = Field(
        default=False, alias="exclude-verb-present-active-infinitive"
    )
    exclude_verb_future_active_infinitive: bool = Field(
        default=False, alias="exclude-verb-future-active-infinitive"
    )
    exclude_verb_perfect_active_infinitive: bool = Field(
        default=False, alias="exclude-verb-perfect-active-infinitive"
    )
    exclude_verb_present_passive_infinitive: bool = Field(
        default=False, alias="exclude-verb-present-passive-infinitive"
    )
    exclude_verb_future_passive_infinitive: bool = Field(
        default=False, alias="exclude-verb-future-passive-infinitive"
    )
    exclude_verb_perfect_passive_infinitive: bool = Field(
        default=False, alias="exclude-verb-perfect-passive-infinitive"
    )
    exclude_verb_singular: bool = Field(default=False, alias="exclude-verb-singular")
    exclude_verb_plural: bool = Field(default=False, alias="exclude-verb-plural")
    exclude_verb_1st_person: bool = Field(
        default=False, alias="exclude-verb-1st-person"
    )
    exclude_verb_2nd_person: bool = Field(
        default=False, alias="exclude-verb-2nd-person"
    )
    exclude_verb_3rd_person: bool = Field(
        default=False, alias="exclude-verb-3rd-person"
    )
    exclude_participles: bool = Field(default=False, alias="exclude-participles")
    exclude_participle_present_active: bool = Field(
        default=False, alias="exclude-participle-present-active"
    )
    exclude_participle_perfect_passive: bool = Field(
        default=False, alias="exclude-participle-perfect-passive"
    )
    exclude_participle_future_active: bool = Field(
        default=False, alias="exclude-participle-future-active"
    )
    exclude_gerundives: bool = Field(default=False, alias="exclude-gerundives")
    exclude_participle_masculine: bool = Field(
        default=False, alias="exclude-participle-masculine"
    )
    exclude_participle_feminine: bool = Field(
        default=False, alias="exclude-participle-feminine"
    )
    exclude_participle_neuter: bool = Field(
        default=False, alias="exclude-participle-neuter"
    )
    exclude_participle_nominative: bool = Field(
        default=False, alias="exclude-participle-nominative"
    )
    exclude_participle_vocative: bool = Field(
        default=False, alias="exclude-participle-vocative"
    )
    exclude_participle_accusative: bool = Field(
        default=False, alias="exclude-participle-accusative"
    )
    exclude_participle_genitive: bool = Field(
        default=False, alias="exclude-participle-genitive"
    )
    exclude_participle_dative: bool = Field(
        default=False, alias="exclude-participle-dative"
    )
    exclude_participle_ablative: bool = Field(
        default=False, alias="exclude-participle-ablative"
    )
    exclude_participle_singular: bool = Field(
        default=False, alias="exclude-participle-singular"
    )
    exclude_participle_plural: bool = Field(
        default=False, alias="exclude-participle-plural"
    )
    exclude_gerunds: bool = Field(default=False, alias="exclude-gerunds")
    exclude_supines: bool = Field(default=False, alias="exclude-supines")
    english_subjunctives: bool = Field(default=False, alias="english-subjunctives")
    english_verbal_nouns: bool = Field(default=False, alias="english-verbal-nouns")
    include_typein_engtolat: bool = Field(
        default=False, alias="include-typein-engtolat"
    )
    include_typein_lattoeng: bool = Field(
        default=False, alias="include-typein-lattoeng"
    )
    include_parse: bool = Field(default=False, alias="include-parse")
    include_inflect: bool = Field(default=False, alias="include-inflect")
    include_principal_parts: bool = Field(
        default=False, alias="include-principal-parts"
    )
    include_multiplechoice_engtolat: bool = Field(
        default=False, alias="include-multiplechoice-engtolat"
    )
    include_multiplechoice_lattoeng: bool = Field(
        default=False, alias="include-multiplechoice-lattoeng"
    )
    number_multiplechoice_options: int = Field(
        default=0, alias="number-multiplechoice-options"
    )
