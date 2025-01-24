from _typeshed import Incomplete

from ._common import *

__all__ = ["NamedConstant", "Constant"]

NamedConstant: Incomplete

class NamedConstantDict(dict):
    def __init__(self) -> None: ...
    def __setitem__(self, key: Incomplete, value: Incomplete) -> None: ...

class NamedConstantMeta(type):
    @classmethod
    def __prepare__(
        metacls: Incomplete,
        cls: Incomplete,
        bases: Incomplete,
        **kwds: Incomplete,
    ) -> Incomplete: ...
    def __new__(
        metacls: Incomplete,
        cls: Incomplete,
        bases: Incomplete,
        clsdict: Incomplete,
    ) -> Incomplete: ...
    def __bool__(cls: Incomplete) -> bool: ...
    def __delattr__(cls: Incomplete, attr: Incomplete) -> None: ...
    def __iter__(cls: Incomplete) -> Incomplete: ...
    def __reversed__(cls: Incomplete) -> Incomplete: ...
    def __len__(cls: Incomplete) -> int: ...
    __nonzero__ = __bool__
    def __setattr__(
        cls: Incomplete, name: Incomplete, value: Incomplete
    ) -> None: ...

Constant = NamedConstant
