import enum as enum
import sqlite3 as sqlite3
from enum import EnumMeta as StdlibEnumMeta

try:
    from enum import FlagBoundary as FlagBoundary
except ImportError:
    class FlagBoundary(StrEnum):
        STRICT: Incomplete
        CONFORM: Incomplete
        EJECT: Incomplete
        KEEP: Incomplete

from types import DynamicClassAttribute

from _typeshed import Incomplete

from ._common import *
from ._constant import NamedConstant
from ._tuple import NamedTuple

__all__ = [
    "bit_count",
    "is_single_bit",
    "bin",
    "property",
    "bits",
    "AddValue",
    "MagicValue",
    "MultiValue",
    "NoAlias",
    "Unique",
    "enum",
    "auto",
    "AddValueEnum",
    "MultiValueEnum",
    "NoAliasEnum",
    "UniqueEnum",
    "AutoNumberEnum",
    "OrderedEnum",
    "unique",
    "no_arg",
    "extend_enum",
    "enum_property",
    "EnumType",
    "EnumMeta",
    "EnumDict",
    "Enum",
    "IntEnum",
    "StrEnum",
    "Flag",
    "IntFlag",
    "LowerStrEnum",
    "UpperStrEnum",
    "ReprEnum",
    "sqlite3",
    "FlagBoundary",
    "STRICT",
    "CONFORM",
    "EJECT",
    "KEEP",
    "add_stdlib_integration",
    "remove_stdlib_integration",
    "export",
    "cls2module",
    "_reduce_ex_by_name",
    "show_flag_values",
    "AutoEnum",
]
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enum import Enum as Enum
else:
    Enum: Incomplete

RecursionError = RuntimeError
MagicValue: Incomplete
AddValue: Incomplete
MultiValue: Incomplete
NoAlias: Incomplete
Unique: Incomplete

def export(
    collection: Incomplete, namespace: Incomplete | None = None
) -> Incomplete: ...
def bit_count(num: Incomplete) -> Incomplete: ...
def is_single_bit(value: Incomplete) -> Incomplete: ...
def bin(
    value: Incomplete, max_bits: Incomplete | None = None
) -> Incomplete: ...
def show_flag_values(value: Incomplete) -> Incomplete: ...

base = DynamicClassAttribute
base = object  # type: ignore[assignment]

class property(base):
    fget: Incomplete
    fset: Incomplete
    fdel: Incomplete
    __doc__: Incomplete
    overwrite_doc: Incomplete
    __isabstractmethod__: Incomplete
    def __init__(
        self,
        fget: Incomplete | None = None,
        fset: Incomplete | None = None,
        fdel: Incomplete | None = None,
        doc: Incomplete | None = None,
    ) -> None: ...
    def getter(self, fget: Incomplete) -> Incomplete: ...
    def setter(self, fset: Incomplete) -> Incomplete: ...
    def deleter(self, fdel: Incomplete) -> Incomplete: ...
    def __get__(
        self, instance: Incomplete, ownerclass: Incomplete | None = None
    ) -> Incomplete: ...
    def __set__(
        self, instance: Incomplete, value: Incomplete
    ) -> Incomplete: ...
    def __delete__(self, instance: Incomplete) -> Incomplete: ...
    name: Incomplete
    clsname: Incomplete
    ownerclass: Incomplete
    def __set_name__(
        self, ownerclass: Incomplete, name: Incomplete
    ) -> None: ...

DynamicClassAttribute = property
enum_property = property

class SentinelType(type): ...

def bits(num: Incomplete) -> Incomplete: ...

class EnumConstants(NamedConstant):
    AddValue: Incomplete
    MagicValue: Incomplete
    MultiValue: Incomplete
    NoAlias: Incomplete
    Unique: Incomplete

class ReprEnum: ...

IntEnum: Incomplete

class Flag: ...

EJECT: Incomplete

KEEP: Incomplete

class enum:
    name: Incomplete
    def __init__(self, *args: Incomplete, **kwds: Incomplete) -> None: ...
    def args(self) -> Incomplete: ...
    def kwds(self) -> Incomplete: ...
    def __hash__(self) -> Incomplete: ...
    def __eq__(self, other: Incomplete) -> Incomplete: ...
    def __ne__(self, other: Incomplete) -> Incomplete: ...

class auto(enum):  # type: ignore[valid-type]
    enum_member: Incomplete
    def __and__(self, other: Incomplete) -> Incomplete: ...
    def __rand__(self, other: Incomplete) -> Incomplete: ...
    def __invert__(self) -> Incomplete: ...
    def __or__(self, other: Incomplete) -> Incomplete: ...
    def __ror__(self, other: Incomplete) -> Incomplete: ...
    def __xor__(self, other: Incomplete) -> Incomplete: ...
    def __rxor__(self, other: Incomplete) -> Incomplete: ...
    def __abs__(self) -> Incomplete: ...
    def __add__(self, other: Incomplete) -> Incomplete: ...
    def __radd__(self, other: Incomplete) -> Incomplete: ...
    def __neg__(self) -> Incomplete: ...
    def __pos__(self) -> Incomplete: ...
    def __rdiv__(self, other: Incomplete) -> Incomplete: ...
    def __floordiv__(self, other: Incomplete) -> Incomplete: ...
    def __rfloordiv__(self, other: Incomplete) -> Incomplete: ...
    def __truediv__(self, other: Incomplete) -> Incomplete: ...
    def __rtruediv__(self, other: Incomplete) -> Incomplete: ...
    def __lshift__(self, other: Incomplete) -> Incomplete: ...
    def __rlshift__(self, other: Incomplete) -> Incomplete: ...
    def __rshift__(self, other: Incomplete) -> Incomplete: ...
    def __rrshift__(self, other: Incomplete) -> Incomplete: ...
    def __mod__(self, other: Incomplete) -> Incomplete: ...
    def __rmod__(self, other: Incomplete) -> Incomplete: ...
    def __mul__(self, other: Incomplete) -> Incomplete: ...
    def __rmul__(self, other: Incomplete) -> Incomplete: ...
    def __pow__(self, other: Incomplete) -> Incomplete: ...
    def __rpow__(self, other: Incomplete) -> Incomplete: ...
    def __sub__(self, other: Incomplete) -> Incomplete: ...
    def __rsub__(self, other: Incomplete) -> Incomplete: ...
    def value(self) -> Incomplete: ...
    @value.setter  # type: ignore[attr-defined]
    def value(self, value: Incomplete) -> None: ...

class _EnumArgSpec(NamedTuple):
    args: Incomplete
    varargs: Incomplete
    keywords: Incomplete
    defaults: Incomplete
    required: Incomplete
    def __new__(cls: Incomplete, _new_func: Incomplete) -> Incomplete: ...

class _proto_member:
    value: Incomplete
    def __init__(self, value: Incomplete) -> None: ...
    def __set_name__(
        self, enum_class: Incomplete, member_name: Incomplete
    ) -> None: ...

class EnumDict(dict):
    def __init__(
        self,
        cls_name: Incomplete,
        settings: Incomplete,
        start: Incomplete,
        constructor_init: Incomplete,
        constructor_start: Incomplete,
        constructor_boundary: Incomplete,
    ) -> None: ...
    def __getitem__(self, key: Incomplete) -> Incomplete: ...
    def __setitem__(self, key: Incomplete, value: Incomplete) -> None: ...

no_arg: Incomplete

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

if StdlibEnumMeta:  # type: ignore[truthy-function]
    class EnumType(EnumType, StdlibEnumMeta): ...

EnumMeta = EnumType

# _reduce_ex_by_name = pickle_by_global_name

class IntEnum(int, ReprEnum): ...

class StrEnum(str, ReprEnum):
    def __new__(
        cls: Incomplete, *values: Incomplete, **kwds: Incomplete
    ) -> Incomplete: ...

class LowerStrEnum(StrEnum):
    def __new__(
        cls: Incomplete,
        value: Incomplete,
        *args: Incomplete,
        **kwds: Incomplete,
    ) -> Incomplete: ...

class UpperStrEnum(StrEnum):
    def __new__(
        cls: Incomplete,
        value: Incomplete,
        *args: Incomplete,
        **kwds: Incomplete,
    ) -> Incomplete: ...

class AutoEnum(Enum): ...

class AutoNumberEnum(Enum):
    def __new__(
        cls: Incomplete, *args: Incomplete, **kwds: Incomplete
    ) -> Incomplete: ...

class AddValueEnum(Enum): ...
class MultiValueEnum(Enum): ...
class NoAliasEnum(Enum): ...

class OrderedEnum(Enum):
    def __ge__(self, other: Incomplete) -> Incomplete: ...
    def __gt__(self, other: Incomplete) -> Incomplete: ...
    def __le__(self, other: Incomplete) -> Incomplete: ...
    def __lt__(self, other: Incomplete) -> Incomplete: ...

class SqliteEnum(Enum):
    def __conform__(self, protocol: Incomplete) -> Incomplete: ...

class UniqueEnum(Enum): ...

def extend_enum(
    enumeration: Incomplete,
    name: Incomplete,
    *args: Incomplete,
    **kwds: Incomplete,
) -> Incomplete: ...
def unique(enumeration: Incomplete) -> Incomplete: ...

class IntFlag(int, ReprEnum, Flag):
    def __contains__(self, other: Incomplete) -> bool: ...

def add_stdlib_integration() -> None: ...
def remove_stdlib_integration() -> None: ...

class cls2module:
    def __init__(self, cls: Incomplete, *args: Incomplete) -> None: ...
    def register(self) -> None: ...

# Names in __all__ with no definition:
#   CONFORM
#   STRICT
