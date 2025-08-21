import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from pathlib import Path

import pytest
from src.core.accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb
from src.core.accido.misc import Gender, MultipleMeanings
from src.core.lego.exceptions import InvalidVocabFileFormatError
from src.core.lego.misc import VocabList
from src.core.lego.reader import _regenerate_vocab_list, read_vocab_file


def test_reader():
    l = read_vocab_file(Path("tests/lego_test/testdata/regular_list.txt"))
    assert l == VocabList(
        [
            Verb("audio", "audire", "audivi", "auditus", meaning="hear"),
            Verb("capio", "capere", "cepi", "captus", meaning="take"),
            Verb("potior", "potiri", "potitus sum", meaning="master"),
            Verb("queror", "queri", "questus sum", meaning="complain"),
            Verb("inquam", meaning="say"),
            Noun("puella", "puellae", gender=Gender.FEMININE, meaning="girl"),
            Noun("agricola", "agricolae", gender=Gender.MASCULINE, meaning="farmer"),
            Noun("puer", "pueri", gender=Gender.MASCULINE, meaning="boy"),
            Noun("canis", "canis", gender=Gender.MASCULINE, meaning="dog"),
            Noun("nomen", "nominis", gender=Gender.NEUTER, meaning="name"),
            Noun("ego", meaning="I"),
            Adjective("ingens", "ingentis", termination=1, declension="3", meaning="large"),
            Adjective("levis", "leve", termination=2, declension="3", meaning="light"),
            Adjective("acer", "acris", "acre", termination=3, declension="3", meaning="keen"),
            Adjective("bonus", "bona", "bonum", declension="212", meaning="good"),
            Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy"),
            Pronoun("hic", meaning="this"),
            Pronoun("ille", meaning="that"),
            RegularWord("in", meaning="into"),
            RegularWord("e", meaning="from"),
        ],
        """@ Verb
hear: audio, audire, audivi, auditus
take: capio, capere, cepi, captus
master: potior, potiri, potitus sum
complain: queror, queri, questus sum
say: inquam

@ Noun
girl: puella, puellae, (f)
farmer: agricola, agricolae, (m)
boy: puer, pueri, (m)
dog: canis, canis, (m)
name: nomen, nominis, (n)
I: ego

@ Adjective
large: ingens, ingentis, (3-1)
light: levis, leve, (3-2)
keen: acer, acris, acre, (3-3)
good: bonus, bona, bonum, (212)
happy: laetus, laeta, laetum, (2-1-2)

@ Pronoun
this: hic, haec, hoc
that: ille

@ Regular
into: in
from: e

# testing comments
# 
#
# asnfdbjx""",
    )


def test_regenerate():
    l = read_vocab_file(Path("tests/lego_test/testdata/regular_list.txt"))
    assert l == _regenerate_vocab_list(l)


def test_reader_with_s():
    l = read_vocab_file(Path("tests/lego_test/testdata/regular_with_s_list.txt"))
    assert l == VocabList(
        [
            Verb("audio", "audire", "audivi", "auditus", meaning="hear"),
            Verb("capio", "capere", "cepi", "captus", meaning="take"),
            Noun("puella", "puellae", gender=Gender.FEMININE, meaning="girl"),
            Noun("agricola", "agricolae", gender=Gender.MASCULINE, meaning="farmer"),
            Noun("puer", "pueri", gender=Gender.MASCULINE, meaning="boy"),
            Noun("canis", "canis", gender=Gender.MASCULINE, meaning="dog"),
            Noun("nomen", "nominis", gender=Gender.NEUTER, meaning="name"),
            Adjective("ingens", "ingentis", termination=1, declension="3", meaning="large"),
            Adjective("levis", "leve", termination=2, declension="3", meaning="light"),
            Adjective("acer", "acris", "acre", termination=3, declension="3", meaning="keen"),
            Pronoun("hic", meaning="this"),
            Pronoun("ille", meaning="that"),
            RegularWord("in", meaning="into"),
            RegularWord("e", meaning="from"),
        ],
        """@Verbs
hear: audio, audire, audivi, auditus
take: capio, capere, cepi, captus

@Nouns
girl: puella, puellae, (f)
farmer: agricola, agricolae, (m)
boy: puer, pueri, (m)
dog: canis, canis, (m)
name: nomen, nominis, (n)

@Adjectives
large: ingens, ingentis, (3-1)
light: levis, leve, (3-2)
keen: acer, acris, acre, (3-3)

@Pronouns
this: hic, haec, hoc
that: ille

@Regulars
into: in
from: e""",
    )


def test_multiple_meanings():
    l = read_vocab_file(Path("tests/lego_test/testdata/multiple_meanings_list.txt"))
    assert l == VocabList(
        [
            Verb("peto", "petere", "petivi", "petitus", meaning=MultipleMeanings(("attack", "make for", "seek", "ask"))), 
            Noun("ancilla", "ancillae", gender=Gender.FEMININE, meaning=MultipleMeanings(("slave-girl", "maid")))
        ],
        """@ Verbs
attack / make for/seek/ask: peto, petere, petivi, petitus

@ Noun
slave-girl/    maid: ancilla, ancillae, (f)"""
    )  # fmt: skip


def test_invalidpos():
    with pytest.raises(InvalidVocabFileFormatError) as error:
        read_vocab_file(Path("tests/lego_test/testdata/invalid_pos_list.txt"))
    assert str(error.value) == "Invalid part of speech: 'Error'"


def test_invalidlinefmt():
    with pytest.raises(InvalidVocabFileFormatError) as error:
        read_vocab_file(Path("tests/lego_test/testdata/invalid_linefmt_list.txt"))
    assert str(error.value) == "Invalid line format: 'error: error: error'"


def test_nopos():
    with pytest.raises(InvalidVocabFileFormatError) as error:
        read_vocab_file(Path("tests/lego_test/testdata/no_pos_list.txt"))
    assert str(error.value) == "Part of speech was not given."


def test_invalidverbfmt():
    with pytest.raises(InvalidVocabFileFormatError) as error:
        read_vocab_file(Path("tests/lego_test/testdata/invalid_verbfmt_list.txt"))
    assert str(error.value) == "Invalid verb format: 'hear: audio, audire, audivi, auditus, error, error, error'"


def test_invalidnounfmt():
    with pytest.raises(InvalidVocabFileFormatError) as error:
        read_vocab_file(Path("tests/lego_test/testdata/invalid_nounfmt_list.txt"))
    assert str(error.value) == "Invalid noun format: 'dog: canis, canis, error, error'"


def test_invalidadjfmt():
    with pytest.raises(InvalidVocabFileFormatError) as error:
        read_vocab_file(Path("tests/lego_test/testdata/invalid_adjfmt_list.txt"))
    assert str(error.value) == "Invalid adjective format: 'good: bonus, bona, bonum, error, error'"


def test_decl1():
    with pytest.raises(InvalidVocabFileFormatError) as error:
        read_vocab_file(Path("tests/lego_test/testdata/invalid_decl1_list.txt"))
    assert str(error.value) == "Invalid adjective declension: '3'"


def test_decl2():
    with pytest.raises(InvalidVocabFileFormatError) as error:
        read_vocab_file(Path("tests/lego_test/testdata/invalid_decl2_list.txt"))
    assert str(error.value) == "Invalid adjective declension: '4'"


def test_invalid_gender():
    with pytest.raises(InvalidVocabFileFormatError) as error:
        read_vocab_file(Path("tests/lego_test/testdata/invalid_gender_list.txt"))
    assert str(error.value) == "Invalid gender: 'l'"
