"""Custom logger for vocab-tuister."""

# ruff: noqa: T201, ARG001

from __future__ import annotations

import datetime
import logging
import sys
from functools import partial
from typing import TYPE_CHECKING, Any, Final, NoReturn

from colors import color as ansicolour  # avoiding spelling nightmare

if TYPE_CHECKING:
    from types import TracebackType

type _AnsiColour = partial[str]
LOGGER_PALETTE: Final[dict[str, _AnsiColour]] = {
    "caller_colour": partial(ansicolour, style="faint"),
    "prefix_colour": partial(ansicolour, fg=86, style="bold"),
    "error_colour": partial(ansicolour, fg=204, style="bold"),
    "warning_colour": partial(ansicolour, fg=192, style="bold"),
    "info_colour": partial(ansicolour, fg=86, style="bold"),
    "debug_colour": partial(ansicolour, fg=63, style="bold"),
    "critical_colour": partial(ansicolour, fg=134, style="bold"),
}


def log_uncaught_exceptions(
    exc_type: type[Exception],
    exc_value: Exception,
    exc_traceback: TracebackType,
) -> NoReturn:
    """Log uncaught exceptions with a critical level log.

    Parameters
    ----------
    exc_type : type[Exception]
    exc_value : Exception
    exc_traceback : TracebackType

    Examples
    --------
    >>> sys.excepthook = log_uncaught_exceptions  # doctest: +SKIP
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
    else:
        logging.critical(  # noqa: LOG015
            "%s: %s", exc_type.__name__, exc_value
        )

    sys.exit(1)


def custom_formatwarning(
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    line: str | None = None,
) -> str:
    """Format any warnings.

    Returns
    -------
    str
        The formatted message.

    Examples
    --------
    >>> warnings.formatwarning = custom_formatwarning  # doctest: +SKIP
    """
    return f"{category.__name__}: {message}"


class CustomLogFormatter(logging.Formatter):
    """A custom formatter that applies custom formatting to logging records.

    This uses https://github.com/charmbracelet/log as a reference.
    """

    def __init__(self) -> None:
        """Initialise the custom log formatter."""
        super().__init__()

        # Map logging levels to colours
        self.level_colours: dict[int, _AnsiColour] = {
            logging.DEBUG: LOGGER_PALETTE["debug_colour"],
            logging.INFO: LOGGER_PALETTE["info_colour"],
            logging.WARNING: LOGGER_PALETTE["warning_colour"],
            logging.ERROR: LOGGER_PALETTE["error_colour"],
            logging.CRITICAL: LOGGER_PALETTE["critical_colour"],
        }

    def format(self, record: logging.LogRecord) -> str:
        """Format the log message.

        Parameters
        ----------
        LogRecord
            The logging record.

        Returns
        -------
        str
            The formatted log message.
        """
        time_str: str = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")  # noqa: DTZ005
        colour: _AnsiColour = self.level_colours.get(
            record.levelno, LOGGER_PALETTE["info_colour"]
        )
        level_str: str = colour(record.levelname[:4])
        caller_info_str: str = LOGGER_PALETTE["caller_colour"](
            f"{record.filename}:{record.lineno}"
        )

        return (
            f"{time_str} {level_str} {record.getMessage()} {caller_info_str}"
        )


class CustomHandler(logging.StreamHandler[Any]):
    """The custom handler that has the custom formatter."""

    def __init__(self) -> None:
        """Initialise the custom handler."""
        super().__init__()

        self.setFormatter(CustomLogFormatter())
