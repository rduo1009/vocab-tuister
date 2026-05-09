from typing import TYPE_CHECKING, cast

from ...pb.vocab_tuister.v1 import ParseWordCompToLatQuestion
from ..accido.endings import RegularWord
from ._pb_convert import ending_components_pb
from ._utils import normalise_to_multipleendings, pick_ending

if TYPE_CHECKING:
    from ..accido.endings import Word
    from ..accido.type_aliases import Endings


def generate_parseword_comptolat(
    chosen_word: Word, filtered_endings: Endings
) -> ParseWordCompToLatQuestion | None:
    # `RegularWord` is not supported (cannot be declined)
    if isinstance(chosen_word, RegularWord):
        return None

    # Pick ending, getting the ending dict key to the ending as well
    ending_components_key, chosen_ending = pick_ending(filtered_endings)

    # Find `EndingComponents` from dict key
    ending_components = chosen_word.create_components(ending_components_key)

    # Determine answers
    chosen_ending = normalise_to_multipleendings(chosen_ending)
    assert hasattr(chosen_ending, "regular")  # `regular` attribute must exist
    main_answer = cast("str", chosen_ending.regular)
    answers = set(chosen_ending.get_all())

    return ParseWordCompToLatQuestion(
        prompt=str(chosen_word),  # __str__ returns dictionary entry
        components=ending_components_pb(ending_components),
        main_answer=main_answer,
        answers=list(answers),
    )
