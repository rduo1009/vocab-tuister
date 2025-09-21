"""Contains a function that finds synonyms of English words."""

# TODO: This module won't be used if the user settings don't enable them.
# So put this import inside a if block to speed up import time

# pyright: reportUnusedCallResult=false

from __future__ import annotations

import logging
import lzma
import sys as _sys
import warnings
from functools import cache
from pathlib import Path
from shutil import copyfileobj
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Any, Final, cast

import wn
from wn.constants import ADJECTIVE, NOUN, VERB

from ..accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb

if TYPE_CHECKING:
    from ..accido.endings import Word

logger = logging.getLogger(__name__)


def _wn_is_installed(name: str) -> bool:
    try:
        return bool(wn.lexicons(lexicon=name))
    except wn.DatabaseError:
        return False


wn.config.allow_multithreading = True
_LEXICON: Final[str] = "oewn:2024"

_trimmed_wn = False

# Frozen with PyInstaller
if getattr(_sys, "frozen", False) and hasattr(_sys, "_MEIPASS"):
    # NOTE: Should work, but type narrowing not implemented
    # See https://github.com/DetachHead/basedpyright/issues/1224
    _wn_data_path = (
        Path(cast("str", _sys._MEIPASS)) / "src/core/transfero/wn_data"  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]
    )
    wn.config.data_directory = str(_wn_data_path)

    if (compressed_db_path := _wn_data_path / "wn.db.xz").exists():
        with (
            lzma.open(compressed_db_path, "rb") as f_in,
            (_wn_data_path / "wn.db").open("wb") as f_out,
        ):
            copyfileobj(f_in, f_out)

    if not _wn_data_path.exists():
        raise LookupError(
            "The wordnet dataset was not found in the package data."
        )

    # The database will always be trimmed in frozen builds
    _trimmed_wn = True

# Regular usage
else:
    # This is the primary, persistent data directory in your project
    _wn_data_path = Path(__file__).parent / "wn_data"
    _wn_data_path.mkdir(parents=True, exist_ok=True)

    # 1. Check if the compressed database exists.
    if (compressed_db_path := _wn_data_path / "wn.db.xz").exists():
        # Decompress into a temporary directory.
        _tmp_dir_obj = TemporaryDirectory()
        _wn_data_path = Path(_tmp_dir_obj.name)

        with (
            lzma.open(compressed_db_path, "rb") as f_in,
            (_wn_data_path / "wn.db").open("wb") as f_out,
        ):
            copyfileobj(f_in, f_out)

        wn.config.data_directory = str(_wn_data_path)

    # 2. If not, check for an existing uncompressed database.
    elif (uncompressed_db_path := _wn_data_path / "wn.db").exists():
        # Use the existing persistent directory directly.
        wn.config.data_directory = str(_wn_data_path)

    # 3. If neither exists, download a fresh copy.
    else:
        # Download will go into the persistent directory.
        wn.config.data_directory = str(_wn_data_path)
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

    # Now, regardless of the path taken, check if the loaded DB is trimmed.
    if not _wn_is_installed(_LEXICON):
        _trimmed_wn = True

if _trimmed_wn:
    from wn import _db  # noqa: PLC2701

    def _do_nothing( 
        *args: Any, **kwargs: Any,  # noqa: ARG001 # pyright: ignore[reportExplicitAny, reportAny, reportUnusedParameter]
    ) -> None:  # fmt: skip
        return

    # Monkeypatch wordnet validation, as the hash will be different
    _db._check_schema_compatibility = _do_nothing  # noqa: SLF001

# Mapping from word classes to WordNet POS tags.
# Adjectives use both 'a' (adjective) and 's' (satellite adjective) for comprehensive search.
# RegularWord has no specific POS, so searches all.
POS_TABLE: Final[dict[type[Word], tuple[str, ...] | None]] = {
    Noun: (NOUN,),
    Pronoun: (NOUN,),
    Verb: (VERB,),
    Adjective: (ADJECTIVE, "s"),
    RegularWord: None,
}


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


@cache
def find_synonyms(
    word: str,
    *,
    pos: type[Word] | None = None,
    known_synonyms: tuple[str, ...] = (),
    include_similar_words: bool = False,
) -> set[str]:
    """Find synonyms and optionally related words of a word.

    Parameters
    ----------
    word : str
        The word to find synonyms of.
    pos : type[Word] | None
        The part of speech of the word. If ``None``, then the synonyms
        of all parts of speech are returned.
    known_synonyms : tuple[str, ...], optional
        Additional known synonyms of the word to help disambiguate its sense.
        If provided, only synsets that contain at least one of these as a lemma
        will be used to find synonyms. If no such synset is found, falls back
        to all synsets.
    include_similar_words : bool, optional
        Whether to include related words in the search (similar, hypernyms,
        hyponyms). Defaults to False.

    Returns
    -------
    set[str]
        The synonyms (and optionally related terms).
    """
    # Log the function call with its arguments for debugging purposes.
    logger.debug(
        "find_synonyms(word=%r, pos=%s, known_synonyms=%s, include_similar_words=%s)",
        word,
        pos,
        known_synonyms,
        include_similar_words,
    )

    # Initialize the WordNet instance using the pre-configured lexicon.
    ewn = wn.Wordnet(_LEXICON)

    # Retrieve the initial list of synsets for the given word and part of speech.
    # Check if a part of speech (POS) is provided.
    if pos:
        # Retrieve the corresponding WordNet POS tags from the POS_TABLE mapping.
        pos_tags = POS_TABLE[pos]
        # If there are specific POS tags for the given word type...
        if pos_tags:
            # ...return a list of synsets by searching for the word with each of the specified POS tags.
            # This handles cases like adjectives which can be 'a' or 's'.
            synsets = [
                ss
                for pos_tag in pos_tags
                for ss in ewn.synsets(word, pos=pos_tag)
            ]
        else:
            # If pos_tags is None (e.g., for RegularWord), it means we should search across all parts of speech.
            # Fallthrough to search all POS.
            synsets = ewn.synsets(word)
    # If no POS is specified at all, search for the word across all parts of speech.
    else:
        synsets = ewn.synsets(word)

    # If known synonyms are provided, filter the synsets to only include those
    # that are relevant to the given sense of the word.
    # If no known synonyms are provided for disambiguation, return the original list of synsets.
    if known_synonyms:
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
        synsets = filtered or synsets

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
