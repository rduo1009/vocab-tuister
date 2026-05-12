"""Contains custom exceptions used by ``rogo``."""

from __future__ import annotations


class InvalidSessionConfigError(Exception):
    """An error that is raised when the given session config is invalid."""
