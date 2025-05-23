# pyright: reportAny=false, reportExplicitAny=false

from collections.abc import Callable
from typing import Any

class LazyCorpusLoader:
    def __getattr__(self, attr: str) -> Callable: ...  # pyright: ignore[reportMissingTypeArgument]
    def __init__(
        self, name: str, reader_cls: Any, *args: Any, **kwargs: Any
    ) -> None: ...
