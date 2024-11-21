from __future__ import annotations

from functools import partial
from typing import Any, Final, TypeIs

from .csscolors import css_colors as css_colors
from .csscolors import parse_rgb as parse_rgb

string_types: type[str]
COLORS: Final[tuple[str, ...]]
STYLES: Final[tuple[str, ...]]

def is_string(obj: object) -> TypeIs[str]: ...
def color(
    s: str,
    fg: str | int | tuple[Any] | None = None,
    bg: str | int | tuple[Any] | None = None,
    style: str | None = None,
) -> str: ...
def strip_color(s: str) -> str: ...
def ansilen(s: str) -> int: ...

black: partial[str]
red: partial[str]
green: partial[str]
yellow: partial[str]
blue: partial[str]
magenta: partial[str]
cyan: partial[str]
white: partial[str]
bold: partial[str]
none: partial[str]
faint: partial[str]
italic: partial[str]
underline: partial[str]
blink: partial[str]
blink2: partial[str]
negative: partial[str]
concealed: partial[str]
crossed: partial[str]
