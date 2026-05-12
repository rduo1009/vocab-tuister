"""The CLI that runs the server."""

# nuitka-project: --standalone
# nuitka-project: --enable-plugin=dill-compat
## nuitka-project: --experimental=deferred-annotations # TODO: Maybe this is necessary/good to use in future (when it is fixed)?

# nuitka-project: --include-data-files=src/core/transfero/wn_data/wn.db.zst=src/core/transfero/wn_data/wn.db.zst
# nuitka-project: --include-data-files=src/core/transfero/adj_to_adv.json=src/core/transfero/adj_to_adv.json
# nuitka-project: --include-data-files=__version__.txt=__version__.txt

# nuitka-project: --include-package-data=lemminflect:resources/*
# nuitka-project: --include-package-data=wn:index.toml
# nuitka-project: --include-package-data=wn:schema.sql

## nuitka-project: --include-module=numpy.core.multiarray
## nuitka-project: --include-module=ddc459050edb75a05942__mypyc # TODO: Do these do anything?
## nuitka-project: --include-module=5bae8a57b5ef85818b48__mypyc
## nuitka-project: --include-module=3c22db458360489351e4__mypyc

## nuitka-project: --nofollow-import-to=typeguard
## nuitka-project: --nofollow-import-to=tkinter

# pyright: basic
# ruff: noqa: TC002, TC003

import logging
import os
import sys
import warnings
from collections.abc import Sequence
from typing import Annotated

from cyclopts import App, Parameter
from cyclopts.types import UInt16
from rich.console import Console

from src import __version__, _seed
from src.server.app import main as server_main
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

console = (
    Console(force_terminal=True, color_system="truecolor")
    if os.environ.get("CI") != "true"
    else Console()
)
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
    debug: bool = False,
) -> None:
    """Start the vocab-tuister server.

    Parameters
    ----------
    port : int
        The port to run the server on.
    verbose : tuple[bool, ...]
        How verbose to make the output (maximum 3).
    debug : bool
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

    server_main(port)


if __name__ == "__main__":
    try:
        cli()
    except Exception:  # noqa: BLE001
        console.print_exception()
