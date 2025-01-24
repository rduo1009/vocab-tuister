import enum as enum
import sqlite3 as sqlite3

from _typeshed import Incomplete

from ._common import *

class EnumType(type):
    @classmethod
    def __prepare__(
        metacls: Incomplete,
        cls: Incomplete,
        bases: Incomplete,
        init: Incomplete | None = None,
        start: Incomplete | None = None,
        settings: Incomplete = (),
        boundary: Incomplete | None = None,
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
        init: Incomplete | None = None,
        start: Incomplete | None = None,
        settings: Incomplete = (),
        boundary: Incomplete | None = None,
        **kwds: Incomplete,
    ) -> Incomplete: ...
    def __bool__(cls: Incomplete) -> bool: ...
    def __call__(
        cls: Incomplete,
        value: Incomplete = ...,
        names: Incomplete | None = None,
        module: Incomplete | None = None,
        qualname: Incomplete | None = None,
        type: Incomplete | None = None,
        start: int = 1,
        boundary: Incomplete | None = None,
    ) -> Incomplete: ...
    def __contains__(cls: Incomplete, value: Incomplete) -> bool: ...
    def __delattr__(cls: Incomplete, attr: Incomplete) -> None: ...
    def __dir__(cls: Incomplete) -> Incomplete: ...
    def __members__(cls: Incomplete) -> Incomplete: ...
    def __getitem__(cls: Incomplete, name: Incomplete) -> Incomplete: ...
    def __iter__(cls: Incomplete) -> Incomplete: ...
    def __reversed__(cls: Incomplete) -> Incomplete: ...
    def __len__(cls: Incomplete) -> int: ...
    __nonzero__ = __bool__
    def __setattr__(
        cls: Incomplete, name: Incomplete, value: Incomplete
    ) -> None: ...

Enum: EnumType
MultiValue: constant
