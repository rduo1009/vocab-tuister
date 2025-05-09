from collections.abc import Callable
from typing import Any

from _typeshed import Incomplete

class LazyCorpusLoader:
    def __getattr__(self, attr: str) -> Callable: ...
    def __init__(
        self,
        name: str,
        reader_cls: Any,
        *args: Incomplete,
        **kwargs: Incomplete,
    ) -> Incomplete: ...
