import os
import sys  # noqa: E401

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import src as src
from src.core.accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb
from src.core.accido.misc import Gender
from src.core.lego.misc import VocabList


def test_vocablist():
    l = VocabList([
        Verb("audio", "audire", "audivi", "auditus", meaning="hear"),
        Noun("nomen", "nominis", gender=Gender.NEUTER, meaning="name"),
        Adjective("bonus", "bona", "bonum", declension="212", meaning="good"),
        RegularWord("e", meaning="from"),
        Pronoun("ille", meaning="that"),
    ])

    assert l.__repr__() == f"VocabList([Verb(audio, audire, audivi, auditus, hear), Noun(nomen, nominis, neuter, name), Adjective(bonus, bona, bonum, None, 212, good), RegularWord(e, from), Pronoun(ille, that)], version={src.__version__})"
