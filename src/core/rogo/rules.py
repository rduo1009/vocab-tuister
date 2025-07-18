"""Contains rules for filtering words and questions."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Final, cast

from ..accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb
from .question_classes import QuestionClasses

if TYPE_CHECKING:
    from ..accido.type_aliases import Endings
    from ..lego.misc import VocabList
    from .type_aliases import Settings, SettingsRules, Vocab

RULE_REGEX: Final[SettingsRules] = {
    # Verb tense/voice/mood
    "exclude-verb-present-active-indicative": r"^Vpreactind[a-z][a-z]\d$",
    "exclude-verb-imperfect-active-indicative": r"^Vimpactind[a-z][a-z]\d$",
    "exclude-verb-future-active-indicative": r"^Vfutactind[a-z][a-z]\d$",
    "exclude-verb-future-perfect-active-indicative": r"^Vfpractind[a-z][a-z]\d$",
    "exclude-verb-perfect-active-indicative": r"^Vperactind[a-z][a-z]\d$",
    "exclude-verb-pluperfect-active-indicative": r"^Vplpactind[a-z][a-z]\d$",
    "exclude-verb-present-passive-indicative": r"^Vprepasind[a-z][a-z]\d$",
    "exclude-verb-imperfect-passive-indicative": r"^Vimppasind[a-z][a-z]\d$",
    "exclude-verb-future-passive-indicative": r"^Vfutpasind[a-z][a-z]\d$",
    "exclude-verb-future-perfect-passive-indicative": r"^Vfprpasind[a-z][a-z]\d$",
    "exclude-verb-perfect-passive-indicative": r"^Vperpasind[a-z][a-z]\d$",
    "exclude-verb-pluperfect-passive-indicative": r"^Vplppasind[a-z][a-z]\d$",
    "exclude-verb-present-active-subjunctive": r"^Vpreactsbj[a-z][a-z]\d$",
    "exclude-verb-imperfect-active-subjunctive": r"^Vimpactsbj[a-z][a-z]\d$",
    "exclude-verb-perfect-active-subjunctive": r"^Vperactsbj[a-z][a-z]\d$",
    "exclude-verb-pluperfect-active-subjunctive": r"^Vplpactsbj[a-z][a-z]\d$",
    "exclude-verb-present-active-imperative": r"^Vpreactipe[a-z][a-z]\d$",
    "exclude-verb-future-active-imperative": r"^Vfutactipe[a-z][a-z]\d$",
    "exclude-verb-present-passive-imperative": r"^Vprepasipe[a-z][a-z]\d$",
    "exclude-verb-future-passive-imperative": r"^Vfutpasipe[a-z][a-z]\d$",
    "exclude-verb-present-active-infinitive": r"^Vpreactinf   $",
    "exclude-verb-future-active-infinitive": r"^Vfutactinf   $",
    "exclude-verb-perfect-active-infinitive": r"^Vperactinf   $",
    "exclude-verb-present-passive-infinitive": r"^Vprepasinf   $",
    "exclude-verb-future-passive-infinitive": r"^Vfutpasinf   $",
    "exclude-verb-perfect-passive-infinitive": r"^Vperpasinf   $",

    # Verb number
    "exclude-verb-singular": r"^V[a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z]sg\d$",
    "exclude-verb-plural": r"^V[a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z]pl\d$",

    # Verb person
    "exclude-verb-1st-person": r"^V[a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z]1$",
    "exclude-verb-2nd-person": r"^V[a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z]2$",
    "exclude-verb-3rd-person": r"^V[a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z][a-z]3$",

    # Participles
    "exclude-participles": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z][a-z][a-z][a-z][a-z][a-z]$",

    # Participle tense/voice
    "exclude-participle-present-active": r"^Vpreactptc[a-z][a-z][a-z][a-z][a-z][a-z]$",
    "exclude-participle-perfect-passive": r"^Vperpasptc[a-z][a-z][a-z][a-z][a-z][a-z]$",
    "exclude-participle-future-active": r"^Vfutactptc[a-z][a-z][a-z][a-z][a-z][a-z]$",
    "exclude-gerundives": r"^Vfutpasptc[a-z][a-z][a-z][a-z][a-z][a-z]$",

    # Participle gender
    "exclude-participle-masculine": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptcm[a-z][a-z][a-z][a-z][a-z]$",
    "exclude-participle-feminine": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptcf[a-z][a-z][a-z][a-z][a-z]$",
    "exclude-participle-neuter": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptcn[a-z][a-z][a-z][a-z][a-z]$",

    # Participle case
    "exclude-participle-nominative": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z]nom[a-z][a-z]$",
    "exclude-participle-vocative": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z]voc[a-z][a-z]$",
    "exclude-participle-accusative": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z]acc[a-z][a-z]$",
    "exclude-participle-genitive": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z]gen[a-z][a-z]$",
    "exclude-participle-dative": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z]dat[a-z][a-z]$",
    "exclude-participle-ablative": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z]abl[a-z][a-z]$",

    # Participle number
    "exclude-participle-singular": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z][a-z][a-z][a-z]sg$",
    "exclude-participle-plural": r"^V[a-z][a-z][a-z][a-z][a-z][a-z]ptc[a-z][a-z][a-z][a-z]pl$",

    # Verbal nouns
    "exclude-gerunds": r"^Vger[a-z][a-z][a-z]$",
    "exclude-supines": r"^Vsup[a-z][a-z][a-z]$",

    # Noun case
    "exclude-noun-nominative": r"^Nnom[a-z][a-z]$",
    "exclude-noun-vocative": r"^Nvoc[a-z][a-z]$",
    "exclude-noun-accusative": r"^Nacc[a-z][a-z]$",
    "exclude-noun-genitive": r"^Ngen[a-z][a-z]$",
    "exclude-noun-dative": r"^Ndat[a-z][a-z]$",
    "exclude-noun-ablative": r"^Nabl[a-z][a-z]$",

    # Noun number
    "exclude-noun-singular": r"^N[a-z][a-z][a-z]sg$",
    "exclude-noun-plural": r"^N[a-z][a-z][a-z]pl$",

    # Adjective gender
    "exclude-adjective-masculine": r"^A[a-z][a-z][a-z]m[a-z][a-z][a-z][a-z][a-z]$",
    "exclude-adjective-feminine": r"^A[a-z][a-z][a-z]f[a-z][a-z][a-z][a-z][a-z]$",
    "exclude-adjective-neuter": r"^A[a-z][a-z][a-z]n[a-z][a-z][a-z][a-z][a-z]$",

    # Adjective case
    "exclude-adjective-nominative": r"^A[a-z][a-z][a-z][a-z]nom[a-z][a-z]$",
    "exclude-adjective-vocative": r"^A[a-z][a-z][a-z][a-z]voc[a-z][a-z]$",
    "exclude-adjective-accusative": r"^A[a-z][a-z][a-z][a-z]acc[a-z][a-z]$",
    "exclude-adjective-genitive": r"^A[a-z][a-z][a-z][a-z]gen[a-z][a-z]$",
    "exclude-adjective-dative": r"^A[a-z][a-z][a-z][a-z]dat[a-z][a-z]$",
    "exclude-adjective-ablative": r"^A[a-z][a-z][a-z][a-z]abl[a-z][a-z]$",
    
    # Adjective number
    "exclude-adjective-singular": r"^A[a-z][a-z][a-z][a-z][a-z][a-z][a-z]sg$",
    "exclude-adjective-plural": r"^A[a-z][a-z][a-z][a-z][a-z][a-z][a-z]pl$",
    
    # Adjective degree
    "exclude-adjective-positive": r"^Apos[a-z][a-z][a-z][a-z][a-z][a-z]$",
    "exclude-adjective-comparative": r"^Acmp[a-z][a-z][a-z][a-z][a-z][a-z]$",
    "exclude-adjective-superlative": r"^Aspr[a-z][a-z][a-z][a-z][a-z][a-z]$",
    
    # Adverb
    "exclude-adverbs": r"^D[a-z][a-z][a-z]$",
    
    # Adverb degree
    "exclude-adverb-positive": r"^Dpos$",
    "exclude-adverb-comparative": r"^Dcmp$",
    "exclude-adverb-superlative": r"^Dspr$",
    
    # Pronoun gender
    "exclude-pronoun-masculine": r"^Pm[a-z][a-z][a-z][a-z][a-z]$",
    "exclude-pronoun-feminine": r"^Pf[a-z][a-z][a-z][a-z][a-z]$",
    "exclude-pronoun-neuter": r"^Pn[a-z][a-z][a-z][a-z][a-z]$",

    # Pronoun case
    "exclude-pronoun-nominative": r"^P[a-z]nom[a-z][a-z]$",
    "exclude-pronoun-vocative": r"^P[a-z]voc[a-z][a-z]$",
    "exclude-pronoun-accusative": r"^P[a-z]acc[a-z][a-z]$",
    "exclude-pronoun-genitive": r"^P[a-z]gen[a-z][a-z]$",
    "exclude-pronoun-dative": r"^P[a-z]dat[a-z][a-z]$",
    "exclude-pronoun-ablative": r"^P[a-z]abl[a-z][a-z]$",

    # Pronoun number
    "exclude-pronoun-singular": r"^P[a-z][a-z][a-z][a-z]sg$",
    "exclude-pronoun-plural": r"^P[a-z][a-z][a-z][a-z]pl$",
}  # fmt: skip

CLASS_RULES: Final[dict[str, QuestionClasses]] = {
    "include-typein-engtolat": QuestionClasses.TYPEIN_ENGTOLAT,
    "include-typein-lattoeng": QuestionClasses.TYPEIN_LATTOENG,
    "include-parse": QuestionClasses.PARSEWORD_LATTOCOMP,
    "include-inflect": QuestionClasses.PARSEWORD_COMPTOLAT,
    "include-principal-parts": QuestionClasses.PRINCIPAL_PARTS,
    "include-multiplechoice-engtolat": QuestionClasses.MULTIPLECHOICE_ENGTOLAT,
    "include-multiplechoice-lattoeng": QuestionClasses.MULTIPLECHOICE_LATTOENG,
}


def filter_words(vocab_list: VocabList, settings: Settings) -> Vocab:
    """Filter the vocabulary list based on the settings given.

    Parameters
    ----------
    vocab_list : VocabList
        The vocabulary list to filter.
    settings : Settings
        The settings to use for filtering.

    Returns
    -------
    Vocab
        The filtered vocabulary list.
    """

    def _filter_classes(vocab_list: Vocab, classes: tuple[type, ...]) -> Vocab:
        return [item for item in vocab_list if not isinstance(item, classes)]

    vocab = vocab_list.vocab.copy()
    to_exclude: list[type] = []

    if settings["exclude-nouns"]:
        to_exclude.append(Noun)
    if settings["exclude-verbs"]:
        to_exclude.append(Verb)
    if settings["exclude-adjectives"]:
        to_exclude.append(Adjective)
    if settings["exclude-pronouns"]:
        to_exclude.append(Pronoun)
    if settings["exclude-regulars"]:
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
                        settings["exclude-verb-first-conjugation"]
                        and current_conjugation == 1
                    )
                    or (
                        settings["exclude-verb-second-conjugation"]
                        and current_conjugation == 2
                    )
                    or (
                        settings["exclude-verb-third-conjugation"]
                        and current_conjugation == 3
                    )
                    or (
                        settings["exclude-verb-fourth-conjugation"]
                        and current_conjugation == 4
                    )
                    or (
                        settings["exclude-verb-mixed-conjugation"]
                        and current_conjugation == 5
                    )
                    or (
                        settings["exclude-verb-irregular-conjugation"]
                        and current_conjugation == 0
                    )
                )
                if conjugation_excluded:
                    vocab.remove(item)

                if settings["exclude-deponents"] and item.deponent:
                    vocab.remove(item)

            case Noun():
                current_declension = item.declension
                declension_excluded = (
                    (
                        settings["exclude-noun-first-declension"]
                        and current_declension == 1
                    )
                    or (
                        settings["exclude-noun-second-declension"]
                        and current_declension == 2
                    )
                    or (
                        settings["exclude-noun-third-declension"]
                        and current_declension == 3
                    )
                    or (
                        settings["exclude-noun-fourth-declension"]
                        and current_declension == 4
                    )
                    or (
                        settings["exclude-noun-fifth-declension"]
                        and current_declension == 5
                    )
                    or (
                        settings["exclude-noun-irregular-declension"]
                        and current_declension == 0
                    )
                )
                if declension_excluded:
                    vocab.remove(item)

            case Adjective():
                current_adj_declension = item.declension
                if (
                    settings["exclude-adjective-212-declension"]
                    and current_adj_declension == "212"
                ) or (
                    settings["exclude-adjective-third-declension"]
                    and current_adj_declension == "3"
                ):
                    vocab.remove(item)

            case _:
                pass

    return vocab


def filter_endings(endings: Endings, settings: Settings) -> Endings:
    """Filter the endings to exclude any endings specified in the settings.

    Parameters
    ----------
    endings : Endings
        The endings to filter.
    settings : Settings
        The settings to use for filtering.

    Returns
    -------
    Endings
        The filtered endings.
    """
    filtered_endings = endings
    for setting, value in settings.items():
        if value and (setting in RULE_REGEX):
            regex_pattern = cast("str", RULE_REGEX[setting])
            filtered_endings = {
                key: ending
                for key, ending in filtered_endings.items()
                if not re.match(regex_pattern, key)
            }

    return filtered_endings


def filter_questions(settings: Settings) -> set[QuestionClasses]:
    """Filter the question types using the settings.

    Parameters
    ----------
    settings : Settings
        The settings to use for filtering.

    Returns
    -------
    set[QuestionClasses]
        The filtered classes.
    """
    return {value for key, value in CLASS_RULES.items() if settings[key]}
