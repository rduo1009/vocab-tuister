"""Contains a function for caching vocabulary files in a cache folder."""

from __future__ import annotations

import hashlib
import logging
import warnings
from pathlib import Path
from typing import TYPE_CHECKING

from .reader import read_vocab_dump, read_vocab_file
from .saver import save_vocab_dump

if TYPE_CHECKING:
    from .misc import VocabList

logger = logging.getLogger(__name__)


def _sha256sum(filename: Path) -> str:
    """Hashes a file.

    Parameters
    ----------
    filename : Path
        The file to hash.

    Returns
    -------
    str
        The hash as a string.

    Notes
    -----
    Code taken from https://stackoverflow.com/a/44873382
    """
    with filename.open("rb", buffering=0) as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def cache_vocab_file(
    cache_folder: Path, vocab_file_path: Path
) -> tuple[VocabList, bool]:
    """Read a vocab file and save the vocab dump inside a cache folder.

    The name of the vocabulary dump file is decided by hashing the
    vocab file given. Note that if the cache folder does not exist,
    it is created.

    Parameters
    ----------
    cache_folder : Path
        The path to the cache folder.
    vocab_file_path : Path
        The path to the vocab file that is to be read.

    Returns
    -------
    VocabList
        The vocab list.
    bool
        Whether the vocab list was generated from cache or not.

    Warnings
    --------
    UserWarning
        If the cache folder did not exist and had to be created, or if the
        vocab dump file already exists and has been overwritten.
    MisleadingFilenameWarning
        If the file path does not end in `.gzip` and the file is being
        compressed, or if the file path ends in `.gzip` and the file is
        not being compressed.

    Raises
    ------
    InvalidVocabFileFormatError
        If the file provided is not a valid vocabulary file, or if the
        formatting is incorrect.
    InvalidVocabDumpError
        If the file in the cache is not a valid vocabulary dump, or if
        the data has been tampered with.
    FileNotFoundError
        If the vocab file or dump does not exist.
    """
    if not cache_folder.exists():
        cache_folder.mkdir(parents=True, exist_ok=True)
        warnings.warn(
            f"The directory {cache_folder} did not exist and has been created",
            stacklevel=2,
        )

    cache_file_name = _sha256sum(vocab_file_path)
    cache_path = Path(cache_folder / cache_file_name)

    if cache_path.exists():
        logger.info("Cache found for hash %s.", cache_file_name)

        return (read_vocab_dump(cache_path), True)

    logger.info("No cache found for hash %s.", cache_file_name)

    vocab_list = read_vocab_file(
        vocab_file_path
    )  # sourcery skip: name-type-suffix
    save_vocab_dump(cache_path, vocab_list)
    return (vocab_list, False)
