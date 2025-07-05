# pyright: reportAny=false, reportExplicitAny=false

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Iterator, Mapping, Sequence
from typing import Any, Literal, TypeVar

from ._common import *

no_arg: object

_EnumTypeSelf = TypeVar("_EnumTypeSelf", bound="EnumType")

_InitParamType = str | list[str] | None
_SettingsParamType = Sequence[str] | str

class EnumDict(OrderedDict[str, Any]): ...

class EnumType(type):
    @classmethod
    def __prepare__(  # type: ignore[override]
        metacls: type[_EnumTypeSelf],
        cls: str,
        bases: tuple[type, ...],
        init: _InitParamType = None,
        start: int | None = None,
        settings: _SettingsParamType = (),
        boundary: Any | None = None,
        **kwds: Any,
    ) -> EnumDict: ...
    def __init__(cls: EnumType, *args: Any, **kwds: Any) -> None: ...
    def __new__(
        metacls: type[_EnumTypeSelf],
        name: str,
        bases: tuple[type, ...],
        clsdict: Mapping[str, Any] | EnumDict,
        init: _InitParamType = None,
        start: int | None = None,
        settings: _SettingsParamType = (),
        boundary: Any | None = None,
        **kwds: Any,
    ) -> type[object]: ...
    def __bool__(cls: EnumType) -> Literal[True]: ...
    def __call__(
        cls: EnumType,
        value: Any = no_arg,
        names: str | Sequence[str | tuple[str, Any]] | Mapping[str, Any] | None = None,
        module: str | None = None,
        qualname: str | None = None,
        type: type | None = None,
        start: int = 1,
        boundary: Any | None = None,
    ) -> EnumType: ...
    def __contains__(cls: EnumType, member_or_value: Any) -> bool: ...
    def __delattr__(cls: EnumType, attr: str) -> None: ...
    def __dir__(cls: EnumType) -> list[str]: ...
    @property
    def __members__(cls: EnumType) -> Mapping[str, EnumType]: ...
    def __getitem__(cls: EnumType, name: str) -> EnumType: ...
    def __iter__(cls: EnumType) -> Iterator[EnumType]: ...
    def __reversed__(cls: EnumType) -> Iterator[EnumType]: ...
    def __len__(cls: EnumType) -> int: ...
    def __repr__(cls: EnumType) -> str: ...
    def __setattr__(cls: EnumType, name: str, value: Any) -> None: ...

    __nonzero__ = __bool__

Enum: EnumType
MultiValue: constant
