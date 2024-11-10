from typing import NamedTuple

from _typeshed import Incomplete

__all__ = [
    "ContextIndex",
    "ConcordanceIndex",
    "TokenSearcher",
    "Text",
    "TextCollection",
]

class ConcordanceLine(NamedTuple):
    left: Incomplete
    query: Incomplete
    right: Incomplete
    offset: Incomplete
    left_print: Incomplete
    right_print: Incomplete
    line: Incomplete

class ContextIndex:
    def __init__(
        self,
        tokens: Incomplete,
        context_func: Incomplete | None = None,
        filter: Incomplete | None = None,
        key: Incomplete = ...,
    ) -> None: ...
    def tokens(self) -> Incomplete: ...
    def word_similarity_dict(self, word: Incomplete) -> Incomplete: ...
    def similar_words(self, word: Incomplete, n: int = 20) -> Incomplete: ...
    def common_contexts(
        self, words: Incomplete, fail_on_unknown: bool = False
    ) -> Incomplete: ...

class ConcordanceIndex:
    def __init__(self, tokens: Incomplete, key: Incomplete = ...) -> None: ...
    def tokens(self) -> Incomplete: ...
    def offsets(self, word: Incomplete) -> Incomplete: ...
    def find_concordance(
        self, word: Incomplete, width: int = 80
    ) -> Incomplete: ...
    def print_concordance(
        self, word: Incomplete, width: int = 80, lines: int = 25
    ) -> None: ...

class TokenSearcher:
    def __init__(self, tokens: Incomplete) -> None: ...
    def findall(self, regexp: Incomplete) -> Incomplete: ...

class Text:
    tokens: Incomplete
    name: Incomplete
    def __init__(
        self, tokens: Incomplete, name: Incomplete | None = None
    ) -> None: ...
    def __getitem__(self, i: Incomplete) -> Incomplete: ...
    def __len__(self) -> int: ...
    def concordance(
        self, word: Incomplete, width: int = 79, lines: int = 25
    ) -> Incomplete: ...
    def concordance_list(
        self, word: Incomplete, width: int = 79, lines: int = 25
    ) -> Incomplete: ...
    def collocation_list(
        self, num: int = 20, window_size: int = 2
    ) -> Incomplete: ...
    def collocations(self, num: int = 20, window_size: int = 2) -> None: ...
    def count(self, word: Incomplete) -> Incomplete: ...
    def index(self, word: Incomplete) -> Incomplete: ...
    def readability(self, method: Incomplete) -> None: ...
    def similar(self, word: Incomplete, num: int = 20) -> Incomplete: ...
    def common_contexts(
        self, words: Incomplete, num: int = 20
    ) -> Incomplete: ...
    def dispersion_plot(self, words: Incomplete) -> None: ...
    def generate(
        self,
        length: int = 100,
        text_seed: Incomplete | None = None,
        random_seed: int = 42,
    ) -> Incomplete: ...
    def plot(self, *args: Incomplete) -> Incomplete: ...
    def vocab(self) -> Incomplete: ...
    def findall(self, regexp: Incomplete) -> None: ...

class TextCollection(Text):
    def __init__(self, source: Incomplete) -> None: ...
    def tf(self, term: Incomplete, text: Incomplete) -> Incomplete: ...
    def idf(self, term: Incomplete) -> Incomplete: ...
    def tf_idf(self, term: Incomplete, text: Incomplete) -> Incomplete: ...