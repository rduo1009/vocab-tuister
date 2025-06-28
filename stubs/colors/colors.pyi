from __future__ import annotations

def color(
    s: str,
    fg: str | int | tuple[int, int, int] | list[int] | None = None,
    bg: str | int | tuple[int, int, int] | list[int] | None = None,
    style: str | None = None,
) -> str: ...
