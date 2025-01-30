"""Contains custom exceptions used by ``transfero``."""


class InvalidWordError(Exception):
    """An error that is raised when the word is invalid."""


class InvalidComponentsError(Exception):
    """An error that is raised when the components are invalid."""
