"""The CLI that runs the server."""

# ruff: noqa: TC002

import logging
import sys
import warnings
from typing import TYPE_CHECKING, Annotated

from cyclopts import App, Parameter, Token
from cyclopts.types import UInt16
from rich.console import Console

from src import __version__, _seed
from src.server.app import main as server_main, main_dev as server_main_dev
from src.utils.logger import (
    CustomHandler,
    custom_formatwarning,
    log_uncaught_exceptions,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

# Initialise logger
logger = logging.getLogger()
logging.captureWarnings(capture=True)

# Set custom formatting for warnings and exceptions
warnings.formatwarning = custom_formatwarning
sys.excepthook = log_uncaught_exceptions

# Set custom handler for logs
for handler in logger.handlers.copy():
    logger.removeHandler(handler)
handler = CustomHandler()
logger.addHandler(handler)

console = Console()
cli = App(
    version=__version__,  # this is needed due to dynamic versioning
    default_parameter=Parameter(negative=()),
    console=console,
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


def _verbosity_converter(
    type_: type[tuple[bool, ...]], tokens: Sequence[Token]
) -> tuple[bool, ...]:
    assert type_ == tuple[bool, ...]

    return tuple((token.keyword == "-v") for token in tokens)


@cli.default
def vocab_tuister_server(
    *,
    port: Annotated[UInt16, Parameter(name=["--port", "-p"])] = 5000,
    verbose: Annotated[
        tuple[bool, ...],
        Parameter(name=["--verbose", "-v"], converter=_verbosity_converter),
    ] = (),
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
        Prints full traceback when the program raises an exception.
        Should not be used usually.
    """
    _set_verbosity(-1 if quiet else sum(verbose))

    # Seed has been set
    if _seed is not None:
        logger.info("Using random seed '%s'.", _seed)

    if debug:
        sys.excepthook = sys.__excepthook__

    if dev or debug:
        server_main_dev(port, debug=debug)
    else:
        server_main(port)


if __name__ == "__main__":
    try:
        cli()
    except Exception:  # noqa: BLE001
        console.print_exception()
