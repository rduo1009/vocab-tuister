from pathlib import Path

from src.core.lego.cache import cache_vocab_file
from src.core.lego.reader import read_vocab_dump


def test_cache():
    hash_string = "74a18441f0062378cba7bc8a1c0ec5957749d9744d057a0a8456fde7c824d051"
    x, _ = cache_vocab_file(Path("tests/lego_test/testdata/test_output/cache"), Path("tests/lego_test/testdata/regular_list.txt"))
    y = read_vocab_dump(Path(f"tests/lego_test/testdata/test_output/cache/{hash_string}"))
    assert x == y


def test_regenerate_cache():
    _, _ = cache_vocab_file(Path("tests/lego_test/testdata/test_output/cache"), Path("tests/lego_test/testdata/regular_with_s_list.txt"))
    _, y = cache_vocab_file(Path("tests/lego_test/testdata/test_output/cache"), Path("tests/lego_test/testdata/regular_with_s_list.txt"))
    assert y
