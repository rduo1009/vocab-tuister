"""A wrapper for the Python packages used by ``vocab-tester``."""

import dunamai as _dunamai

from . import core, server

try:
    __version__ = _dunamai.get_version(
        "src", third_choice=_dunamai.Version.from_any_vcs
    ).serialize()
except RuntimeError:
    import sys as _sys

    # Frozen with PyInstaller
    if getattr(_sys, "frozen", False) and hasattr(_sys, "_MEIPASS"):
        from pathlib import Path

        version_path = Path(__file__).parent.parent / "__version__.txt"

        with open(version_path) as file:
            __version__ = file.read().strip()
    else:
        raise

__author__ = "rduo1009"
__copyright__ = "2024, rduo1009"
__license__ = "MIT"
__all__ = ["core", "server"]
