"""The CLI that runs the server."""

# pyright: basic
# ruff: noqa: TC002, TC003

import logging
import sys
import warnings
from collections.abc import Sequence
from typing import Annotated

from cyclopts import App, Parameter
from cyclopts.types import UInt16
from rich.console import Console

from src import __version__, _seed
from src.server.app import main as server_main, main_dev as server_main_dev
from src.utils.logger import (
    CustomHandler,
    custom_formatwarning,
    log_uncaught_exceptions,
)

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
    name="vocab-tuister-server",
    version=__version__,  # this is needed due to dynamic versioning
    default_parameter=Parameter(negative=()),
    help_on_error=True,
    console=console,
)
cli.register_install_completion_command()


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
        Sequence[bool], Parameter(alias="-v", negative="--quiet")
    ] = (),
    dev: bool = False,
    debug: bool = False,
) -> None:
    """Start the vocab-tuister server.

    Parameters
    ----------
    port : int
        The port to run the server on.
    verbose : tuple[bool, ...]
        How verbose to make the output (maximum 3).
    dev : bool
        Use the Flask development server instead of the production server.
        Should not be used usually.
    debug : bool
        Run in debug mode. Implies ``--dev``.
        Prints full traceback when the program raises an exception.
        Should not be used usually.
    """
    # Handle `--quiet`: any occurrence forces verbosity -1, otherwise count -v (max 3)
    if any(not v for v in verbose):
        verbosity = -1
    else:
        verbosity = min(3, sum(1 for v in verbose if v))
    _set_verbosity(verbosity)

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
