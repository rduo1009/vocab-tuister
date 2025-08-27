# pyright: reportUnknownParameterType=false, reportUnknownArgumentType=false, reportMissingParameterType=false

import pytest
from src.core.accido.misc import Case, Degree, EndingComponents, Gender, Number
from src.core.transfero.exceptions import InvalidComponentsError
from src.core.transfero.words import find_inflection, find_pronoun_inflections


def test_invalid_type():
    with pytest.raises(InvalidComponentsError) as error:
        find_pronoun_inflections("house", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.NEUTER, degree=Degree.POSITIVE))
    assert str(error.value) == "Invalid type: 'adjective'"


PRONOUN_COMBINATIONS = (
    (Case.NOMINATIVE, Number.SINGULAR, Gender.MASCULINE),
    (Case.VOCATIVE, Number.SINGULAR, Gender.MASCULINE),
    (Case.ACCUSATIVE, Number.SINGULAR, Gender.MASCULINE),
    (Case.GENITIVE, Number.SINGULAR, Gender.MASCULINE),
    (Case.DATIVE, Number.SINGULAR, Gender.MASCULINE),
    (Case.ABLATIVE, Number.SINGULAR, Gender.MASCULINE),
    (Case.NOMINATIVE, Number.PLURAL, Gender.MASCULINE),
    (Case.VOCATIVE, Number.PLURAL, Gender.MASCULINE),
    (Case.ACCUSATIVE, Number.PLURAL, Gender.MASCULINE),
    (Case.GENITIVE, Number.PLURAL, Gender.MASCULINE),
    (Case.DATIVE, Number.PLURAL, Gender.MASCULINE),
    (Case.ABLATIVE, Number.PLURAL, Gender.MASCULINE),
)


class TestPronounInflection:
    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        {"this"},
        {"this"},
        {"this"},
        {"of this"},
        {"for this", "to this"},
        {"by this", "by means of this", "with this", "this"},
        {"these"},
        {"these"},
        {"these"},
        {"of these"},
        {"for these", "to these"},
        {"by these", "by means of these", "with these", "these"},
    ])])  # fmt: skip
    def test_pronoun_inflections_1(self, case, number, gender, expected):
        assert find_inflection("this", EndingComponents(case=case, number=number, gender=gender)) == expected

    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "this", "this", "this", "of this", "for this", "by this",
        "these", "these", "these", "of these", "for these", "by these",
    ])])  # fmt: skip
    def test_main_pronoun_inflections_1(self, case, number, gender, expected):
        assert find_inflection("this", EndingComponents(case=case, number=number, gender=gender), main=True) == expected

    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        {"that"},
        {"that"},
        {"that"},
        {"of that"}, 
        {"for that", "to that"}, 
        {"by that", "by means of that", "with that", "that"},
        {"those"},
        {"those"},
        {"those"},
        {"of those"},
        {"for those", "to those"},
        {"by those", "by means of those", "with those", "those"},
    ])])  # fmt: skip
    def test_pronoun_inflections_2(self, case, number, gender, expected):
        assert find_inflection("that", EndingComponents(case=case, number=number, gender=gender)) == expected

    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "that", "that", "that", "of that", "for that", "by that",
        "those", "those", "those", "of those", "for those", "by those",
    ])])  # fmt: skip
    def test_main_pronoun_inflections_2(self, case, number, gender, expected):
        assert find_inflection("that", EndingComponents(case=case, number=number, gender=gender), main=True) == expected


class TestNounlikePronounInflection:
    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        {"I"},
        {"I"},
        {"me"},
        {"of me", "my"},
        {"for me", "to me"},
        {"me", "with me", "by me", "by means of me"},
        {"we"},
        {"we"},
        {"us"},
        {"of us", "our"},
        {"for us", "to us"},
        {"us", "with us", "by us", "by means of us"},
    ])])  # fmt: skip
    def test_pronoun_inflections_1(self, case, number, gender, expected):
        assert find_inflection("I", EndingComponents(case=case, number=number, gender=gender)) == expected

    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "I", "I", "me", "of me", "for me", "by me",
        "we", "we", "us", "of us", "for us", "by us",
    ])])  # fmt: skip
    def test_main_pronoun_inflections_1(self, case, number, gender, expected):
        assert find_inflection("I", EndingComponents(case=case, number=number, gender=gender), main=True) == expected

    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        {"you"},
        {"you"},
        {"you"},
        {"of you", "your"},
        {"for you", "to you"},
        {"you", "with you", "by you", "by means of you"},
        {"you all"},
        {"you all"},
        {"you all"},
        {"of you all", "your"},
        {"for you all", "to you all"},
        {"you all", "with you all", "by you all", "by means of you all"},
    ])])  # fmt: skip
    def test_pronoun_inflections_2(self, case, number, gender, expected):
        assert find_inflection("you", EndingComponents(case=case, number=number, gender=gender)) == expected

    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "you", "you", "you", "of you", "for you", "by you",
        "you all", "you all", "you all", "of you all", "for you all", "by you all",
    ])])  # fmt: skip
    def test_main_pronoun_inflections_2(self, case, number, gender, expected):
        assert find_inflection("you", EndingComponents(case=case, number=number, gender=gender), main=True) == expected

    # NOTE: No nominative, so cannot parametrize probably
    def test_pronoun_inflections_3(self):
        word = "oneself"

        assert find_inflection(word, EndingComponents(case=Case.ACCUSATIVE, number=Number.SINGULAR, gender=Gender.MASCULINE)) == {"oneself", "himself", "herself", "itself"}
        assert find_inflection(word, EndingComponents(case=Case.GENITIVE, number=Number.SINGULAR, gender=Gender.MASCULINE)) == {"of oneself", "one's", "of himself", "his", "of herself", "her", "of itself", "its"}
        assert find_inflection(word, EndingComponents(case=Case.DATIVE, number=Number.SINGULAR, gender=Gender.MASCULINE)) == {"for oneself", "for himself", "for herself", "for itself", "to oneself", "to himself", "to herself", "to itself"}
        assert find_inflection(word, EndingComponents(case=Case.ABLATIVE, number=Number.SINGULAR, gender=Gender.MASCULINE)) == {
            "oneself", "himself", "herself", "itself",
            "with oneself", "with himself", "with herself", "with itself",
            "by oneself", "by himself", "by herself", "by itself",
            "by means of oneself", "by means of himself", "by means of herself", "by means of itself",
        }  # fmt: skip
        assert find_inflection(word, EndingComponents(case=Case.ACCUSATIVE, number=Number.PLURAL, gender=Gender.MASCULINE)) == {"themselves"}
        assert find_inflection(word, EndingComponents(case=Case.GENITIVE, number=Number.PLURAL, gender=Gender.MASCULINE)) == {"of themselves", "their"}
        assert find_inflection(word, EndingComponents(case=Case.DATIVE, number=Number.PLURAL, gender=Gender.MASCULINE)) == {"for themselves", "to themselves"}
        assert find_inflection(word, EndingComponents(case=Case.ABLATIVE, number=Number.PLURAL, gender=Gender.MASCULINE)) == {"themselves", "with themselves", "by themselves", "by means of themselves"}

    def test_main_pronoun_inflections_3(self):
        word = "oneself"

        assert find_inflection(word, EndingComponents(case=Case.ACCUSATIVE, number=Number.SINGULAR, gender=Gender.MASCULINE), main=True) == "oneself"
        assert find_inflection(word, EndingComponents(case=Case.GENITIVE, number=Number.SINGULAR, gender=Gender.MASCULINE), main=True) == "of oneself"
        assert find_inflection(word, EndingComponents(case=Case.DATIVE, number=Number.SINGULAR, gender=Gender.MASCULINE), main=True) == "for oneself"
        assert find_inflection(word, EndingComponents(case=Case.ABLATIVE, number=Number.SINGULAR, gender=Gender.MASCULINE), main=True) == "by oneself"
        assert find_inflection(word, EndingComponents(case=Case.ACCUSATIVE, number=Number.PLURAL, gender=Gender.MASCULINE), main=True) == "themselves"
        assert find_inflection(word, EndingComponents(case=Case.GENITIVE, number=Number.PLURAL, gender=Gender.MASCULINE), main=True) == "of themselves"
        assert find_inflection(word, EndingComponents(case=Case.DATIVE, number=Number.PLURAL, gender=Gender.MASCULINE), main=True) == "for themselves"
        assert find_inflection(word, EndingComponents(case=Case.ABLATIVE, number=Number.PLURAL, gender=Gender.MASCULINE), main=True) == "by themselves"
