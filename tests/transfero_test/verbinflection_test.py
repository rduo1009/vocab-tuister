import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from src.core.accido.misc import Case, EndingComponents, Gender, Mood, Number, Tense, Voice
from src.core.transfero._verb_inflection import find_main_verb_inflection, find_verb_inflections
from src.core.transfero.exceptions import InvalidComponentsError


def test_invalid_type():
    with pytest.raises(InvalidComponentsError) as error:
        find_verb_inflections("teach", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.NEUTER))
    assert str(error.value) == "Invalid type: 'pronoun'"


def test_invalid_type_participle():
    with pytest.raises(InvalidComponentsError) as error:
        find_verb_inflections("teach", EndingComponents(tense=Tense.PRESENT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE))
    assert str(error.value) == "Invalid subtype: 'infinitive'"


def test_invalid_type_infinitive():
    with pytest.raises(InvalidComponentsError) as error:
        find_verb_inflections("teach", EndingComponents(tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.INFINITIVE, number=Number.SINGULAR, case=Case.NOMINATIVE, gender=Gender.MASCULINE))
    assert str(error.value) == "Invalid subtype: 'participle'"


def test_verb_error_not_implemented():
    with pytest.raises(NotImplementedError) as error:
        find_verb_inflections("attack", EndingComponents(tense=Tense.PRESENT, voice=Voice.PASSIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1))
    assert str(error.value) == "The present passive indicative has not been implemented."


def test_participle_error_not_implemented():
    with pytest.raises(NotImplementedError) as error:
        find_verb_inflections("attack", EndingComponents(tense=Tense.PRESENT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, case=Case.NOMINATIVE, gender=Gender.MASCULINE, number=Number.SINGULAR))
    assert str(error.value) == "The present passive participle has not been implemented."


# TODO: Parametrize this?
class TestVerbInflection:
    def test_verb_present(self):
        word = "attack"

        assert find_verb_inflections(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1)) == {"I attack", "I am attacking"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=2)) == {"you attack", "you are attacking"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=3)) == {"he attacks", "he is attacking", "she attacks", "she is attacking", "it attacks", "it is attacking"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=1)) == {"we attack", "we are attacking"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=2)) == {"you attack", "you are attacking"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=3)) == {"they attack", "they are attacking"}

    def test_verb_imperfect(self):
        word = "attack"

        assert find_verb_inflections(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1)) == {"I was attacking"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=2)) == {"you were attacking"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=3)) == {"he was attacking", "she was attacking", "it was attacking"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=1)) == {"we were attacking"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=2)) == {"you were attacking"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=3)) == {"they were attacking"}

    def test_verb_future(self):
        word = "attack"

        assert find_verb_inflections(word, EndingComponents(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1)) == {"I will attack", "I will be attacking", "I shall attack", "I shall be attacking"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=2)) == {"you will attack", "you will be attacking", "you shall attack", "you shall be attacking"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=3)) == {"he will attack", "he will be attacking", "he shall attack", "he shall be attacking", "she will attack", "she will be attacking", "she shall attack", "she shall be attacking", "it will attack", "it will be attacking", "it shall attack", "it shall be attacking"}  # fmt: skip
        assert find_verb_inflections(word, EndingComponents(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=1)) == {"we will attack", "we will be attacking", "we shall attack", "we shall be attacking"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=2)) == {"you will attack", "you will be attacking", "you shall attack", "you shall be attacking"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=3)) == {"they will attack", "they will be attacking", "they shall attack", "they shall be attacking"}

    def test_verb_perfect(self):
        word = "attack"

        assert find_verb_inflections(word, EndingComponents(tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1)) == {"I attacked", "I have attacked", "I did attack"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=2)) == {"you attacked", "you have attacked", "you did attack"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=3)) == {"he attacked", "he has attacked", "he did attack", "she has attacked", "she attacked", "she did attack", "it attacked", "it has attacked", "it did attack"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=1)) == {"we attacked", "we have attacked", "we did attack"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=2)) == {"you attacked", "you have attacked", "you did attack"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=3)) == {"they attacked", "they have attacked", "they did attack"}

    def test_verb_pluperfect(self):
        word = "attack"

        assert find_verb_inflections(word, EndingComponents(tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1)) == {"I had attacked"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=2)) == {"you had attacked"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=3)) == {"he had attacked", "she had attacked", "it had attacked"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=1)) == {"we had attacked"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=2)) == {"you had attacked"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=3)) == {"they had attacked"}

    def test_verb_future_perfect(self):
        word = "attack"

        assert find_verb_inflections(word, EndingComponents(tense=Tense.FUTURE_PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1)) == {"I will have attacked"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.FUTURE_PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=2)) == {"you will have attacked"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.FUTURE_PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=3)) == {"he will have attacked", "she will have attacked", "it will have attacked"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.FUTURE_PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=1)) == {"we will have attacked"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.FUTURE_PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=2)) == {"you will have attacked"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.FUTURE_PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=3)) == {"they will have attacked"}

    def test_verb_infinitive(self):
        word = "attack"

        assert find_verb_inflections(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INFINITIVE)) == {"to attack"}

    def test_verb_present_imperative(self):
        word = "attack"

        assert find_verb_inflections(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE, number=Number.SINGULAR, person=2)) == {"attack"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE, number=Number.PLURAL, person=2)) == {"attack"}

    def test_verb_imperfect_stative(self):
        word = "have"

        assert find_verb_inflections(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1)) == {"I had", "I was having"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=2)) == {"you had", "you were having"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=3)) == {"he was having", "he had", "she was having", "she had", "it was having", "it had"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=1)) == {"we were having", "we had"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=2)) == {"you were having", "you had"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=3)) == {"they were having", "they had"}

    def test_main_verb_present(self):
        word = "attack"

        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1)) == "I attack"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=2)) == "you attack"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=3)) == "he attacks"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=1)) == "we attack"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=2)) == "you attack"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=3)) == "they attack"

    def test_main_verb_imperfect(self):
        word = "attack"

        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1)) == "I was attacking"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=2)) == "you were attacking"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=3)) == "he was attacking"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=1)) == "we were attacking"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=2)) == "you were attacking"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=3)) == "they were attacking"

    def test_main_verb_future(self):
        word = "attack"

        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1)) == "I will attack"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=2)) == "you will attack"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=3)) == "he will attack"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=1)) == "we will attack"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=2)) == "you will attack"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.FUTURE, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=3)) == "they will attack"

    def test_main_verb_perfect(self):
        word = "attack"

        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1)) == "I attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=2)) == "you attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=3)) == "he attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=1)) == "we attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=2)) == "you attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=3)) == "they attacked"

    def test_main_verb_pluperfect(self):
        word = "attack"

        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1)) == "I had attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=2)) == "you had attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=3)) == "he had attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=1)) == "we had attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=2)) == "you had attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PLUPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=3)) == "they had attacked"

    def test_main_verb_future_perfect(self):
        word = "attack"

        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.FUTURE_PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1)) == "I will have attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.FUTURE_PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=2)) == "you will have attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.FUTURE_PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=3)) == "he will have attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.FUTURE_PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=1)) == "we will have attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.FUTURE_PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=2)) == "you will have attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.FUTURE_PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=3)) == "they will have attacked"

    def test_main_verb_infinitive(self):
        word = "attack"

        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INFINITIVE)) == "to attack"

    def test_main_verb_present_imperative(self):
        word = "attack"

        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE, number=Number.SINGULAR, person=2)) == "attack"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.IMPERATIVE, number=Number.PLURAL, person=2)) == "attack"

    def test_main_verb_imperfect_stative(self):
        word = "have"

        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=1)) == "I had"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=2)) == "you had"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=3)) == "he had"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=1)) == "we had"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=2)) == "you had"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.IMPERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.PLURAL, person=3)) == "they had"


class TestParticipleInflection:
    def test_participle_inflections(self):
        word = "attack"

        assert find_verb_inflections(word, EndingComponents(tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, number=Number.SINGULAR, case=Case.NOMINATIVE, gender=Gender.MASCULINE)) == {"having been attacked"}
        assert find_verb_inflections(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, number=Number.SINGULAR, case=Case.NOMINATIVE, gender=Gender.MASCULINE)) == {"attacking"}

    def test_main_participle_inflections(self):
        word = "attack"

        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PERFECT, voice=Voice.PASSIVE, mood=Mood.PARTICIPLE, number=Number.SINGULAR, case=Case.NOMINATIVE, gender=Gender.MASCULINE)) == "having been attacked"
        assert find_main_verb_inflection(word, EndingComponents(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.PARTICIPLE, number=Number.SINGULAR, case=Case.NOMINATIVE, gender=Gender.MASCULINE)) == "attacking"
