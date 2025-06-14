# pyright: reportAny=false, reportExplicitAny=false

from __future__ import annotations

from abc import ABCMeta

path: list[str]

class PathPointer(metaclass=ABCMeta): ...
class ZipFilePathPointer(PathPointer): ...

def find(resource_name: str, paths: list[str] | None = None) -> str: ...
