from collections.abc import Callable, Iterator

from _typeshed import Incomplete

from nltk.data import FileSystemPathPointer, ZipFilePathPointer

class StreamBackedCorpusView:
    def __getitem__(self, i: int | slice) -> str | list[str]: ...
    def __init__(
        self,
        fileid: ZipFilePathPointer | FileSystemPathPointer,
        block_reader: Callable | None = ...,
        startpos: int = ...,
        encoding: str = ...,
    ) -> None: ...
    def _open(self) -> Incomplete: ...
    def close(self) -> Incomplete: ...
    def iterate_from(self, start_tok: int) -> Iterator[str]: ...
