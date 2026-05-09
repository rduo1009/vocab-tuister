from typing import TYPE_CHECKING

from ...pb.vocab_tuister.v1 import ParseWordLatToCompQuestion
from ..accido.endings import RegularWord
from ._pb_convert import ending_components_pb
from ._utils import pick_ending, pick_ending_from_multipleendings

if TYPE_CHECKING:
    from ..accido.endings import Word
    from ..accido.type_aliases import Endings


def generate_parseword_lattocomp(
    chosen_word: Word, filtered_endings: Endings
) -> ParseWordLatToCompQuestion | None:
    # `RegularWord` is not supported (cannot be declined)
    if isinstance(chosen_word, RegularWord):
        return None

    # Pick ending
    _, chosen_ending = pick_ending(filtered_endings)
    chosen_ending = pick_ending_from_multipleendings(chosen_ending)

    # Find possible `EndingComponents`
    all_ending_components = set(chosen_word.find(chosen_ending))

    # Pick main ending components
    main_ending_components = max(all_ending_components)

    return ParseWordLatToCompQuestion(
        prompt=chosen_ending,
        main_answer=ending_components_pb(main_ending_components),
        answers=[ending_components_pb(ec) for ec in all_ending_components],
        dictionary_entry=str(chosen_word),  # __str__ returns dictionary entry
    )
