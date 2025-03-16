"""Contains functions that generate questions and check answers."""

from __future__ import annotations

import logging
import random
from typing import TYPE_CHECKING, Final, overload

from ...utils import set_choice
from ..accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb
from ..accido.misc import (
    Case,
    ComponentsSubtype,
    Gender,
    Mood,
    MultipleEndings,
    MultipleMeanings,
    Number,
)
from ..transfero.words import find_inflection
from .exceptions import InvalidSettingsError
from .question_classes import (
    MultipleChoiceEngToLatQuestion,
    MultipleChoiceLatToEngQuestion,
    ParseWordCompToLatQuestion,
    ParseWordLatToCompQuestion,
    PrincipalPartsQuestion,
    QuestionClasses,
    TypeInEngToLatQuestion,
    TypeInLatToEngQuestion,
)
from .rules import filter_endings, filter_questions, filter_words

if TYPE_CHECKING:
    from collections.abc import Iterable

    from ..accido.endings import _Word
    from ..accido.type_aliases import Ending, Endings
    from ..lego.misc import VocabList
    from .question_classes import Question
    from .type_aliases import Settings, Vocab

logger = logging.getLogger(__name__)

MAX_RETRIES: Final[int] = 1000


def ask_question_without_sr(
    vocab_list: VocabList, amount: int, settings: Settings
) -> Iterable[Question]:
    """Ask a question about Latin vocabulary.

    Parameters
    ----------
    vocab_list : VocabList
        The vocabulary list to use.
    amount : int
        The number of questions to ask.
    settings : Settings
        The settings to use.

    Yields
    ------
    Question
        The question to ask.

    Raises
    ------
    RuntimeError
        If a question cannot be created with the current vocab list and
        settings.
    InvalidSettingsError
        If the settings in `settings` are invalid.
    """
    filtered_vocab = filter_words(vocab_list, settings)
    filtered_questions = filter_questions(settings)

    if len(filtered_vocab) < settings["number-multiplechoice-options"]:
        filtered_questions.discard(QuestionClasses.MULTIPLECHOICE_ENGTOLAT)
        filtered_questions.discard(QuestionClasses.MULTIPLECHOICE_LATTOENG)

    if not filtered_questions:
        raise InvalidSettingsError("No question type has been enabled.")

    for _ in range(amount):
        retries = 0
        while retries < MAX_RETRIES:
            chosen_word = random.choice(filtered_vocab)
            filtered_endings = filter_endings(chosen_word.endings, settings)
            if not filtered_endings:
                retries += 1
                continue

            question_type = set_choice(filtered_questions)

            logger.debug(
                "Creating new question of type %s with word '%s'.",
                question_type.value,
                chosen_word,
            )

            output: Question | None
            match question_type:
                case QuestionClasses.TYPEIN_ENGTOLAT:
                    output = _generate_typein_engtolat(
                        chosen_word, filtered_endings
                    )

                case QuestionClasses.TYPEIN_LATTOENG:
                    output = _generate_typein_lattoeng(
                        chosen_word, filtered_endings
                    )

                case QuestionClasses.PARSEWORD_LATTOCOMP:
                    output = _generate_parse(chosen_word, filtered_endings)

                case QuestionClasses.PARSEWORD_COMPTOLAT:
                    output = _generate_inflect(chosen_word, filtered_endings)

                case QuestionClasses.PRINCIPAL_PARTS:
                    output = _generate_principal_parts_question(chosen_word)

                case QuestionClasses.MULTIPLECHOICE_ENGTOLAT:
                    output = _generate_multiplechoice_engtolat(
                        filtered_vocab,
                        chosen_word,
                        settings["number-multiplechoice-options"],
                    )

                case QuestionClasses.MULTIPLECHOICE_LATTOENG:
                    output = _generate_multiplechoice_lattoeng(
                        filtered_vocab,
                        chosen_word,
                        settings["number-multiplechoice-options"],
                    )

            if output is not None:
                logger.info(
                    "Creating question of type %s with word '%s' succeeded.",
                    question_type.value,
                    chosen_word,
                )

                yield output
                break

            retries += 1
            logger.debug(
                "Creating question of type %s with word '%s' failed.",
                question_type.value,
                chosen_word,
            )
        else:
            raise RuntimeError(
                f"Failed to generate a valid question after {MAX_RETRIES} retries."
            )


def _pick_ending(endings: Endings) -> tuple[str, Ending]:
    return random.choice(list(endings.items()))


def _pick_ending_from_multipleendings(ending: Ending) -> str:
    if isinstance(ending, MultipleEndings):
        return random.choice(ending.get_all())

    return ending


def _generate_typein_engtolat(
    chosen_word: _Word, filtered_endings: Endings
) -> TypeInEngToLatQuestion | None:
    # Pick ending, getting the ending dict key to the ending as well
    ending_components_key, chosen_ending = _pick_ending(filtered_endings)
    chosen_ending = _pick_ending_from_multipleendings(chosen_ending)

    # Using the dict key, create an `EndingComponents`
    ending_components = chosen_word.create_components(ending_components_key)

    # Unsupported endings
    # Subjunctives cannot be translated to English on their own
    verb_subjunctive = (
        isinstance(chosen_word, Verb)
        and ending_components.mood == Mood.SUBJUNCTIVE
    )

    if verb_subjunctive:
        return None

    # Double-up endings
    noun_nom_acc_voc = isinstance(
        chosen_word, Noun
    ) and ending_components.case in {
        Case.NOMINATIVE,
        Case.ACCUSATIVE,
        Case.VOCATIVE,
    }

    adjective_not_adverb_flag = (
        isinstance(chosen_word, Adjective)
        and ending_components.subtype != ComponentsSubtype.ADVERB
    )

    participle_flag = (
        isinstance(chosen_word, Verb)
        and ending_components.subtype == ComponentsSubtype.PARTICIPLE
    )

    verb_second_person_flag = (
        isinstance(chosen_word, Verb)
        and ending_components.subtype
        not in {ComponentsSubtype.INFINITIVE, ComponentsSubtype.PARTICIPLE}
        and ending_components.person == 2
    )

    pronoun_flag = isinstance(chosen_word, Pronoun)

    answers = {chosen_ending}

    # Nominative, vocative, accusative nouns translate the same way
    # NOTE: Might change later? Give accusative nouns a separate meaning
    if noun_nom_acc_voc:
        endings_to_add = (
            chosen_word.get(
                case=Case.NOMINATIVE, number=ending_components.number
            ),
            chosen_word.get(
                case=Case.ACCUSATIVE, number=ending_components.number
            ),
            chosen_word.get(
                case=Case.VOCATIVE, number=ending_components.number
            ),
        )
        for ending in filter(None, endings_to_add):
            if isinstance(ending, str):
                answers.add(ending)
            else:
                assert isinstance(ending, MultipleEndings)
                answers.update(ending.get_all())

    # Adjectives all translate the same if they have the same degree
    elif adjective_not_adverb_flag:
        answers = {
            item
            for key, value in chosen_word.endings.items()
            if key.startswith("A")
            and key[1:4] == ending_components.degree.shorthand  # same degree
            for item in (  # unpack `MultipleEndings`
                value.get_all()
                if isinstance(value, MultipleEndings)
                else [value]
            )
        }

        chosen_ending = str(  # __str__ returns main ending
            chosen_word.get(
                case=Case.NOMINATIVE,
                number=Number.SINGULAR,
                gender=Gender.MASCULINE,
                degree=ending_components.degree,
            )
        )

    # All participles translate the same way
    elif participle_flag:
        answers = {
            item
            for key, value in chosen_word.endings.items()
            if key[7:10] == Mood.PARTICIPLE.shorthand
            for item in (  # unpack `MultipleEndings`
                value.get_all()
                if isinstance(value, MultipleEndings)
                else [value]
            )
        }

        chosen_ending = str(  # __str__ returns main ending
            chosen_word.get(
                tense=ending_components.tense,
                voice=ending_components.voice,
                mood=Mood.PARTICIPLE,
                number=Number.SINGULAR,
                participle_case=Case.NOMINATIVE,
                participle_gender=Gender.MASCULINE,
            )
        )

    # English doesn't have 2nd person plural, so it's the same as singular
    elif verb_second_person_flag:
        if second_person_plural := chosen_word.get(
            tense=ending_components.tense,
            voice=ending_components.voice,
            mood=ending_components.mood,
            number=Number.PLURAL,
            person=2,
        ):
            if isinstance(second_person_plural, MultipleEndings):
                temp_second_person_plural = tuple(
                    second_person_plural.get_all()
                )
            else:
                temp_second_person_plural = (second_person_plural,)

            answers = {
                chosen_ending,  # second person singular
                *temp_second_person_plural,
            }
        else:
            answers = {chosen_ending}

    # All pronouns translate the same way if same case and number
    elif pronoun_flag:

        @overload
        def _convert_to_tuple(ending: Ending) -> tuple[str, ...]: ...
        @overload
        def _convert_to_tuple(ending: None) -> tuple[None]: ...

        def _convert_to_tuple(
            ending: Ending | None,
        ) -> tuple[str, ...] | tuple[None]:
            if ending is None:
                return ()

            if isinstance(ending, MultipleEndings):
                return tuple(ending.get_all())

            return (ending,)

        answers = {
            *_convert_to_tuple(
                chosen_word.get(
                    case=ending_components.case,
                    number=ending_components.number,
                    gender=Gender.MASCULINE,
                )
            ),
            *_convert_to_tuple(
                chosen_word.get(
                    case=ending_components.case,
                    number=ending_components.number,
                    gender=Gender.FEMININE,
                )
            ),
            *_convert_to_tuple(
                chosen_word.get(
                    case=ending_components.case,
                    number=ending_components.number,
                    gender=Gender.NEUTER,
                )
            ),
        }

        chosen_ending = str(
            chosen_word.get(
                case=ending_components.case,
                number=ending_components.number,
                gender=Gender.MASCULINE,
            )
        )

    # Determine meaning
    raw_meaning = str(chosen_word.meaning)  # __str__ returns main ending
    inflected_meaning = set_choice(
        find_inflection(raw_meaning, components=ending_components)
    )

    return TypeInEngToLatQuestion(
        prompt=inflected_meaning, main_answer=chosen_ending, answers=answers
    )


def _generate_typein_lattoeng(
    chosen_word: _Word, filtered_endings: Endings
) -> TypeInLatToEngQuestion | None:
    # Pick ending
    _, chosen_ending = _pick_ending(filtered_endings)
    chosen_ending = _pick_ending_from_multipleendings(chosen_ending)

    # Find all possible `EndingComponents` for the ending
    # e.g. 'puellae' could be 'girls' or 'of the girl'
    all_ending_components = chosen_word.find(chosen_ending)
    possible_main_answers: set[str] = set()
    inflected_meanings: set[str] = set()

    for ending_components in all_ending_components:
        verb_subjunctive = (
            isinstance(chosen_word, Verb)
            and ending_components.mood == Mood.SUBJUNCTIVE
        )

        # Subjunctives cannot be translated to English on their own
        if verb_subjunctive:
            continue

        # Find uninflected meanings
        raw_meaning = chosen_word.meaning
        if isinstance(raw_meaning, MultipleMeanings):
            main_meaning = str(raw_meaning)  # __str__ returns the main meaning
            meanings = set(raw_meaning.meanings)
        else:
            main_meaning = raw_meaning
            meanings = {raw_meaning}

        # Inflect meanings
        for meaning in meanings:
            inflected_meanings.update(
                find_inflection(meaning, components=ending_components)
            )

        possible_main_answers.add(
            find_inflection(
                main_meaning, components=ending_components, main=True
            )
        )

    # If the loop went to `continue` every time (i.e. the ending was subjunctive)
    if not possible_main_answers:
        return None

    # Pick a main answer
    main_answer = set_choice(possible_main_answers)

    return TypeInLatToEngQuestion(
        prompt=chosen_ending,
        main_answer=main_answer,
        answers=inflected_meanings,
    )


def _generate_parse(
    chosen_word: _Word, filtered_endings: Endings
) -> ParseWordLatToCompQuestion | None:
    # `RegularWord` is not supported (cannot be declined)
    if isinstance(chosen_word, RegularWord):
        return None

    # Pick ending
    _, chosen_ending = _pick_ending(filtered_endings)
    chosen_ending = _pick_ending_from_multipleendings(chosen_ending)

    # Find possible `EndingComponents`
    all_ending_components = set(chosen_word.find(chosen_ending))

    # Pick main ending components
    main_ending_components = set_choice(all_ending_components)

    return ParseWordLatToCompQuestion(
        prompt=chosen_ending,
        main_answer=main_ending_components,
        answers=all_ending_components,
        dictionary_entry=str(chosen_word),  # __str__ returns dictionary entry
    )


def _generate_inflect(
    chosen_word: _Word, filtered_endings: Endings
) -> ParseWordCompToLatQuestion | None:
    # `RegularWord` is not supported (cannot be declined)
    if isinstance(chosen_word, RegularWord):
        return None

    # Pick ending, getting the ending dict key to the ending as well
    ending_components_key, chosen_ending = _pick_ending(filtered_endings)

    # Find `EndingComponents` from dict key
    ending_components = chosen_word.create_components(ending_components_key)

    # Convert `chosen_ending` to string if necessary
    if isinstance(chosen_ending, MultipleEndings):
        # If the `MutipleEndings` has a `regular` attribute then use that
        if hasattr(chosen_ending, "regular"):
            main_answer = chosen_ending.regular
        else:
            main_answer = random.choice(chosen_ending.get_all())
        answers = set(chosen_ending.get_all())
    else:
        main_answer = chosen_ending
        answers = {chosen_ending}

    return ParseWordCompToLatQuestion(
        prompt=str(chosen_word),  # __str__ returns dictionary entry
        components=ending_components,
        main_answer=main_answer,
        answers=answers,
    )


def _generate_principal_parts_question(
    chosen_word: _Word,
) -> PrincipalPartsQuestion | None:
    # `RegularWord` is not supported (not principal parts)
    if isinstance(chosen_word, RegularWord):
        return None

    # Get principal parts
    principal_parts: tuple[str, ...]
    match chosen_word:
        case Verb():
            if chosen_word.conjugation == 0:  # irregular verb
                return None

            assert chosen_word.infinitive is not None
            assert chosen_word.perfect is not None

            if chosen_word.ppp:
                assert chosen_word.ppp is not None

                principal_parts = (
                    chosen_word.present,
                    chosen_word.infinitive,
                    chosen_word.perfect,
                    chosen_word.ppp,
                )
            else:
                principal_parts = (
                    chosen_word.present,
                    chosen_word.infinitive,
                    chosen_word.perfect,
                )

        case Noun():
            if chosen_word.declension == 0:  # irregular noun
                return None

            assert chosen_word.genitive is not None

            principal_parts = (chosen_word.nominative, chosen_word.genitive)

        case Adjective():
            match chosen_word.declension:
                case "212":
                    principal_parts = (
                        chosen_word.mascnom,
                        chosen_word.femnom,
                        chosen_word.neutnom,
                    )
                case "3":
                    match chosen_word.termination:
                        case 1:
                            principal_parts = (
                                chosen_word.mascnom,
                                chosen_word.mascgen,
                            )
                        case 2:
                            principal_parts = (
                                chosen_word.mascnom,
                                chosen_word.neutnom,
                            )
                        case 3:
                            principal_parts = (
                                chosen_word.mascnom,
                                chosen_word.femnom,
                                chosen_word.neutnom,
                            )

        case Pronoun():
            principal_parts = (
                chosen_word.mascnom,
                chosen_word.femnom,
                chosen_word.neutnom,
            )

        case _:
            raise TypeError(f"Invalid type: {type(chosen_word)}")

    return PrincipalPartsQuestion(
        prompt=principal_parts[0], principal_parts=principal_parts
    )


def _generate_multiplechoice_engtolat(
    vocab_list: Vocab, chosen_word: _Word, number_multiplechoice_options: int
) -> MultipleChoiceEngToLatQuestion:
    # Remove `chosen_word` from copy of `vocab_list`
    vocab_list = vocab_list.copy()  # sourcery skip: name-type-suffix
    vocab_list.remove(chosen_word)

    # Get a single meaning if it is `MultipleMeanings`
    meaning = chosen_word.meaning
    if isinstance(meaning, MultipleMeanings):
        meaning = random.choice(meaning.meanings)

    # Find answer and other choices
    answer = chosen_word._first  # noqa: SLF001
    other_choices = (
        vocab._first  # noqa: SLF001
        for vocab in random.sample(
            vocab_list,
            # minus one as the chosen word is already in the question
            number_multiplechoice_options - 1,
        )
    )

    # Put together choices
    choices = [answer, *other_choices]
    random.shuffle(choices)

    return MultipleChoiceEngToLatQuestion(
        prompt=meaning, answer=answer, choices=tuple(choices)
    )


def _generate_multiplechoice_lattoeng(
    vocab_list: Vocab, chosen_word: _Word, number_multiplechoice_options: int
) -> MultipleChoiceLatToEngQuestion:
    prompt = chosen_word._first  # noqa: SLF001

    # Pick correct choice
    if isinstance(chosen_word.meaning, MultipleMeanings):
        chosen_word_meanings = tuple(chosen_word.meaning.meanings)
    else:
        chosen_word_meanings = (chosen_word.meaning,)

    answer = random.choice(chosen_word_meanings)

    # Pick other possible choices
    possible_choices: list[str] = []
    for vocab in vocab_list:
        current_meaning = vocab.meaning
        if isinstance(current_meaning, str):
            if current_meaning in chosen_word_meanings:
                continue
            possible_choices.append(current_meaning)
        else:
            possible_choices.extend(
                meaning
                for meaning in current_meaning.meanings
                if meaning not in chosen_word_meanings
            )
    choices = [
        answer,
        *random.sample(possible_choices, number_multiplechoice_options - 1),
    ]
    random.shuffle(choices)

    return MultipleChoiceLatToEngQuestion(
        prompt=prompt, answer=answer, choices=tuple(choices)
    )
