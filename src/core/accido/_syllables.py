"""Contains a functions that finds the number of syllables in a Latin word."""

from __future__ import annotations

from typing import Final

VOWELS: Final[set[str]] = {"a", "e", "i", "o", "u"}
DIPHTHONGS: Final[set[str]] = {"ae", "au", "ei", "eu", "oe", "ui"}


def count_syllables(word: str) -> int:
    """Find the number of syllables in a Latin word.

    Parameters
    ----------
    word : str

    Returns
    -------
    int
        The number of syllables.
    """
    num_syllables = 0
    word_length = len(word)
    i = 0  # Index in word

    while i < word_length:
        if i < word_length - 1 and word[i : i + 2] in DIPHTHONGS:
            num_syllables += 1
            i += 2
        elif word[i] in VOWELS:
            num_syllables += 1
            i += 1
        else:
            i += 1

    return num_syllables
