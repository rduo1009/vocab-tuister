"""Contains functions for reading vocab files."""

from __future__ import annotations

import gzip
import hashlib
import hmac
import logging
import warnings
from io import StringIO
from pathlib import Path
from re import match
from typing import TYPE_CHECKING, BinaryIO, Literal, TextIO, cast

import dill as pickle

import src

from ..accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb
from ..accido.misc import Gender, MultipleMeanings
from ..accido.type_aliases import is_termination
from .exceptions import InvalidVocabDumpError, InvalidVocabFileFormatError
from .misc import KEY, VocabList

if TYPE_CHECKING:
    from ..accido.endings import _Word
    from ..accido.type_aliases import Meaning

logger = logging.getLogger(__name__)


def read_vocab_dump(source: str | Path | BinaryIO) -> VocabList:
    """Read a vocab dump file and return a ``VocabList`` object.

    The pickle files are signed with a HMAC signature to ensure the data
    has not been tampered with. If the data is invalid, an exception is
    raised.
    If the file ends in `.gzip`, the file is decompressed using gzip.

    Parameters
    ----------
    source : str | Path | BinaryIO
        The path to the vocab dump, or a binary readable object.

    Returns
    -------
    VocabList
        The vocab list generated from the vocab dump.

    Raises
    ------
    InvalidVocabDumpError
        If the file is not a valid vocab dump, or if the data has been
        tampered with.
    FileNotFoundError
        If the file does not exist.

    Examples
    --------
    >>> read_vocab_dump(Path("path_to_file.pickle"))  # doctest: +SKIP
    """
    if isinstance(source, (str, Path)):
        filename = Path(source)
        if filename.suffix == ".gzip":
            logger.info("File %s is being decompressed and read.", filename)

            with gzip.open(filename, "rb") as file:
                content = file.read()
        else:
            logger.info("File %s being read.", filename)

            content = filename.read_bytes()
    else:
        content = source.read()

    pickled_data = content[:-64]
    signature = content[-64:].decode()

    if hmac.new(KEY, pickled_data, hashlib.sha256).hexdigest() != signature:
        raise InvalidVocabDumpError(
            "Data integrity check failed for vocab dump."
        )

    raw_data = pickle.loads(pickled_data)
    if isinstance(raw_data, VocabList):
        if raw_data.version == src.__version__:
            return raw_data

        warnings.warn(
            "Vocab dump is from a different version of vocab-tester.",
            stacklevel=2,
        )
        return read_vocab_file(StringIO(raw_data.vocab_list_text))

    raise InvalidVocabDumpError("Vocab dump is not valid.")


type _PartOfSpeech = Literal[  # pragma: no mutate
    "Verb", "Adjective", "Noun", "Regular", "Pronoun"  # pragma: no mutate
]


def _is_typeofspeech(x: str) -> bool:
    return x in {"Verb", "Adjective", "Noun", "Regular", "Pronoun"}


def _generate_meaning(meaning: str) -> Meaning:
    if "/" in meaning:
        return MultipleMeanings(tuple(x.strip() for x in meaning.split("/")))
    return meaning


def read_vocab_file(source: str | Path | TextIO) -> VocabList:
    """Read a vocab file and return a ``VocabList`` object.

    Parameters
    ----------
    source : str | Path | TextIO
        The path to the vocab file, or any readable object (e.g. an opened
        file).

    Returns
    -------
    VocabList
        The vocab list generated from the file.

    Raises
    ------
    InvalidVocabFileFormatError
        If the file is not a valid vocab file, or if the formatting is
        incorrect.
    FileNotFoundError
        If the file does not exist.
    InvalidVocabListError
        If the vocab list created from the file is invalid.

    Examples
    --------
    >>> read_vocab_file(Path("path_to_file.txt"))  # doctest: +SKIP
    """
    if isinstance(source, (str, Path)):
        with Path(source).open("r", encoding="utf-8") as f:
            contents = f.read()
    else:
        contents = source.read()

    vocab: list[_Word] = []
    current: _PartOfSpeech | Literal[""] = ""

    for line in (
        raw_line.strip()  # remove whitespace
        for raw_line in contents.split("\n")  # for line in file
        if raw_line.strip()  # but skip if the line is blank
    ):
        logger.debug("Reading line '%s'", line)

        match line[0]:
            case "#":
                continue

            case "@":
                match line[1:].strip():
                    case "Verb" | "Adjective" | "Noun" | "Regular" | "Pronoun":
                        assert _is_typeofspeech(line[1:].strip())
                        current = cast("_PartOfSpeech", line[1:].strip())

                    case (
                        "Verbs"
                        | "Adjectives"
                        | "Nouns"
                        | "Regulars"
                        | "Pronouns"
                    ):
                        assert _is_typeofspeech(line[1:-1].strip())
                        current = cast("_PartOfSpeech", line[1:-1].strip())

                    case _:
                        raise InvalidVocabFileFormatError(
                            f"Invalid part of speech: '{line[1:].strip()}'"
                        )

            case _:
                parts = line.split(":")
                if len(parts) != 2:
                    raise InvalidVocabFileFormatError(
                        f"Invalid line format: '{line}'"
                    )

                meaning = _generate_meaning(parts[0].strip())
                latin_parts = [
                    raw_part.strip() for raw_part in parts[1].split(",")
                ]

                if not current:
                    raise InvalidVocabFileFormatError(
                        "Part of speech was not given."
                    )

                vocab.append(_parse_line(current, latin_parts, meaning, line))

    return VocabList(vocab, str(contents))


def _parse_line(
    current: _PartOfSpeech, latin_parts: list[str], meaning: Meaning, line: str
) -> _Word:
    """Create a word object from a line of a vocab file and the pos.

    Parameters
    ----------
    current : _PartOfSpeech
        The part of speech of the word object.
    latin_parts : list[str]
        The split parts of the word definition in the vocab file.
    meaning : Meaning
        The meaning of the word.
    line : str
        The actual line.

    Returns
    -------
    _Word
        The word object created.

    Raises
    ------
    InvalidVocabFileFormatError
        If the vocab file is formatted incorrectly.
    """
    if current == "Verb":
        if len(latin_parts) not in {1, 3, 4}:
            raise InvalidVocabFileFormatError(f"Invalid verb format: '{line}'")

        # Irregular verb
        if len(latin_parts) == 1:
            return Verb(latin_parts[0], meaning=meaning)

        # Deponent verbs
        if len(latin_parts) == 3:
            return Verb(
                latin_parts[0], latin_parts[1], latin_parts[2], meaning=meaning
            )

        # Non-deponent verbs
        return Verb(
            latin_parts[0],
            latin_parts[1],
            latin_parts[2],
            latin_parts[3],
            meaning=meaning,
        )

    if current == "Noun":
        if len(latin_parts) not in {1, 3}:
            raise InvalidVocabFileFormatError(f"Invalid noun format: '{line}'")

        # Irregular noun
        if len(latin_parts) == 1:
            return Noun(latin_parts[0], meaning=meaning)

        try:
            return Noun(
                latin_parts[0],
                latin_parts[1].split()[0],
                gender=Gender(latin_parts[2].split()[-1].strip("()")),
                meaning=meaning,
            )
        except ValueError as e:
            raise InvalidVocabFileFormatError(
                f"Invalid gender: '{latin_parts[2].split()[-1].strip('()')}'"
            ) from e

    if current == "Adjective":
        if len(latin_parts) not in {3, 4}:
            raise InvalidVocabFileFormatError(
                f"Invalid adjective format: '{line}'"
            )

        declension = latin_parts[-1].strip("()")

        if declension not in {"212", "2-1-2"} and not match(
            r"^3-.$", declension
        ):
            raise InvalidVocabFileFormatError(
                f"Invalid adjective declension: '{declension}'"
            )

        # Third declension adjective
        if declension.startswith("3"):
            termination = int(declension[2])
            assert is_termination(termination)

            return Adjective(
                *latin_parts[:-1],
                termination=termination,
                declension="3",
                meaning=meaning,
            )

        # Second declension adjective
        return Adjective(*latin_parts[:-1], meaning=meaning, declension="212")

    if current == "Regular":
        return RegularWord(latin_parts[0], meaning=meaning)

    return Pronoun(latin_parts[0], meaning=meaning)
