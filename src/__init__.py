"""A wrapper for the Python packages used by ``vocab-tester``."""

from __future__ import annotations

import os as _os

_seed: str | None = _os.getenv("VOCAB_TUISTER_RANDOM_SEED")
if _seed is not None:
    import random
    import sys as _sys
    import types as _types

    try:
        _seed_value: int = int(_seed)
    except ValueError as e:
        raise ValueError(
            f"Invalid seed value: {_seed}. Must be an integer."
        ) from e

    _custom_random = _types.ModuleType("random")
    _custom_random_class = random.Random(_seed_value)

    _custom_random.Random = random.Random  # type: ignore[attr-defined]
    _custom_random.SystemRandom = random.SystemRandom  # type: ignore[attr-defined]

    _custom_random.random = _custom_random_class.random  # type: ignore[attr-defined]
    _custom_random.uniform = _custom_random_class.uniform  # type: ignore[attr-defined]

    _custom_random.randint = _custom_random_class.randint  # type: ignore[attr-defined]
    _custom_random.randrange = _custom_random_class.randrange  # type: ignore[attr-defined]

    _custom_random.choice = _custom_random_class.choice  # type: ignore[attr-defined]
    _custom_random.sample = _custom_random_class.sample  # type: ignore[attr-defined]
    _custom_random.shuffle = _custom_random_class.shuffle  # type: ignore[attr-defined]

    _sys.modules["random"] = _custom_random


import dunamai as _dunamai

from . import core, server

try:
    __version__ = _dunamai.get_version(
        "src", third_choice=_dunamai.Version.from_any_vcs
    ).serialize()
except RuntimeError:
    import sys as _sys

    # Frozen with PyInstaller
    if getattr(_sys, "frozen", False) and hasattr(
        _sys, "_MEIPASS"
    ):  # pragma: no cover
        from pathlib import Path

        version_path = Path(__file__).parent.parent / "__version__.txt"

        __version__ = version_path.read_text().strip()
    else:
        raise

__author__ = "rduo1009"
__copyright__ = "2024, rduo1009"
__license__ = "MIT"
__all__ = ["core", "server"]
