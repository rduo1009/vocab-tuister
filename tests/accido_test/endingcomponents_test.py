import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.accido.misc import Case, Degree, EndingComponents, Gender, Number


class TestEndingComponentsDunder:
    def test_eq(self):
        a = EndingComponents(case=Case.ACCUSATIVE, number=Number.PLURAL, gender=Gender.NEUTER)
        b = EndingComponents(case=Case.ACCUSATIVE, number=Number.PLURAL, gender=Gender.NEUTER)
        assert a == b

    def test_noeq(self):
        a = EndingComponents(case=Case.ACCUSATIVE, number=Number.PLURAL, gender=Gender.NEUTER)
        b = EndingComponents(case=Case.ACCUSATIVE, number=Number.PLURAL, gender=Gender.NEUTER, degree=Degree.POSITIVE)
        assert a != b

    def test_hash(self):
        a = EndingComponents(case=Case.ACCUSATIVE, number=Number.PLURAL, gender=Gender.NEUTER)
        b = EndingComponents(case=Case.ACCUSATIVE, number=Number.PLURAL, gender=Gender.NEUTER)
        assert hash(a) == hash(b)

    def test_repr(self):
        a = EndingComponents(case=Case.ACCUSATIVE, number=Number.PLURAL, gender=Gender.NEUTER, string="accusative plural neuter")
        assert repr(a) == "accusative plural neuter"
