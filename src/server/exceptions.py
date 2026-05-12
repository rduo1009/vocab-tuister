"""Contains custom exceptions used by the server."""

from __future__ import annotations


class InvalidSettingsError(Exception):
    """An error that is raised when the given settings are invalid."""
