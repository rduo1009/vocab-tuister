# pyright: reportAny=false, reportExplicitAny=false

from pickle import Unpickler as StockUnpickler
from typing import Any

def dumps(
    obj: object,
    protocol: int | None = None,
    byref: bool | None = None,
    fmode: str | None = None,
    recurse: bool | None = None,
    **kwds: Any,
) -> bytes: ...
def loads(
    str: str | bytes, ignore: bool | None = None, **kwds: Any
) -> Unpickler: ...

class Unpickler(StockUnpickler): ...
