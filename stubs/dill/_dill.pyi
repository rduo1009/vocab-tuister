from __future__ import annotations

from pickle import Unpickler as StockUnpickler
from typing import Any

from _typeshed import Incomplete

def dumps(
    obj: object,
    protocol: Incomplete | None = None,
    byref: Incomplete | None = None,
    fmode: Incomplete | None = None,
    recurse: Incomplete | None = None,
    **kwds: Incomplete,
) -> Incomplete: ...
def loads(
    str: str | bytes, ignore: Incomplete | None = None, **kwds: Any
) -> Unpickler: ...

class Unpickler(StockUnpickler):
    settings: dict[str, Any]
    def find_class(
        self, module: Incomplete, name: Incomplete
    ) -> Incomplete: ...
    def __init__(self, *args: Incomplete, **kwds: Incomplete) -> None: ...
    def load(self) -> Incomplete: ...
