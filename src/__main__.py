"""The CLI that runs the server."""

# ruff: noqa: TCH002

from typing import Annotated

from cyclopts import App, Parameter
from cyclopts.types import UInt16

from src import __version__  # for some reason this is needed

from .server.app import main as server_main
from .server.app import main_dev as server_main_dev

cli = App(
    version=__version__,
    version_flags=["--version", "-v"],
    default_parameter=Parameter(negative=()),
)


@cli.default
def vocab_tuister_server(
    *,
    port: Annotated[UInt16, Parameter(name=["--port", "-p"])] = 5000,
    dev: bool = False,
    debug: bool = False,
):
    """Start the vocab-tuister server.

    Parameters
    ----------
    port : int
        The port to run the server on.
    dev : bool
        Use the Flask development server instead of the production server.
        Should not be used usually.
    debug : bool
        Run in debug mode. Implies ``--dev``.
        Should not be used usually.
    """
    if dev or debug:
        server_main_dev(port, debug=debug)
    else:
        server_main(port)


if __name__ == "__main__":
    cli()
