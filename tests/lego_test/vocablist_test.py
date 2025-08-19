import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import src
from src.core.accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb
from src.core.accido.misc import Gender, MultipleMeanings
from src.core.lego.misc import VocabList


def test_vocablist():
    l = VocabList([Verb("audio", "audire", "audivi", "auditus", meaning="hear"), Noun("nomen", "nominis", gender=Gender.NEUTER, meaning="name"), Adjective("bonus", "bona", "bonum", declension="212", meaning="good"), RegularWord("e", meaning="from"), Pronoun("ille", meaning="that")], "")

    assert repr(l) == f"VocabList([Verb(audio, audire, audivi, auditus, meaning=hear), Noun(nomen, nominis, gender=neuter, meaning=name), Adjective(bonus, bona, bonum, termination=None, declension=212, meaning=good), RegularWord(e, meaning=from), Pronoun(ille, meaning=that)], version={src.__version__})"


def test_vocablist_add():
    list_1 = VocabList(
        [
            Verb("audio", "audire", "audivi", "auditus", meaning="hear"),
            Noun("templum", "templi", gender=Gender.NEUTER, meaning="temple"),
            Adjective("bonus", "bona", "bonum", declension="212", meaning="good"),
            Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy"),
            RegularWord("e", meaning="from"),
            Pronoun("ille", meaning="that"),
        ],
        """@ Verbs
hear: audio, audire, audivi, auditus

@ Nouns
temple: templum, templi, (n)

@ Adjectives
good: bonus, bona, bonum, (212)
happy: laetus, laeta, laetum, (2-1-2)

@ Pronouns
that: ille

@ Regulars
from: e""",
    )

    list_2 = VocabList(
        [
            Verb("audio", "audire", "audivi", "auditus", meaning="listen"), 
            Noun("templum", "templi", gender=Gender.NEUTER, meaning="shrine"), 
            Adjective("laetus", "laeta", "laetum", declension="212", meaning="joyful"), 
            RegularWord("e", meaning="out"),
            Pronoun("ille", meaning="that"),
        ], 
        """@ Verbs
listen: audio, audire, audivi, auditus

@ Nouns
shrine: templum, templi, (n)

@ Adjectives
joyful: laetus, laeta, laetum, (2-1-2)

@ Pronouns
that: ille

@ Regulars
out: e""",
    )  # fmt: skip

    assert list_1 + list_2 == VocabList(
        [
            Verb("audio", "audire", "audivi", "auditus", meaning=MultipleMeanings(("hear", "listen"))),
            Noun("templum", "templi", gender=Gender.NEUTER, meaning=MultipleMeanings(("temple", "shrine"))),
            Adjective("bonus", "bona", "bonum", declension="212", meaning="good"),
            Adjective("laetus", "laeta", "laetum", declension="212", meaning=MultipleMeanings(("happy", "joyful"))),
            RegularWord("e", meaning=MultipleMeanings(("from", "out"))),
            Pronoun("ille", meaning="that"),
        ],
        """@ Verbs
hear: audio, audire, audivi, auditus

@ Nouns
temple: templum, templi, (n)

@ Adjectives
good: bonus, bona, bonum, (212)
happy: laetus, laeta, laetum, (2-1-2)

@ Pronouns
that: ille

@ Regulars
from: e

@ Verbs
listen: audio, audire, audivi, auditus

@ Nouns
shrine: templum, templi, (n)

@ Adjectives
joyful: laetus, laeta, laetum, (2-1-2)

@ Pronouns
that: ille

@ Regulars
out: e""",
    )
