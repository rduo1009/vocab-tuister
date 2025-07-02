from __future__ import annotations

from typing import TextIO

def download(
    info_or_id: str | None = None,
    download_dir: str | None = None,
    quiet: bool = False,
    force: bool = False,
    prefix: str = "[nltk_data] ",
    halt_on_error: bool = True,
    raise_on_error: bool = False,
    print_error_to: TextIO | None = None,
) -> bool: ...
