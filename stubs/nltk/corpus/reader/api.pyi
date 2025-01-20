from typing import Any

from _typeshed import Incomplete

from nltk.data import (
    FileSystemPathPointer,
    SeekableUnicodeStreamReader,
    ZipFilePathPointer,
)

class CorpusReader:
    def __init__(
        self,
        root: ZipFilePathPointer | FileSystemPathPointer,
        fileids: str | tuple[str, ...],
        encoding: str | list[tuple[str, str]] = ...,
        tagset: None = ...,
    ) -> Incomplete: ...
    def abspath(self, fileid: str) -> ZipFilePathPointer: ...
    def abspaths(
        self,
        fileids: str | None = ...,
        include_encoding: bool = ...,
        include_fileid: bool = ...,
    ) -> list[
        tuple[FileSystemPathPointer, str]
        | tuple[ZipFilePathPointer, str]
        | Any
    ]: ...
    def encoding(self, file: str) -> str: ...
    def ensure_loaded(self) -> Incomplete: ...
    def fileids(self) -> list[Any]: ...
    def open(self, file: str) -> SeekableUnicodeStreamReader: ...
