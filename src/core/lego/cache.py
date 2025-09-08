"""Contains a function for caching vocabulary files in a cache folder."""

from __future__ import annotations

import hashlib
import logging
import warnings
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, TextIO

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
    source: str | Path | TextIO,
    cache_folder: str | Path,
    *,
    compress: bool = False,
) -> tuple[VocabList, bool]:
    """Read a vocab file and save the vocab dump inside a cache folder.

    The name of the vocab dump is decided by hashing the vocab file given. Note
    that if the cache folder does not exist, it is created.

    Parameters
    ----------
    source : str | Path | TextIO
        The path to the vocab file that is to be read, or a text stream.
    cache_folder : str | Path
        The path to the cache folder.
    compress : bool
        Whether to compress the cache file. The default is False.

    Returns
    -------
    VocabList
        The vocab list.
    bool
        Whether the vocab list was created from cache or not.

    Warnings
    --------
    UserWarning
        If the cache folder did not exist and had to be created, or if the
        vocab dump already exists and has been overwritten.
    MisleadingFilenameWarning
        If the file path does not end in `.gzip` and the file is being
        compressed, or if the file path ends in `.gzip` and the file is
        not being compressed.

    Raises
    ------
    InvalidVocabFileFormatError
        If the file provided is not a valid vocab file, or if the formatting is
        incorrect.
    InvalidVocabDumpError
        If the file in the cache is not a valid vocab dump, or if the data has
        been tampered with.
    FileNotFoundError
        If the vocab file or dump does not exist.
    """
    cache_folder = Path(cache_folder)
    if not cache_folder.exists():
        cache_folder.mkdir(parents=True, exist_ok=True)
        warnings.warn(
            f"The directory {cache_folder} did not exist and has been created",
            stacklevel=2,
        )

    if not isinstance(source, (str, Path)):
        # Handle stream source
        content = source.read()
        hasher = hashlib.sha256()
        hasher.update(content.encode("utf-8"))
        cache_hash = hasher.hexdigest()
        cache_file_name = cache_hash + (".gzip" if compress else "")
        cache_path = cache_folder / cache_file_name

        if cache_path.exists():
            logger.info("Cache found for hash %s.", cache_hash)
            return (read_vocab_dump(cache_path), True)

        logger.info("No cache found for hash %s.", cache_hash)
        vocab_list = read_vocab_file(StringIO(content))
        save_vocab_dump(cache_path, vocab_list, compress=compress)
        return (vocab_list, False)

    # Handle file path source
    vocab_file_path = Path(source)
    cache_hash = _sha256sum(vocab_file_path)
    cache_file_name = cache_hash + (".gzip" if compress else "")
    cache_path = cache_folder / cache_file_name

    if cache_path.exists():
        logger.info("Cache found for hash %s.", cache_hash)
        return (read_vocab_dump(cache_path), True)

    logger.info("No cache found for hash %s.", cache_hash)
    vocab_list = read_vocab_file(vocab_file_path)
    save_vocab_dump(cache_path, vocab_list, compress=compress)
    return (vocab_list, False)
