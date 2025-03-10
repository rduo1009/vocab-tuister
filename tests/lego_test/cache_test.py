import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from pathlib import Path

from src.core.lego.cache import cache_vocab_file
from src.core.lego.reader import read_vocab_dump


def test_cache():
    hash_string = "7b5f46ebe47dcba62c0210be71543f26be109f24cfef89efd4e89e266d8b0d3d"
    x, _ = cache_vocab_file(Path("tests/lego_test/testdata/test_output/cache"), Path("tests/lego_test/testdata/regular_list.txt"))
    y = read_vocab_dump(Path(f"tests/lego_test/testdata/test_output/cache/{hash_string}"))
    assert x == y


def test_regenerate_cache():
    _, _ = cache_vocab_file(Path("tests/lego_test/testdata/test_output/cache"), Path("tests/lego_test/testdata/regular_with_s_list.txt"))
    _, y = cache_vocab_file(Path("tests/lego_test/testdata/test_output/cache"), Path("tests/lego_test/testdata/regular_with_s_list.txt"))
    assert y
