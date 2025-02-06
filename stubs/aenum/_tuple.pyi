from _typeshed import Incomplete

from ._common import *
from ._constant import NamedConstant

__all__ = ["TupleSize", "NamedTuple"]

class NamedTupleDict(OrderedDict):
    def __init__(self, *args: Incomplete, **kwds: Incomplete) -> None: ...
    def __setitem__(self, key: Incomplete, value: Incomplete) -> None: ...

class _TupleAttributeAtIndex:
    name: Incomplete
    index: Incomplete
    __doc__: Incomplete
    default: Incomplete
    def __init__(
        self,
        name: Incomplete,
        index: Incomplete,
        doc: Incomplete,
        default: Incomplete,
    ) -> None: ...
    def __get__(
        self, instance: Incomplete, owner: Incomplete
    ) -> Incomplete: ...

class undefined:
    def __bool__(self) -> bool: ...
    __nonzero__ = __bool__

class TupleSize(NamedConstant):
    fixed: Incomplete
    minimum: Incomplete
    variable: Incomplete

class NamedTupleMeta(type):
    @classmethod
    def __prepare__(
        metacls: Incomplete,
        cls: Incomplete,
        bases: Incomplete,
        size: Incomplete = ...,
        **kwds: Incomplete,
    ) -> Incomplete: ...
    def __init__(
        cls: Incomplete, *args: Incomplete, **kwds: Incomplete
    ) -> None: ...
    def __new__(
        metacls: Incomplete,
        cls: Incomplete,
        bases: Incomplete,
        clsdict: Incomplete,
        size: Incomplete = ...,
        **kwds: Incomplete,
    ) -> Incomplete: ...
    def __add__(cls: Incomplete, other: Incomplete) -> Incomplete: ...
    def __call__(
        cls: Incomplete, *args: Incomplete, **kwds: Incomplete
    ) -> Incomplete: ...
    def __fields__(cls: Incomplete) -> Incomplete: ...
    def __aliases__(cls: Incomplete) -> Incomplete: ...

NamedTuple: Incomplete
