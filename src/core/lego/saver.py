"""Contains a function for saving vocabulary files."""

# pyright: reportUnusedCallResult=false

from __future__ import annotations

import hashlib
import hmac
import logging
import warnings
import zlib
from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO

import dill as pickle

from .exceptions import MisleadingFilenameWarning
from .misc import KEY

if TYPE_CHECKING:
    from .misc import VocabList

logger = logging.getLogger(__name__)


def save_vocab_dump(
    destination: str | Path | BinaryIO,
    vocab_list: VocabList,
    *,
    compress: bool = False,
) -> None:
    """Save a vocab dump file.

    The pickle files are signed with a HMAC signature to ensure the data
    has not been tampered with.
    The files can also be compressed using gzip. If this is the case, the files
    will be saved with the `.gzip` extension, unless the user has put the
    `.gzip` extension in the file path already.

    Parameters
    ----------
    destination : str | Path | BinaryIO
        The path to the vocab dump file, or a binary writable object.
    vocab_list : VocabList
        The vocab list to save.
    compress : bool
        Whether to compress the pickle file. The default is False.

    Raises
    ------
    FileNotFoundError
        If the directory of the file does not exist.

    Warnings
    --------
    UserWarning
        If the file already exists and has been overwritten.
    MisleadingFilenameWarning
        If the file path does not end in `.gzip` and the file is being
        compressed, or if the file path ends in `.gzip` and the file is
        not being compressed.

    Examples
    --------
    >>> save_vocab_dump(
    ...     Path("path_to_file.pickle"), VocabList()
    ... )  # doctest: +SKIP
    """
    pickled_data = pickle.dumps(vocab_list)
    signature = hmac.new(KEY, pickled_data, hashlib.sha256).hexdigest()

    if not isinstance(destination, (str, Path)):
        if compress:
            logger.info("Saving vocab dump with compression to stream.")
            destination.write(zlib.compress(pickled_data + signature.encode()))
        else:
            logger.info("Saving vocab dump to stream.")
            destination.write(pickled_data)
            destination.write(signature.encode())

        return

    file_path = Path(destination)
    if not file_path.parent.exists():
        raise FileNotFoundError(
            f"The directory '{file_path.parent}' does not exist."
        )

    if file_path.exists():
        warnings.warn(
            f"The file '{file_path}' already exists and has been overwritten.",
            stacklevel=2,
        )

    if compress:
        if file_path.suffix != ".gzip":
            warnings.warn(
                f"The file '{file_path}' is being compressed, "
                "but the '.gzip' extension is not present and is being added.",
                category=MisleadingFilenameWarning,
                stacklevel=2,
            )
            file_path = file_path.with_suffix(f"{file_path.suffix}.gzip")

        logger.info("Saving vocab dump with compression to %s.", file_path)

        with Path(file_path).open("wb") as file:
            file.write(zlib.compress(pickled_data + signature.encode()))
        return

    if file_path.suffix == ".gzip":
        warnings.warn(
            f"The file '{file_path}' is not being compressed, "
            "but the file extension ('.gzip') suggests it is.",
            category=MisleadingFilenameWarning,
            stacklevel=2,
        )

    logger.info("Saving vocab dump to %s.", file_path)

    with file_path.open("wb") as file:
        file.write(pickled_data)
        file.write(signature.encode())
