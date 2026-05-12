"""Contains custom exceptions used by ``transfero``."""

from __future__ import annotations


class InvalidWordError(Exception):
    """An error that is raised when the word is invalid."""


class InvalidComponentsError(Exception):
    """An error that is raised when the components are invalid."""
