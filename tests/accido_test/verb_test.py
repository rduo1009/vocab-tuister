import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from src.core.accido.endings import Noun, Verb
from src.core.accido.exceptions import InvalidInputError
from src.core.accido.misc import Case, EndingComponents, Gender, Mood, MultipleMeanings, Number, Tense, Voice
from src.utils import compare


class TestVerbErrors:
    def test_errors_invalid_infinitive(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("celo", "error", "celavi", "celatus", meaning="hide")
        assert str(error.value) == "Invalid infinitive form: 'error'"

    def test_errors_invalid_present(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("errorr", "celare", "celavi", "celatus", meaning="hide")  # error ends in -or!
        assert str(error.value) == "Invalid present form: 'errorr' (must end in '-o')"

    def test_errors_invalid_perfect(self):
        with pytest.raises(InvalidInputError) as error:
            Verb("celo", "celare", "error", "celatus", meaning="hide")
        assert str(error.value) == "Invalid perfect form: 'error' (must end in '-i')"


class TestVerbDunder:
    def test_getnone(self):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert not word.get(tense=Tense.FUTURE_PERFECT, voice=Voice.PASSIVE, mood=Mood.SUBJUNCTIVE, person=2, number=Number.PLURAL)

    def test_repr(self):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert repr(word) == "Verb(celo, celare, celavi, celatus, meaning=hide)"

    def test_repr_noppp(self):
        word = Verb("loquor", "loqui", "locutus sum", meaning="say")
        assert repr(word) == "Verb(loquor, loqui, locutus sum, meaning=say)"

    def test_repr_irregular(self):
        word = Verb("inquam", meaning="say")
        assert repr(word) == "Verb(inquam, meaning=say)"

    def test_str(self):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert str(word) == "hide: celo, celare, celavi, celatus"

    def test_str_noppp(self):
        word = Verb("loquor", "loqui", "locutus sum", meaning="say")
        assert str(word) == "say: loquor, loqui, locutus sum"

    def test_str_irregular(self):
        word = Verb("inquam", meaning="say")
        assert str(word) == "say: inquam"

    def test_eq(self):
        word1 = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        word2 = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert word1 == word2

    def test_lt(self):
        word1 = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        word2 = Verb("amo", "amare", "amavi", "amatus", meaning="love")
        # word2 must be smaller than word1 as word1.first = "test1" and word2.first = "aaatest1"
        assert word1 > word2

    def test_find(self):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert compare(word.find("celabam"), [EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1, string="imperfect active indicative singular 1st person")])

    def test_find_participle(self):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert compare(word.find("celatus"), [EndingComponents(tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, gender=Gender.MASCULINE, case=Case.NOMINATIVE, number=Number.SINGULAR, string="perfect passive participle masculine nominative singular")])

    # def test_find_infinitive(self):
    #     word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
    #     assert compare(word.find("celare"), [EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INFINITIVE, string="present active infinitive")])

    def test_add_different_word(self):
        word1 = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        word2 = Verb("amo", "amare", "amavi", "amatus", meaning="love")
        with pytest.raises(TypeError):
            word1 + word2

    def test_add_different_pos(self):
        word1 = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        word2 = Noun("puella", "puellae", gender=Gender.FEMININE, meaning="girl")
        with pytest.raises(TypeError):
            word1 + word2

    def test_add(self):
        word1 = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        word2 = Verb("celo", "celare", "celavi", "celatus", meaning="conceal")
        assert word1 + word2 == Verb("celo", "celare", "celavi", "celatus", meaning=MultipleMeanings(("hide", "conceal")))

    def test_add_irregular(self):
        word1 = Verb("inquam", meaning="say")
        word2 = Verb("inquam", meaning="speak")
        assert word1 + word2 == Verb("inquam", meaning=MultipleMeanings(("say", "speak")))


class TestSemiDeponentVerb:
    """Test semi-deponent verbs."""

    def test_audeo(self) -> None:
        """Test `audeo`."""
        verb = Verb("audeo", "audere", "ausus sum", meaning="dare")
        assert verb.semi_deponent is True
        assert verb.deponent is False
        assert verb.conjugation == 2

        # Present active indicative
        assert verb["Vpreactindsg1"] == "audeo"
        assert verb["Vpreactindsg2"] == "audes"
        assert verb["Vpreactindsg3"] == "audet"
        assert verb["Vpreactindpl1"] == "audemus"
        assert verb["Vpreactindpl2"] == "audetis"
        assert verb["Vpreactindpl3"] == "audent"

        # Imperfect active indicative
        assert verb["Vimpactindsg1"] == "audebam"

        # Future active indicative
        assert verb["Vfutactindsg1"] == "audebo"

        # Perfect "semi-deponent" (passive form) indicative
        assert verb["Vpersdpindsg1"] == "ausus sum"
        assert verb["Vpersdpindsg2"] == "ausus es"
        assert verb["Vpersdpindsg3"] == "ausus est"
        assert verb["Vpersdpindpl1"] == "ausi sumus"
        assert verb["Vpersdpindpl2"] == "ausi estis"
        assert verb["Vpersdpindpl3"] == "ausi sunt"

        # Pluperfect "semi-deponent" (passive form) indicative
        assert verb["Vplpsdpindsg1"] == "ausus eram"

        # Future Perfect "semi-deponent" (passive form) indicative
        assert verb["Vfprsdpindsg1"] == "ausus ero"

        # Present active subjunctive
        assert verb["Vpreactsbjsg1"] == "audeam"

        # Perfect "semi-deponent" (passive form) subjunctive
        assert verb["Vpersdpsbjsg1"] == "ausus sim"

        # Present active infinitive
        assert verb.get(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INFINITIVE) == "audere"

        # Perfect "semi-deponent" (passive form) infinitive
        # Key for perfect passive/deponent infinitive is Vperpasinf or Vperdepinf
        # For semi-deponent, it should be Vpersdpinf
        assert verb.get(tense=Tense.PERFECT, voice=Voice.SEMI_DEPONENT, mood=Mood.INFINITIVE) == "ausus esse"

        # Future active infinitive
        assert verb.get(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.INFINITIVE) == "ausurus esse"

        # Present active participle
        assert verb["Vpreactptcmnomsg"] == "audens"

        # Perfect passive participle (used as perfect sdp participle)
        # For semi-deponents, this is keyed as Vperpasptc... because its form is passive
        assert verb["Vperpasptcmnomsg"] == "ausus"

        # Future active participle
        assert verb["Vfutactptcmnomsg"] == "ausurus"

        # Gerund
        assert verb["Vgeracc"] == "audendum"

        # Supine
        assert verb["Vsupacc"] == "ausum"

        # Check that purely passive present system forms are not there
        assert verb.get(tense=Tense.PRESENT, voice=Voice.PASSIVE, mood=Mood.INDICATIVE, person=1, number=Number.SINGULAR) is None
        # Check that purely active perfect system forms are not there
        assert verb.get(tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, person=1, number=Number.SINGULAR) is None

    def test_soleo(self) -> None:
        """Test `soleo` (semi-deponent, no future)."""
        verb = Verb("soleo", "solere", "solitus sum", meaning="be accustomed")
        assert verb.semi_deponent is True
        assert verb.no_future is True  # This flag is set in __init__

        assert verb["Vpreactindsg1"] == "soleo"
        assert verb["Vpersdpindsg1"] == "solitus sum"

        # Future forms should be missing due to no_future flag processing
        assert verb.get(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, person=1, number=Number.SINGULAR) is None
        assert verb.get(tense=Tense.FUTURE_PERFECT, voice=Voice.SEMI_DEPONENT, mood=Mood.INDICATIVE, person=1, number=Number.SINGULAR) is None

        # Future active infinitive ('soliturus esse') should be missing if future tense is missing
        assert verb.get(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.INFINITIVE) is None

        # Future active participle ('soliturus') should also be missing if future tense is missing
        assert verb.get(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, participle_gender=Gender.MASCULINE, participle_case=Case.NOMINATIVE, number=Number.SINGULAR) is None

    def test_gaudeo(self) -> None:
        """Test `gaudeo`."""
        verb = Verb("gaudeo", "gaudere", "gavisus sum", meaning="rejoice")
        assert verb.semi_deponent is True
        assert verb["Vpreactindsg1"] == "gaudeo"
        assert verb["Vpersdpindsg1"] == "gavisus sum"
        assert verb["Vfutactptcmnomsg"] == "gavisurus"  # Should have FAP

    def test_fido(self) -> None:
        """Test `fido` (3rd conjugation semi-deponent)."""
        verb = Verb("fido", "fidere", "fisus sum", meaning="trust")
        assert verb.semi_deponent is True
        # Based on "fidere" (short e), it should be 3rd conjugation.
        # The logic in __init__ for semi-deponents:
        # elif self.infinitive.endswith("ere"):
        #     if self.present.endswith("eo"): self.conjugation = 2
        #     else: self.conjugation = 3
        # Since "fido" doesn't end with "eo", it should be 3rd.
        assert verb.conjugation == 3

        assert verb["Vpreactindsg1"] == "fido"
        assert verb["Vpreactindsg2"] == "fidis"  # 3rd conj present
        assert verb["Vpersdpindsg1"] == "fisus sum"
        assert verb["Vfutactindsg1"] == "fidam"  # 3rd conj future active
        assert verb["Vfutactptcmnomsg"] == "fisurus"

    def test_semi_deponent_errors(self) -> None:
        """Test error conditions for semi-deponent verbs."""
        # PPP provided
        with pytest.raises(
            InvalidInputError,
            # Updated regex to be more flexible with parentheses and extra text
            match=r"Verb 'audeo' is semi-deponent, but ppp \('ausus'\) was provided",
        ):
            Verb("audeo", "audere", "ausus sum", "ausus", meaning="dare")

        # Present not ending in -o (and not irregular)
        with pytest.raises(InvalidInputError, match="Invalid present form for semi-deponent verb: 'auder' \\(must end in '-o'\\)"):
            Verb("auder", "audere", "ausus sum", meaning="dare")

        # Perfect not ending in " sum" - this should make it NOT a semi-deponent.
        # It will then be processed as a regular verb and fail there if the perfect is malformed for regular.
        with pytest.raises(
            InvalidInputError,
            match="Invalid perfect form: 'ausus' \\(must end in '-i'\\)",  # Error from regular verb validation path
        ):
            Verb("audeo", "audere", "ausus", meaning="dare")  # Not ending in " sum"

        # Infinitive missing (and not irregular)
        with pytest.raises(InvalidInputError, match="Verb 'audeo' is not irregular, but no infinitive provided\\."):
            Verb("audeo", perfect="ausus sum", meaning="dare")
