"""Contains a function that finds synonyms of English words."""

from __future__ import annotations

import logging
import sys as _sys
import warnings
from pathlib import Path

from nltk import download
from nltk.corpus import wordnet
from nltk.data import find, path

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


def find_synonyms(word: str) -> set[str]:
    """Find synonyms of a word.

    Parameters
    ----------
    word : str
        The word to find synonyms of.

    Returns
    -------
    set[str]
        The synonyms of the word.
    """
    logger.debug("find_synonyms(%s)", word)

    synonyms: set[str] = set()

    for synset in wordnet.synsets(word):
        synonyms.update(
            lemma.name()
            for lemma in synset.lemmas()
            if lemma.name() != word and "_" not in lemma.name()
        )

    logger.debug("Synonyms: %s", synonyms)

    return synonyms
