import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from pathlib import Path

from src.core.lego.cache import cache_vocab_file
from src.core.lego.reader import read_vocab_dump


def test_cache():
    hash_string = "248a3b540525e8ee44cb3be7147b8cd7068b156f1f68e95574a7e5f75a6d13c9"
    x, _ = cache_vocab_file(Path("tests/lego_test/testdata/test_output/cache"), Path("tests/lego_test/testdata/regular_list.txt"))
    y = read_vocab_dump(Path(f"tests/lego_test/testdata/test_output/cache/{hash_string}"))
    assert x == y


def test_regenerate_cache():
    _, _ = cache_vocab_file(Path("tests/lego_test/testdata/test_output/cache"), Path("tests/lego_test/testdata/regular_with_s_list.txt"))
    _, y = cache_vocab_file(Path("tests/lego_test/testdata/test_output/cache"), Path("tests/lego_test/testdata/regular_with_s_list.txt"))
    assert y
