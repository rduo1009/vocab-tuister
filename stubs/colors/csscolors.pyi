from __future__ import annotations

from typing import Final

string_types: type[str]
css_colors: Final[dict[str, tuple[str, str, str]]]

def parse_rgb(s: str) -> tuple[str, str, str]: ...
