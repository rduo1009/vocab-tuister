import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import re
from pathlib import Path

import pytest
from src.core.lego.exceptions import MisleadingFilenameWarning
from src.core.lego.reader import read_vocab_dump, read_vocab_file
from src.core.lego.saver import save_vocab_dump


def test_saver():
    x = read_vocab_file(Path("tests/lego_test/testdata/regular_list.txt"))
    save_vocab_dump(Path("tests/lego_test/testdata/test_output/regular_list.test_output"), x)
    y = read_vocab_dump(Path("tests/lego_test/testdata/test_output/regular_list.test_output"))
    assert x == y


def test_saver_wronglz4extension():
    x = read_vocab_file(Path("tests/lego_test/testdata/regular_list.txt"))
    with pytest.warns(MisleadingFilenameWarning, match=re.escape("The file 'tests/lego_test/testdata/test_output/regular_list.test_output.wrong.lz4' is not being compressed, but the file extension ('.lz4') suggests it is.")):
        save_vocab_dump(Path("tests/lego_test/testdata/test_output/regular_list.test_output.wrong.lz4"), x, compress=False)


def test_saver_compress():
    x = read_vocab_file(Path("tests/lego_test/testdata/regular_list.txt"))
    save_vocab_dump(Path("tests/lego_test/testdata/test_output/regular_list.test_output.lz4"), x, compress=True)
    y = read_vocab_dump(Path("tests/lego_test/testdata/test_output/regular_list.test_output.lz4"))
    assert x == y


def test_saver_compress_nolz4extension():
    x = read_vocab_file(Path("tests/lego_test/testdata/regular_list.txt"))
    with pytest.warns(MisleadingFilenameWarning, match=re.escape("The file 'tests/lego_test/testdata/test_output/regular_list.compressedtest_output' is being compressed, but the '.lz4' extension is not present and is being added.")):
        save_vocab_dump(Path("tests/lego_test/testdata/test_output/regular_list.compressedtest_output"), x, compress=True)
    y = read_vocab_dump(Path("tests/lego_test/testdata/test_output/regular_list.compressedtest_output.lz4"))
    assert x == y


def test_nodirectory():
    x = read_vocab_file(Path("tests/lego_test/testdata/regular_list.txt"))
    with pytest.raises(FileNotFoundError) as error:
        save_vocab_dump(Path("tests/lego_test/testdataajofsdifhbd/test_output/regular_list.test_output"), x)
    assert str(error.value) == "The directory 'tests/lego_test/testdataajofsdifhbd/test_output' does not exist."
