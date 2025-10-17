"""Contains rules for filtering words and questions."""

import re
from typing import TYPE_CHECKING, Final

from ..accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb
from .question_classes import QuestionClasses

if TYPE_CHECKING:
    from ..accido.type_aliases import Endings
    from ..lego.misc import VocabList
    from .type_aliases import SessionConfig, Vocab

RULE_REGEX: Final[dict[str,str]] = {
    # Verb tense/voice/mood
    "exclude_verb_present_active_indicative": r"^Vpreactind[a-z][a-z]\d$",
    "exclude_verb_imperfect_active_indicative": r"^Vimpactind[a-z][a-z]\d$",
    "exclude_verb_future_active_indicative": r"^Vfutactind[a-z][a-z]\d$",
    "exclude_verb_future_perfect_active_indicative": r"^Vfpractind[a-z][a-z]\d$",
    "exclude_verb_perfect_active_indicative": r"^Vperactind[a-z][a-z]\d$",
    "exclude_verb_pluperfect_active_indicative": r"^Vplpactind[a-z][a-z]\d$",
    "exclude_verb_present_passive_indicative": r"^Vprepasind[a-z][a-z]\d$",
    "exclude_verb_imperfect_passive_indicative": r"^Vimppasind[a-z][a-z]\d$",
    "exclude_verb_future_passive_indicative": r"^Vfutpasind[a-z][a-z]\d$",
    "exclude_verb_future_perfect_passive_indicative": r"^Vfprpasind[a-z][a-z]\d$",
    "exclude_verb_perfect_passive_indicative": r"^Vperpasind[a-z][a-z]\d$",
    "exclude_verb_pluperfect_passive_indicative": r"^Vplppasind[a-z][a-z]\d$",
    "exclude_verb_present_active_subjunctive": r"^Vpreactsbj[a-z][a-z]\d$",
    "exclude_verb_imperfect_active_subjunctive": r"^Vimpactsbj[a-z][a-z]\d$",
    "exclude_verb_perfect_active_subjunctive": r"^Vperactsbj[a-z][a-z]\d$",
    "exclude_verb_pluperfect_active_subjunctive": r"^Vplpactsbj[a-z][a-z]\d$",
    "exclude_verb_present_active_imperative": r"^Vpreactipe[a-z][a-z]\d$",
    "exclude_verb_future_active_imperative": r"^Vfutactipe[a-z][a-z]\d$",
    "exclude_verb_present_passive_imperative": r"^Vprepasipe[a-z][a-z]\d$",
    "exclude_verb_future_passive_imperative": r"^Vfutpasipe[a-z][a-z]\d$",
    "exclude_verb_present_active_infinitive": r"^Vpreactinf   $",
    "exclude_verb_future_active_infinitive": r"^Vfutactinf   $",
    "exclude_verb_perfect_active_infinitive": r"^Vperactinf   $",
    "exclude_verb_present_passive_infinitive": r"^Vprepasinf   $",
    "exclude_verb_future_passive_infinitive": r"^Vfutpasinf   $",
    "exclude_verb_perfect_passive_infinitive": r"^Vperpasinf   $",

    # Verb number
    "exclude_verb_singular": r"^V[a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z]sg\d$",
    "exclude_verb_plural": r"^V[a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z]pl\d$",

    # Verb person
    "exclude_verb_1st_person": r"^V[a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z]1$",
    "exclude_verb_2nd_person": r"^V[a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z]2$",
    "exclude_verb_3rd_person": r"^V[a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z]3$",

    # Participles
    "exclude_participles": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z][a-z][a-z][a-z][a-z][a-z]$",

    # Participle tense/voice
    "exclude_participle_present_active": r"^Vpreactptc[a-z][a-z][a-z][a-z][a-z][a-z]$",
    "exclude_participle_perfect_passive": r"^Vperpasptc[a-z][a-z][a-z][a-z][a-z][a-z]$",
    "exclude_participle_future_active": r"^Vfutactptc[a-z][a-z][a-z][a-z][a-z][a-z]$",
    "exclude_gerundives": r"^Vfutpasptc[a-z][a-z][a-z][a-z][a-z][a-z]$",

    # Participle gender
    "exclude_participle_masculine": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptcm[a-z][a-z][a-z][a-z][a-z]$",
    "exclude_participle_feminine": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptcf[a-z][a-z][a-z][a-z][a-z]$",
    "exclude_participle_neuter": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptcn[a-z][a-z][a-z][a-z][a-z]$",

    # Participle case
    "exclude_participle_nominative": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z]nom[a-z][a-z]$",
    "exclude_participle_vocative": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z]voc[a-z][a-z]$",
    "exclude_participle_accusative": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z]acc[a-z][a-z]$",
    "exclude_participle_genitive": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z]gen[a-z][a-z]$",
    "exclude_participle_dative": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z]dat[a-z][a-z]$",
    "exclude_participle_ablative": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z]abl[a-z][a-z]$",

    # Participle number
    "exclude_participle_singular": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z][a-z][a-z][a-z]sg$",
    "exclude_participle_plural": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z][a-z][a-z][a-z]pl$",

    # Verbal nouns
    "exclude_gerunds": r"^Vger[a-z][a-z][a-z]$",
    "exclude_supines": r"^Vsup[a-z][a-z][a-z]$",

    # Noun case
    "exclude_noun_nominative": r"^Nnom[a-z][a-z]$",
    "exclude_noun_vocative": r"^Nvoc[a-z][a-z]$",
    "exclude_noun_accusative": r"^Nacc[a-z][a-z]$",
    "exclude_noun_genitive": r"^Ngen[a-z][a-z]$",
    "exclude_noun_dative": r"^Ndat[a-z][a-z]$",
    "exclude_noun_ablative": r"^Nabl[a-z][a-z]$",

    # Noun number
    "exclude_noun_singular": r"^N[a-z][a-z][a-z]sg$",
    "exclude_noun_plural": r"^N[a-z][a-z][a-z]pl$",

    # Adjective gender
    "exclude_adjective_masculine": r"^A[a-z][a-z][a-z]m[a-z][a-z][a-z][a-z][a-z]$",
    "exclude_adjective_feminine": r"^A[a-z][a-z][a-z]f[a-z][a-z][a-z][a-z][a-z]$",
    "exclude_adjective_neuter": r"^A[a-z][a-z][a-z]n[a-z][a-z][a-z][a-z][a-z]$",

    # Adjective case
    "exclude_adjective_nominative": r"^A[a-z][a-z][a-z][a-z]nom[a-z][a-z]$",
    "exclude_adjective_vocative": r"^A[a-z][a-z][a-z][a-z]voc[a-z][a-z]$",
    "exclude_adjective_accusative": r"^A[a-z][a-z][a-z][a-z]acc[a-z][a-z]$",
    "exclude_adjective_genitive": r"^A[a-z][a-z][a-z][a-z]gen[a-z][a-z]$",
    "exclude_adjective_dative": r"^A[a-z][a-z][a-z][a-z]dat[a-z][a-z]$",
    "exclude_adjective_ablative": r"^A[a-z][a-z][a-z][a-z]abl[a-z][a-z]$",
    
    # Adjective number
    "exclude_adjective_singular": r"^A[a-z][a-z][a-z][a-z][a-z][a-z][a-z]sg$",
    "exclude_adjective_plural": r"^A[a-z][a-z][a-z][a-z][a-z][a-z][a-z]pl$",
    
    # Adjective degree
    "exclude_adjective_positive": r"^Apos[a-z][a-z][a-z][a-z][a-z][a-z]$",
    "exclude_adjective_comparative": r"^Acmp[a-z][a-z][a-z][a-z][a-z][a-z]$",
    "exclude_adjective_superlative": r"^Aspr[a-z][a-z][a-z][a-z][a-z][a-z]$",
    
    # Adverb
    "exclude_adverbs": r"^D[a-z][a-z][a-z]$",
    
    # Adverb degree
    "exclude_adverb_positive": r"^Dpos$",
    "exclude_adverb_comparative": r"^Dcmp$",
    "exclude_adverb_superlative": r"^Dspr$",
    
    # Pronoun gender
    "exclude_pronoun_masculine": r"^Pm[a-z][a-z][a-z][a-z][a-z]$",
    "exclude_pronoun_feminine": r"^Pf[a-z][a-z][a-z][a-z][a-z]$",
    "exclude_pronoun_neuter": r"^Pn[a-z][a-z][a-z][a-z][a-z]$",

    # Pronoun case
    "exclude_pronoun_nominative": r"^P[a-z]nom[a-z][a-z]$",
    "exclude_pronoun_vocative": r"^P[a-z]voc[a-z][a-z]$",
    "exclude_pronoun_accusative": r"^P[a-z]acc[a-z][a-z]$",
    "exclude_pronoun_genitive": r"^P[a-z]gen[a-z][a-z]$",
    "exclude_pronoun_dative": r"^P[a-z]dat[a-z][a-z]$",
    "exclude_pronoun_ablative": r"^P[a-z]abl[a-z][a-z]$",

    # Pronoun number
    "exclude_pronoun_singular": r"^P[a-z][a-z][a-z][a-z]sg$",
    "exclude_pronoun_plural": r"^P[a-z][a-z][a-z][a-z]pl$",
}  # fmt: skip

CLASS_RULES: Final[dict[str, QuestionClasses]] = {
    "include_typein_engtolat": QuestionClasses.TYPEIN_ENGTOLAT,
    "include_typein_lattoeng": QuestionClasses.TYPEIN_LATTOENG,
    "include_parse": QuestionClasses.PARSEWORD_LATTOCOMP,
    "include_inflect": QuestionClasses.PARSEWORD_COMPTOLAT,
    "include_principal_parts": QuestionClasses.PRINCIPAL_PARTS,
    "include_multiplechoice_engtolat": QuestionClasses.MULTIPLECHOICE_ENGTOLAT,
    "include_multiplechoice_lattoeng": QuestionClasses.MULTIPLECHOICE_LATTOENG,
}


def filter_words(
    vocab_list: VocabList, session_config: SessionConfig
) -> Vocab:
    """Filter the vocab list based on the session config given.

    Parameters
    ----------
    vocab_list : VocabList
        The vocab list to filter.
    session_config : SessionConfig
        The session config to use for filtering.

    Returns
    -------
    Vocab
        The filtered vocab (as just a list of the objects).
    """

    def _filter_classes(vocab_list: Vocab, classes: tuple[type, ...]) -> Vocab:
        return [item for item in vocab_list if not isinstance(item, classes)]

    vocab = vocab_list.vocab.copy()
    to_exclude: list[type] = []

    if session_config.exclude_nouns:
        to_exclude.append(Noun)
    if session_config.exclude_verbs:
        to_exclude.append(Verb)
    if session_config.exclude_adjectives:
        to_exclude.append(Adjective)
    if session_config.exclude_pronouns:
        to_exclude.append(Pronoun)
    if session_config.exclude_regulars:
        to_exclude.append(RegularWord)

    if to_exclude:
        vocab = _filter_classes(vocab, tuple(to_exclude))

    # Iterate over copy of list to avoid errors
    for item in vocab.copy():
        match item:
            case Verb():
                current_conjugation = item.conjugation
                conjugation_excluded = (
                    (
                        session_config.exclude_verb_first_conjugation
                        and current_conjugation == 1
                    )
                    or (
                        session_config.exclude_verb_second_conjugation
                        and current_conjugation == 2
                    )
                    or (
                        session_config.exclude_verb_third_conjugation
                        and current_conjugation == 3
                    )
                    or (
                        session_config.exclude_verb_fourth_conjugation
                        and current_conjugation == 4
                    )
                    or (
                        session_config.exclude_verb_mixed_conjugation
                        and current_conjugation == 5
                    )
                    or (
                        session_config.exclude_verb_irregular_conjugation
                        and current_conjugation == 0
                    )
                )
                if conjugation_excluded:
                    vocab.remove(item)

                if session_config.exclude_deponents and item.deponent:
                    vocab.remove(item)

            case Noun():
                current_declension = item.declension
                declension_excluded = (
                    (
                        session_config.exclude_noun_first_declension
                        and current_declension == 1
                    )
                    or (
                        session_config.exclude_noun_second_declension
                        and current_declension == 2
                    )
                    or (
                        session_config.exclude_noun_third_declension
                        and current_declension == 3
                    )
                    or (
                        session_config.exclude_noun_fourth_declension
                        and current_declension == 4
                    )
                    or (
                        session_config.exclude_noun_fifth_declension
                        and current_declension == 5
                    )
                    or (
                        session_config.exclude_noun_irregular_declension
                        and current_declension == 0
                    )
                )
                if declension_excluded:
                    vocab.remove(item)

            case Adjective():
                current_adj_declension = item.declension
                if (
                    session_config.exclude_adjective_212_declension
                    and current_adj_declension == "212"
                ) or (
                    session_config.exclude_adjective_third_declension
                    and current_adj_declension == "3"
                ):
                    vocab.remove(item)

            case _:
                pass

    return vocab


def filter_endings(endings: Endings, session_config: SessionConfig) -> Endings:
    """Filter the endings to exclude any endings specified in the session config.

    Parameters
    ----------
    endings : Endings
        The endings to filter.
    session_config : SessionConfig
        The session config to use for filtering.

    Returns
    -------
    Endings
        The filtered endings.
    """
    filtered_endings = endings
    for setting, value in session_config.model_dump().items():  # pyright: ignore[reportAny]
        if value and (setting in RULE_REGEX):
            regex_pattern = RULE_REGEX[setting]
            filtered_endings = {
                key: ending
                for key, ending in filtered_endings.items()
                if not re.match(regex_pattern, key)
            }

    return filtered_endings


def filter_questions(session_config: SessionConfig) -> set[QuestionClasses]:
    """Filter the question types using the session config.

    Parameters
    ----------
    session_config : SessionConfig
        The session config to use for filtering.

    Returns
    -------
    set[QuestionClasses]
        The filtered classes.
    """
    return {
        value
        for key, value in CLASS_RULES.items()
        if getattr(session_config, key)
    }
