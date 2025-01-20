from __future__ import annotations

from typing import Any

def color(
    s: str,
    fg: str | int | tuple[Any] | None = None,
    bg: str | int | tuple[Any] | None = None,
    style: str | None = None,
) -> str: ...
