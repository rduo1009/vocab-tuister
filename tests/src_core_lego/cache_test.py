import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from pathlib import Path

from src.core.lego.cache import cache_vocab_file
from src.core.lego.reader import read_vocab_dump


def test_cache():
    hash_string = "a58242a6a237cc769ee385de7d89e921f8ca6a8fb51e0c3dc67392731086ab3f"
    x, _ = cache_vocab_file(Path("tests/src_core_lego/test_vocab_files/testdump/cache"), Path("tests/src_core_lego/test_vocab_files/regular_list.txt"))
    y = read_vocab_dump(Path(f"tests/src_core_lego/test_vocab_files/testdump/cache/{hash_string}"))
    assert x == y


def test_regenerate_cache():
    _, _ = cache_vocab_file(Path("tests/src_core_lego/test_vocab_files/testdump/cache"), Path("tests/src_core_lego/test_vocab_files/regular_with_s_list.txt"))
    _, y = cache_vocab_file(Path("tests/src_core_lego/test_vocab_files/testdump/cache"), Path("tests/src_core_lego/test_vocab_files/regular_with_s_list.txt"))
    assert y
