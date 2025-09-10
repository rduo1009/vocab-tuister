"""Contains a function that finds synonyms of English words."""

# pyright: reportUnusedCallResult=false

from __future__ import annotations

import logging
import sys as _sys
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Final

from nltk import download
from nltk.corpus import wordnet
from nltk.data import find, path

from ..accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb

if TYPE_CHECKING:
    from ..accido.endings import _Word

logger = logging.getLogger(__name__)

_project_root = Path(__file__).parent.parent.parent.parent

# Frozen with PyInstaller
if getattr(_sys, "frozen", False) and hasattr(
    _sys, "_MEIPASS"
):  # pragma: no cover
    import pkgutil

    _nltk_data_path = (
        _project_root / "src" / "core" / "transfero" / "nltk_data"
    )

    # Read nltk corpora from package data
    data = pkgutil.get_data(
        "src.core.transfero", "nltk_data/corpora/wordnet.zip"
    )
    if data is None:
        raise LookupError(
            "The wordnet dataset was not found in the package data."
        )

    # Write nltk corpora in provided temporary directory
    Path(_nltk_data_path / "corpora" / "wordnet.zip").write_bytes(data)

# Regular usage
else:
    _nltk_data_path = _project_root / "nltk_data"

_nltk_data_path.mkdir(parents=True, exist_ok=True)
path.append(str(_nltk_data_path))

try:
    find("corpora/wordnet.zip")
except LookupError:
    download("wordnet", download_dir=str(_nltk_data_path))
    warnings.warn(
        f"The wordnet dataset was not found in {_nltk_data_path} and has "
        "been downloaded",
        stacklevel=2,
    )

del find, download, path

POS_TABLE: Final[dict[type[_Word], str | None]] = {
    Noun: wordnet.NOUN,
    Pronoun: wordnet.NOUN,
    Verb: wordnet.VERB,
    Adjective: wordnet.ADJ,
    RegularWord: None,
}


def find_synonyms(
    word: str,
    *,
    pos: type[_Word] | None = None,
    include_similar_words: bool = False,
    known_synonyms: tuple[str, ...] = (),
) -> set[str]:
    """Find synonyms of a word.

    Parameters
    ----------
    word : str
        The word to find synonyms of.
    pos : type[_Word] | None
        The part of speech of the word. If ``None``, then the synonyms
        of all parts of speech are returned.
    include_similar_words : bool, optional
        Whether to include similar words in the search, by default False.
        This leverages WordNet's 'similar to' relationships, often useful
        for adjectives (e.g., finding 'massive' as similar to 'big') or
        other related terms that aren't strict synonyms.
    known_synonyms : tuple[str, ...], optional
        Additional known synonyms of the word to help disambiguate its sense.
        If provided, only synsets that contain at least one of these as a lemma
        will be used to find synonyms. If no such synset is found, falls back
        to all synsets.
        Defaults to ().

    Returns
    -------
    set[str]
        The synonyms of the word.
    """
    logger.debug(
        "find_synonyms(word=%r, pos=%s, include_similar_words=%s, known_synonyms=%s)",
        word,
        pos,
        include_similar_words,
        known_synonyms,
    )

    synonyms: set[str] = set()

    # Get all synsets for the word with the given POS tag
    synsets = wordnet.synsets(word, pos=POS_TABLE[pos] if pos else None)

    # Filter synsets based on known_synonyms if provided
    if known_synonyms:
        filtered_synsets = [
            synset
            for synset in synsets
            if any(
                lemma.name().lower().replace("_", " ") in known_synonyms
                for lemma in synset.lemmas()
            )
        ]
        if filtered_synsets:
            synsets = filtered_synsets

    for synset in synsets:
        # Add lemmas from the synset itself
        synonyms.update(
            lemma.name()
            .lower()  # some words are capitalised
            .replace("_", " ")
            for lemma in synset.lemmas()
            if lemma.name().lower() != word
        )

        # Add lemmas from similar_tos synsets if requested
        if include_similar_words:
            for similar_synset in synset.similar_tos():
                synonyms.update(
                    lemma.name().lower().replace("_", " ")
                    for lemma in similar_synset.lemmas()
                    if lemma.name().lower() != word
                )

    logger.debug("Synonyms: %s", synonyms)

    return synonyms
