"""The CLI that runs the server."""

# ruff: noqa: TCH002

from __future__ import annotations

import logging
import sys
import warnings
from typing import Annotated

from cyclopts import App, Parameter
from cyclopts.types import UInt16

from src import __version__
from src.utils.logger import (
    CustomHandler,
    custom_formatwarning,
    log_uncaught_exceptions,
)

from .server.app import main as server_main
from .server.app import main_dev as server_main_dev

# Initialise logger
logger = logging.getLogger()
logging.captureWarnings(capture=True)

# Set custom formatting for warnings and exceptions
warnings.formatwarning = custom_formatwarning
sys.excepthook = log_uncaught_exceptions  # type: ignore[assignment]

# Set custom handler for logs
for handler in logger.handlers.copy():
    logger.removeHandler(handler)
handler = CustomHandler()


logger.addHandler(handler)
cli = App(
    version=__version__,  # for some reason this is needed
    default_parameter=Parameter(negative=()),
)


def _set_verbosity(verbosity: int) -> None:
    verbosity_map = {
        -1: logging.CRITICAL,  # quiet mode
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
    }

    logger.setLevel(verbosity_map.get(verbosity, logging.DEBUG))
    handler.setLevel(verbosity_map.get(verbosity, logging.DEBUG))


@cli.default
def vocab_tuister_server(
    *,
    port: Annotated[UInt16, Parameter(name=["--port", "-p"])] = 5000,
    verbose: Annotated[
        tuple[bool, ...], Parameter(name=["--verbose", "-v"])
    ] = (False,),
    quiet: bool = False,
    dev: bool = False,
    debug: bool = False,
) -> None:
    """Start the vocab-tuister server.

    Parameters
    ----------
    port : int
        The port to run the server on.
    verbose : tuple[bool, ...]
        How verbose to make the output (maximum 3). Note that additional
        verbosity flags must be added like ``-v -v -v``, due to a bug with
        Cyclopts.
    quiet : bool
        Whether to make the output quiet (only critical errors). Overrides
        ``--verbose``.
    dev : bool
        Use the Flask development server instead of the production server.
        Should not be used usually.
    debug : bool
        Run in debug mode. Implies ``--dev``.
        Should not be used usually.
    """
    _set_verbosity(-1 if quiet else sum(verbose))

    if dev or debug:
        server_main_dev(port, debug=debug)
    else:
        server_main(port)


if __name__ == "__main__":
    cli()
