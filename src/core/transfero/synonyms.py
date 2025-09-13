"""Contains a function that finds synonyms of English words."""

# pyright: reportUnusedCallResult=false

from __future__ import annotations

import logging
import sys as _sys
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Final, cast

import wn
from wn.constants import ADJECTIVE, NOUN, VERB

from ..accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb

if TYPE_CHECKING:
    from ..accido.endings import _Word

logger = logging.getLogger(__name__)

_LEXICON: Final[str] = "oewn:2024"


def _wn_is_installed(name: str) -> bool:
    return name in [f"{lex.id}:{lex.version}" for lex in wn.lexicons()]


# Frozen with PyInstaller
if getattr(_sys, "frozen", False) and hasattr(
    _sys, "_MEIPASS"
):  # pragma: no cover
    # NOTE: Should work, but type narrowing not implemented
    # See https://github.com/DetachHead/basedpyright/issues/1224
    _wn_data_path = Path(cast("str", _sys._MEIPASS)) / "wn_data"  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]
    wn.config.data_directory = str(_wn_data_path)
    if not _wn_data_path.exists() or not _wn_is_installed(_LEXICON):
        raise LookupError(
            "The wordnet dataset was not found in the package data."
        )

# Regular usage
else:
    _wn_data_path = Path(__file__).parent / "wn_data"
    _wn_data_path.mkdir(parents=True, exist_ok=True)
    wn.config.data_directory = str(_wn_data_path)
    if not _wn_is_installed(_LEXICON):
        try:
            wn.download(_LEXICON)
            warnings.warn(
                f"The wordnet lexicon '{_LEXICON}' was not found in {_wn_data_path} "
                "and has been downloaded.",
                stacklevel=2,
            )
        except Exception as e:
            raise LookupError(
                "Could not download or load the wordnet lexicon."
            ) from e


# Mapping from word classes to WordNet POS tags.
# Adjectives use both 'a' (adjective) and 's' (satellite adjective) for comprehensive search.
# RegularWord has no specific POS, so searches all.
POS_TABLE: Final[dict[type[_Word], tuple[str, ...] | None]] = {
    Noun: (NOUN,),
    Pronoun: (NOUN,),
    Verb: (VERB,),
    Adjective: (ADJECTIVE, "s"),
    RegularWord: None,
}


def _get_synsets(
    ewn: wn.Wordnet, word: str, pos: type[_Word] | None = None
) -> list[wn.Synset]:
    # Check if a part of speech (POS) is provided.
    if pos:
        # Retrieve the corresponding WordNet POS tags from the POS_TABLE mapping.
        pos_tags = POS_TABLE[pos]
        # If there are specific POS tags for the given word type...
        if pos_tags:
            # ...return a list of synsets by searching for the word with each of the specified POS tags.
            # This handles cases like adjectives which can be 'a' or 's'.
            return [
                ss
                for pos_tag in pos_tags
                for ss in ewn.synsets(word, pos=pos_tag)
            ]

        # If pos_tags is None (e.g., for RegularWord), it means we should search across all parts of speech.
        # Fallthrough to search all POS.
        return ewn.synsets(word)
    # If no POS is specified at all, search for the word across all parts of speech.
    return ewn.synsets(word)


def _filter_synsets_by_known(
    synsets: list[wn.Synset], known_synonyms: tuple[str, ...]
) -> list[wn.Synset]:
    # If no known synonyms are provided for disambiguation, return the original list of synsets.
    if not known_synonyms:
        return synsets

    # Helper function to check if a lemma from a synset matches any of the known synonyms.
    def _lemma_matches(lemma: str) -> bool:
        # Normalize the lemma by converting to lowercase and replacing underscores with spaces for comparison.
        normalized = lemma.lower().replace("_", " ")
        # Check if the normalized lemma is present in the list of known synonyms.
        return normalized in known_synonyms

    # Filter the list of synsets. A synset is kept if it contains at least one lemma
    # that matches any of the provided known synonyms.
    filtered = [
        synset
        for synset in synsets
        if any(_lemma_matches(lemma) for lemma in synset.lemmas())
    ]
    # If the filtering results in an empty list (no matches found),
    # return the original unfiltered list of synsets as a fallback.
    # This ensures that we still get some results even if the known synonyms don't match perfectly.
    return filtered or synsets


def _add_lemmas_to_set(
    synset: wn.Synset, synonyms_set: set[str], exclude_word: str
) -> None:
    # Iterate over all lemmas (words) in the given synset.
    for lemma in synset.lemmas():
        # Normalize the lemma by converting it to lowercase and replacing underscores with spaces.
        normalized = lemma.lower().replace("_", " ")
        # Ensure the original word is not added to its own set of synonyms.
        if normalized != exclude_word:
            # Add the normalized lemma to the set of synonyms.
            synonyms_set.add(normalized)


def find_synonyms(
    word: str,
    *,
    pos: type[_Word] | None = None,
    include_similar_words: bool = False,
    known_synonyms: tuple[str, ...] = (),
) -> set[str]:
    """Find synonyms and optionally related words of a word.

    Parameters
    ----------
    word : str
        The word to find synonyms of.
    pos : type[_Word] | None
        The part of speech of the word. If ``None``, then the synonyms
        of all parts of speech are returned.
    include_similar_words : bool, optional
        Whether to include related words in the search (similar, hypernyms,
        hyponyms). Defaults to False.
    known_synonyms : tuple[str, ...], optional
        Additional known synonyms of the word to help disambiguate its sense.
        If provided, only synsets that contain at least one of these as a lemma
        will be used to find synonyms. If no such synset is found, falls back
        to all synsets.

    Returns
    -------
    set[str]
        The synonyms (and optionally related terms).
    """
    # Log the function call with its arguments for debugging purposes.
    logger.debug(
        "find_synonyms(word=%r, pos=%s, include_similar_words=%s, known_synonyms=%s)",
        word,
        pos,
        include_similar_words,
        known_synonyms,
    )

    # Initialize the WordNet instance using the pre-configured lexicon.
    ewn = wn.Wordnet(_LEXICON)
    # Retrieve the initial list of synsets for the given word and part of speech.
    synsets = _get_synsets(ewn, word, pos)
    # If known synonyms are provided, filter the synsets to only include those
    # that are relevant to the given sense of the word.
    synsets = _filter_synsets_by_known(synsets, known_synonyms)

    # Create an empty set to store the collected synonyms.
    synonyms: set[str] = set()
    # Iterate over the filtered list of synsets.
    for synset in synsets:
        # Add all lemmas from the current synset to the synonyms set, excluding the original word.
        _add_lemmas_to_set(synset, synonyms, word.lower())

        # If the option to include similar words is enabled, expand the search.
        if include_similar_words:
            # Add lemmas from synsets that are "similar to" the current synset.
            for similar_synset in synset.get_related("similar"):
                _add_lemmas_to_set(similar_synset, synonyms, word.lower())
            # Add lemmas from hypernyms (more general concepts).
            for hypernym in synset.hypernyms():
                _add_lemmas_to_set(hypernym, synonyms, word.lower())
            # Add lemmas from hyponyms (more specific concepts).
            for hyponym in synset.hyponyms():
                _add_lemmas_to_set(hyponym, synonyms, word.lower())

    # Log the final set of synonyms before returning.
    logger.debug("Synonyms: %s", synonyms)

    # Return the complete set of synonyms.
    return synonyms
