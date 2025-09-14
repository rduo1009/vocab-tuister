"""Contains functions that generate questions and check answers."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import logging
import random
from typing import TYPE_CHECKING, Final

from ...utils import set_choice
from ._multiplechoice_engtolat import generate_multiplechoice_engtolat
from ._multiplechoice_lattoeng import generate_multiplechoice_lattoeng
from ._parseword_comptolat import generate_inflect
from ._parseword_lattocomp import generate_parse
from ._principal_parts import generate_principal_parts_question
from ._typein_engtolat import generate_typein_engtolat
from ._typein_lattoeng import generate_typein_lattoeng
from .exceptions import InvalidSettingsError
from .question_classes import QuestionClasses
from .rules import filter_endings, filter_questions, filter_words

if TYPE_CHECKING:
    from collections.abc import Iterable

    from ..lego.misc import VocabList
    from .question_classes import Question
    from .type_aliases import Settings

logger = logging.getLogger(__name__)

MAX_RETRIES: Final[int] = 1000


def ask_question_without_sr(
    vocab_list: VocabList, amount: int, settings: Settings
) -> Iterable[Question]:
    """Ask a question about Latin vocabulary.

    Parameters
    ----------
    vocab_list : VocabList
        The vocab list to use.
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

    if not filtered_vocab:
        raise InvalidSettingsError(
            "No words in the vocab list after filtering."
        )

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
                    output = generate_typein_engtolat(
                        chosen_word,
                        filtered_endings,
                        english_subjunctives=settings["english-subjunctives"],
                        english_verbal_nouns=settings["english-verbal-nouns"],
                    )

                case QuestionClasses.TYPEIN_LATTOENG:
                    output = generate_typein_lattoeng(
                        chosen_word,
                        filtered_endings,
                        english_subjunctives=settings["english-subjunctives"],
                        english_verbal_nouns=settings["english-verbal-nouns"],
                    )

                case QuestionClasses.PARSEWORD_LATTOCOMP:
                    output = generate_parse(chosen_word, filtered_endings)

                case QuestionClasses.PARSEWORD_COMPTOLAT:
                    output = generate_inflect(chosen_word, filtered_endings)

                case QuestionClasses.PRINCIPAL_PARTS:
                    output = generate_principal_parts_question(chosen_word)

                case QuestionClasses.MULTIPLECHOICE_ENGTOLAT:
                    output = generate_multiplechoice_engtolat(
                        filtered_vocab,
                        chosen_word,
                        settings["number-multiplechoice-options"],
                    )

                case QuestionClasses.MULTIPLECHOICE_LATTOENG:
                    output = generate_multiplechoice_lattoeng(
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
