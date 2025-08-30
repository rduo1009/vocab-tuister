import pytest
from src.core.accido.endings import Adjective
from src.core.accido.misc import Case, Degree, Gender, Number

ADJECTIVE_COMBINATIONS = (
    (Degree.POSITIVE, Gender.MASCULINE, Case.NOMINATIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.MASCULINE, Case.VOCATIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.MASCULINE, Case.ACCUSATIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.MASCULINE, Case.GENITIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.MASCULINE, Case.DATIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.MASCULINE, Case.ABLATIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.MASCULINE, Case.NOMINATIVE, Number.PLURAL), (Degree.POSITIVE, Gender.MASCULINE, Case.VOCATIVE, Number.PLURAL), (Degree.POSITIVE, Gender.MASCULINE, Case.ACCUSATIVE, Number.PLURAL), (Degree.POSITIVE, Gender.MASCULINE, Case.GENITIVE, Number.PLURAL), (Degree.POSITIVE, Gender.MASCULINE, Case.DATIVE, Number.PLURAL), (Degree.POSITIVE, Gender.MASCULINE, Case.ABLATIVE, Number.PLURAL),
    (Degree.POSITIVE, Gender.FEMININE, Case.NOMINATIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.FEMININE, Case.VOCATIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.FEMININE, Case.ACCUSATIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.FEMININE, Case.GENITIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.FEMININE, Case.DATIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.FEMININE, Case.ABLATIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.FEMININE, Case.NOMINATIVE, Number.PLURAL), (Degree.POSITIVE, Gender.FEMININE, Case.VOCATIVE, Number.PLURAL), (Degree.POSITIVE, Gender.FEMININE, Case.ACCUSATIVE, Number.PLURAL), (Degree.POSITIVE, Gender.FEMININE, Case.GENITIVE, Number.PLURAL), (Degree.POSITIVE, Gender.FEMININE, Case.DATIVE, Number.PLURAL), (Degree.POSITIVE, Gender.FEMININE, Case.ABLATIVE, Number.PLURAL),
    (Degree.POSITIVE, Gender.NEUTER, Case.NOMINATIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.NEUTER, Case.VOCATIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.NEUTER, Case.ACCUSATIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.NEUTER, Case.GENITIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.NEUTER, Case.DATIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.NEUTER, Case.ABLATIVE, Number.SINGULAR), (Degree.POSITIVE, Gender.NEUTER, Case.NOMINATIVE, Number.PLURAL), (Degree.POSITIVE, Gender.NEUTER, Case.VOCATIVE, Number.PLURAL), (Degree.POSITIVE, Gender.NEUTER, Case.ACCUSATIVE, Number.PLURAL), (Degree.POSITIVE, Gender.NEUTER, Case.GENITIVE, Number.PLURAL), (Degree.POSITIVE, Gender.NEUTER, Case.DATIVE, Number.PLURAL), (Degree.POSITIVE, Gender.NEUTER, Case.ABLATIVE, Number.PLURAL),
    (Degree.COMPARATIVE, Gender.MASCULINE, Case.NOMINATIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.MASCULINE, Case.VOCATIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.MASCULINE, Case.ACCUSATIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.MASCULINE, Case.GENITIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.MASCULINE, Case.DATIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.MASCULINE, Case.ABLATIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.MASCULINE, Case.NOMINATIVE, Number.PLURAL), (Degree.COMPARATIVE, Gender.MASCULINE, Case.VOCATIVE, Number.PLURAL), (Degree.COMPARATIVE, Gender.MASCULINE, Case.ACCUSATIVE, Number.PLURAL), (Degree.COMPARATIVE, Gender.MASCULINE, Case.GENITIVE, Number.PLURAL), (Degree.COMPARATIVE, Gender.MASCULINE, Case.DATIVE, Number.PLURAL), (Degree.COMPARATIVE, Gender.MASCULINE, Case.ABLATIVE, Number.PLURAL),
    (Degree.COMPARATIVE, Gender.FEMININE, Case.NOMINATIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.FEMININE, Case.VOCATIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.FEMININE, Case.ACCUSATIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.FEMININE, Case.GENITIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.FEMININE, Case.DATIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.FEMININE, Case.ABLATIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.FEMININE, Case.NOMINATIVE, Number.PLURAL), (Degree.COMPARATIVE, Gender.FEMININE, Case.VOCATIVE, Number.PLURAL), (Degree.COMPARATIVE, Gender.FEMININE, Case.ACCUSATIVE, Number.PLURAL), (Degree.COMPARATIVE, Gender.FEMININE, Case.GENITIVE, Number.PLURAL), (Degree.COMPARATIVE, Gender.FEMININE, Case.DATIVE, Number.PLURAL), (Degree.COMPARATIVE, Gender.FEMININE, Case.ABLATIVE, Number.PLURAL),
    (Degree.COMPARATIVE, Gender.NEUTER, Case.NOMINATIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.NEUTER, Case.VOCATIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.NEUTER, Case.ACCUSATIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.NEUTER, Case.GENITIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.NEUTER, Case.DATIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.NEUTER, Case.ABLATIVE, Number.SINGULAR), (Degree.COMPARATIVE, Gender.NEUTER, Case.NOMINATIVE, Number.PLURAL), (Degree.COMPARATIVE, Gender.NEUTER, Case.VOCATIVE, Number.PLURAL), (Degree.COMPARATIVE, Gender.NEUTER, Case.ACCUSATIVE, Number.PLURAL), (Degree.COMPARATIVE, Gender.NEUTER, Case.GENITIVE, Number.PLURAL), (Degree.COMPARATIVE, Gender.NEUTER, Case.DATIVE, Number.PLURAL), (Degree.COMPARATIVE, Gender.NEUTER, Case.ABLATIVE, Number.PLURAL),
    (Degree.SUPERLATIVE, Gender.MASCULINE, Case.NOMINATIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.MASCULINE, Case.VOCATIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.MASCULINE, Case.ACCUSATIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.MASCULINE, Case.GENITIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.MASCULINE, Case.DATIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.MASCULINE, Case.ABLATIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.MASCULINE, Case.NOMINATIVE, Number.PLURAL), (Degree.SUPERLATIVE, Gender.MASCULINE, Case.VOCATIVE, Number.PLURAL), (Degree.SUPERLATIVE, Gender.MASCULINE, Case.ACCUSATIVE, Number.PLURAL), (Degree.SUPERLATIVE, Gender.MASCULINE, Case.GENITIVE, Number.PLURAL), (Degree.SUPERLATIVE, Gender.MASCULINE, Case.DATIVE, Number.PLURAL), (Degree.SUPERLATIVE, Gender.MASCULINE, Case.ABLATIVE, Number.PLURAL),
    (Degree.SUPERLATIVE, Gender.FEMININE, Case.NOMINATIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.FEMININE, Case.VOCATIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.FEMININE, Case.ACCUSATIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.FEMININE, Case.GENITIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.FEMININE, Case.DATIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.FEMININE, Case.ABLATIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.FEMININE, Case.NOMINATIVE, Number.PLURAL), (Degree.SUPERLATIVE, Gender.FEMININE, Case.VOCATIVE, Number.PLURAL), (Degree.SUPERLATIVE, Gender.FEMININE, Case.ACCUSATIVE, Number.PLURAL), (Degree.SUPERLATIVE, Gender.FEMININE, Case.GENITIVE, Number.PLURAL), (Degree.SUPERLATIVE, Gender.FEMININE, Case.DATIVE, Number.PLURAL), (Degree.SUPERLATIVE, Gender.FEMININE, Case.ABLATIVE, Number.PLURAL),
    (Degree.SUPERLATIVE, Gender.NEUTER, Case.NOMINATIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.NEUTER, Case.VOCATIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.NEUTER, Case.ACCUSATIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.NEUTER, Case.GENITIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.NEUTER, Case.DATIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.NEUTER, Case.ABLATIVE, Number.SINGULAR), (Degree.SUPERLATIVE, Gender.NEUTER, Case.NOMINATIVE, Number.PLURAL), (Degree.SUPERLATIVE, Gender.NEUTER, Case.VOCATIVE, Number.PLURAL), (Degree.SUPERLATIVE, Gender.NEUTER, Case.ACCUSATIVE, Number.PLURAL), (Degree.SUPERLATIVE, Gender.NEUTER, Case.GENITIVE, Number.PLURAL), (Degree.SUPERLATIVE, Gender.NEUTER, Case.DATIVE, Number.PLURAL), (Degree.SUPERLATIVE, Gender.NEUTER, Case.ABLATIVE, Number.PLURAL),
)  # fmt: skip

ADVERB_COMBINATIONS = (Degree.POSITIVE, Degree.COMPARATIVE, Degree.SUPERLATIVE)


@pytest.fixture
def adjective_declension212():
    return Adjective("laetus", "laeta", "laetum", declension="212", meaning="happy")


@pytest.fixture
def adjective_declension212_noadverb():
    return Adjective("magnus", "magna", "magnum", declension="212", meaning="big")


@pytest.fixture
def adjective_declension212_irregular():
    return Adjective("bonus", "bona", "bonum", declension="212", meaning="good")


@pytest.fixture
def adjective_declension31():
    return Adjective("egens", "egentis", termination=1, declension="3", meaning="poor")


@pytest.fixture
def adjective_declension31_irregular():
    return Adjective("uber", "uberis", termination=1, declension="3", meaning="fruitful")


@pytest.fixture
def adjective_declension31_adverb():
    return Adjective("prudens", "prudentis", termination=1, declension="3", meaning="wise")


@pytest.fixture
def adjective_declension32():
    return Adjective("facilis", "facile", termination=2, declension="3", meaning="easy")


@pytest.fixture
def adjective_declension33():
    return Adjective("celer", "celeris", "celere", termination=3, declension="3", meaning="quick")


class TestAdjectiveDeclension:
    @pytest.mark.parametrize(("degree", "gender", "case", "number", "expected"), [ADJECTIVE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "laetus", "laete", "laetum", "laeti", "laeto", "laeto", "laeti", "laeti", "laetos", "laetorum", "laetis", "laetis",
        "laeta", "laeta", "laetam", "laetae", "laetae", "laeta", "laetae", "laetae", "laetas", "laetarum", "laetis", "laetis",
        "laetum", "laetum", "laetum", "laeti", "laeto", "laeto", "laeta", "laeta", "laeta", "laetorum", "laetis", "laetis",
        "laetior", "laetior", "laetiorem", "laetioris", "laetiori", "laetiore", "laetiores", "laetiores", "laetiores", "laetiorum", "laetioribus", "laetioribus",
        "laetior", "laetior", "laetiorem", "laetioris", "laetiori", "laetiore", "laetiores", "laetiores", "laetiores", "laetiorum", "laetioribus", "laetioribus",
        "laetius", "laetius", "laetius", "laetioris", "laetiori", "laetiore", "laetiora", "laetiora", "laetiora", "laetiorum", "laetioribus", "laetioribus",
        "laetissimus", "laetissime", "laetissimum", "laetissimi", "laetissimo", "laetissimo", "laetissimi", "laetissimi", "laetissimos", "laetissimorum", "laetissimis", "laetissimis",
        "laetissima", "laetissima", "laetissimam", "laetissimae", "laetissimae", "laetissima", "laetissimae", "laetissimae", "laetissimas", "laetissimarum", "laetissimis", "laetissimis",
        "laetissimum", "laetissimum", "laetissimum", "laetissimi", "laetissimo", "laetissimo", "laetissima", "laetissima", "laetissima", "laetissimorum", "laetissimis", "laetissimis",
    ])])  # fmt: skip
    def test_declension212(self, adjective_declension212, degree, gender, case, number, expected):
        assert adjective_declension212.get(degree=degree, gender=gender, case=case, number=number) == expected

    @pytest.mark.parametrize(("degree", "gender", "case", "number", "expected"), [ADJECTIVE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "bonus", "bone", "bonum", "boni", "bono", "bono", "boni", "boni", "bonos", "bonorum", "bonis", "bonis",
        "bona", "bona", "bonam", "bonae", "bonae", "bona", "bonae", "bonae", "bonas", "bonarum", "bonis", "bonis",
        "bonum", "bonum", "bonum", "boni", "bono", "bono", "bona", "bona", "bona", "bonorum", "bonis", "bonis",
        "melior", "melior", "meliorem", "melioris", "meliori", "meliore", "meliores", "meliores", "meliores", "meliorum", "melioribus", "melioribus",
        "melior", "melior", "meliorem", "melioris", "meliori", "meliore", "meliores", "meliores", "meliores", "meliorum", "melioribus", "melioribus",
        "melius", "melius", "melius", "melioris", "meliori", "meliore", "meliora", "meliora", "meliora", "meliorum", "melioribus", "melioribus",
        "optimus", "optime", "optimum", "optimi", "optimo", "optimo", "optimi", "optimi", "optimos", "optimorum", "optimis", "optimis",
        "optima", "optima", "optimam", "optimae", "optimae", "optima", "optimae", "optimae", "optimas", "optimarum", "optimis", "optimis",
        "optimum", "optimum", "optimum", "optimi", "optimo", "optimo", "optima", "optima", "optima", "optimorum", "optimis", "optimis",
    ])])  # fmt: skip
    def test_declension212_irregular(self, adjective_declension212_irregular, degree, gender, case, number, expected):
        assert adjective_declension212_irregular.get(degree=degree, gender=gender, case=case, number=number) == expected

    @pytest.mark.parametrize(("degree", "gender", "case", "number", "expected"), [ADJECTIVE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "egens", "egens", "egentem", "egentis", "egenti", "egenti", "egentes", "egentes", "egentes", "egentium", "egentibus", "egentibus",
        "egens", "egens", "egentem", "egentis", "egenti", "egenti", "egentes", "egentes", "egentes", "egentium", "egentibus", "egentibus",
        "egens", "egens", "egens", "egentis", "egenti", "egenti", "egentia", "egentia", "egentia", "egentium", "egentibus", "egentibus",
        "egentior", "egentior", "egentiorem", "egentioris", "egentiori", "egentiore", "egentiores", "egentiores", "egentiores", "egentiorum", "egentioribus", "egentioribus",
        "egentior", "egentior", "egentiorem", "egentioris", "egentiori", "egentiore", "egentiores", "egentiores", "egentiores", "egentiorum", "egentioribus", "egentioribus",
        "egentius", "egentius", "egentius", "egentioris", "egentiori", "egentiore", "egentiora", "egentiora", "egentiora", "egentiorum", "egentioribus", "egentioribus",
        "egentissimus", "egentissime", "egentissimum", "egentissimi", "egentissimo", "egentissimo", "egentissimi", "egentissimi", "egentissimos", "egentissimorum", "egentissimis", "egentissimis",
        "egentissima", "egentissima", "egentissimam", "egentissimae", "egentissimae", "egentissima", "egentissimae", "egentissimae", "egentissimas", "egentissimarum", "egentissimis", "egentissimis",
        "egentissimum", "egentissimum", "egentissimum", "egentissimi", "egentissimo", "egentissimo", "egentissima", "egentissima", "egentissima", "egentissimorum", "egentissimis", "egentissimis",
    ])])  # fmt: skip
    def test_declension31_regular(self, adjective_declension31, degree, gender, case, number, expected):
        assert adjective_declension31.get(degree=degree, gender=gender, case=case, number=number) == expected

    @pytest.mark.parametrize(("degree", "gender", "case", "number", "expected"), [ADJECTIVE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "uber", "uber", "uberem", "uberis", "uberi", "uberi", "uberes", "uberes", "uberes", "uberium", "uberibus", "uberibus",
        "uber", "uber", "uberem", "uberis", "uberi", "uberi", "uberes", "uberes", "uberes", "uberium", "uberibus", "uberibus",
        "uber", "uber", "uber", "uberis", "uberi", "uberi", "uberia", "uberia", "uberia", "uberium", "uberibus", "uberibus",
        "uberior", "uberior", "uberiorem", "uberioris", "uberiori", "uberiore", "uberiores", "uberiores", "uberiores", "uberiorum", "uberioribus", "uberioribus",
        "uberior", "uberior", "uberiorem", "uberioris", "uberiori", "uberiore", "uberiores", "uberiores", "uberiores", "uberiorum", "uberioribus", "uberioribus",
        "uberius", "uberius", "uberius", "uberioris", "uberiori", "uberiore", "uberiora", "uberiora", "uberiora", "uberiorum", "uberioribus", "uberioribus",
        "uberrimus", "uberrime", "uberrimum", "uberrimi", "uberrimo", "uberrimo", "uberrimi", "uberrimi", "uberrimos", "uberrimorum", "uberrimis", "uberrimis",
        "uberrima", "uberrima", "uberrimam", "uberrimae", "uberrimae", "uberrima", "uberrimae", "uberrimae", "uberrimas", "uberrimarum", "uberrimis", "uberrimis",
        "uberrimum", "uberrimum", "uberrimum", "uberrimi", "uberrimo", "uberrimo", "uberrima", "uberrima", "uberrima", "uberrimorum", "uberrimis", "uberrimis",
    ])])  # fmt: skip
    def test_declension31_with_rr(self, adjective_declension31_irregular, degree, gender, case, number, expected):
        assert adjective_declension31_irregular.get(degree=degree, gender=gender, case=case, number=number) == expected

    @pytest.mark.parametrize(("degree", "gender", "case", "number", "expected"), [ADJECTIVE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "facilis", "facilis", "facilem", "facilis", "facili", "facili", "faciles", "faciles", "faciles", "facilium", "facilibus", "facilibus",
        "facilis", "facilis", "facilem", "facilis", "facili", "facili", "faciles", "faciles", "faciles", "facilium", "facilibus", "facilibus",
        "facile", "facile", "facile", "facilis", "facili", "facili", "facilia", "facilia", "facilia", "facilium", "facilibus", "facilibus",
        "facilior", "facilior", "faciliorem", "facilioris", "faciliori", "faciliore", "faciliores", "faciliores", "faciliores", "faciliorum", "facilioribus", "facilioribus",
        "facilior", "facilior", "faciliorem", "facilioris", "faciliori", "faciliore", "faciliores", "faciliores", "faciliores", "faciliorum", "facilioribus", "facilioribus",
        "facilius", "facilius", "facilius", "facilioris", "faciliori", "faciliore", "faciliora", "faciliora", "faciliora", "faciliorum", "facilioribus", "facilioribus",
        "facillimus", "facillime", "facillimum", "facillimi", "facillimo", "facillimo", "facillimi", "facillimi", "facillimos", "facillimorum", "facillimis", "facillimis",
        "facillima", "facillima", "facillimam", "facillimae", "facillimae", "facillima", "facillimae", "facillimae", "facillimas", "facillimarum", "facillimis", "facillimis",
        "facillimum", "facillimum", "facillimum", "facillimi", "facillimo", "facillimo", "facillima", "facillima", "facillima", "facillimorum", "facillimis", "facillimis",
    ])])  # fmt: skip
    def test_declension32(self, adjective_declension32, degree, gender, case, number, expected):
        assert adjective_declension32.get(degree=degree, gender=gender, case=case, number=number) == expected

    @pytest.mark.parametrize(("degree", "gender", "case", "number", "expected"), [ADJECTIVE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "celer", "celer", "celerem", "celeris", "celeri", "celeri", "celeres", "celeres", "celeres", "celerium", "celeribus", "celeribus",
        "celeris", "celeris", "celerem", "celeris", "celeri", "celeri", "celeres", "celeres", "celeres", "celerium", "celeribus", "celeribus",
        "celere", "celere", "celere", "celeris", "celeri", "celeri", "celeria", "celeria", "celeria", "celerium", "celeribus", "celeribus",
        "celerior", "celerior", "celeriorem", "celerioris", "celeriori", "celeriore", "celeriores", "celeriores", "celeriores", "celeriorum", "celerioribus", "celerioribus",
        "celerior", "celerior", "celeriorem", "celerioris", "celeriori", "celeriore", "celeriores", "celeriores", "celeriores", "celeriorum", "celerioribus", "celerioribus",
        "celerius", "celerius", "celerius", "celerioris", "celeriori", "celeriore", "celeriora", "celeriora", "celeriora", "celeriorum", "celerioribus", "celerioribus",
        "celerrimus", "celerrime", "celerrimum", "celerrimi", "celerrimo", "celerrimo", "celerrimi", "celerrimi", "celerrimos", "celerrimorum", "celerrimis", "celerrimis",
        "celerrima", "celerrima", "celerrimam", "celerrimae", "celerrimae", "celerrima", "celerrimae", "celerrimae", "celerrimas", "celerrimarum", "celerrimis", "celerrimis",
        "celerrimum", "celerrimum", "celerrimum", "celerrimi", "celerrimo", "celerrimo", "celerrima", "celerrima", "celerrima", "celerrimorum", "celerrimis", "celerrimis",
    ])])  # fmt: skip
    def test_declension33(self, adjective_declension33, degree, gender, case, number, expected):
        assert adjective_declension33.get(degree=degree, gender=gender, case=case, number=number) == expected


class TestAdverbDeclension:
    @pytest.mark.parametrize(("degree", "expected"), [(ADVERB_COMBINATIONS[i], form) for i, form in enumerate([
        "laete", "laetius", "laetissime"
    ])])  # fmt: skip
    def test_adverb_212(self, adjective_declension212, degree, expected):
        assert adjective_declension212.get(degree=degree, adverb=True) == expected

    @pytest.mark.parametrize(("degree", "expected"), [(ADVERB_COMBINATIONS[i], form) for i, form in enumerate([
        "prudenter", "prudentius", "prudentissime"
    ])])  # fmt: skip
    def test_adverb_31(self, adjective_declension31_adverb, degree, expected):
        assert adjective_declension31_adverb.get(degree=degree, adverb=True) == expected

    @pytest.mark.parametrize(("degree", "expected"), [(ADVERB_COMBINATIONS[i], form) for i, form in enumerate([
        "faciliter", "facilius", "facillime"
    ])])  # fmt: skip
    def test_adverb_32(self, adjective_declension32, degree, expected):
        assert adjective_declension32.get(degree=degree, adverb=True) == expected

    @pytest.mark.parametrize(("degree", "expected"), [(ADVERB_COMBINATIONS[i], form) for i, form in enumerate([
        "celeriter", "celerius", "celerrime"
    ])])  # fmt: skip
    def test_adverb_33(self, adjective_declension33, degree, expected):
        assert adjective_declension33.get(degree=degree, adverb=True) == expected

    @pytest.mark.parametrize(("degree", "expected"), [(ADVERB_COMBINATIONS[i], form) for i, form in enumerate([
        "bene", "melius", "optime"
    ])])  # fmt: skip
    def test_irregularadverb(self, adjective_declension212_irregular, degree, expected):
        assert adjective_declension212_irregular.get(degree=degree, adverb=True) == expected

    @pytest.mark.parametrize(("degree", "expected"), [(ADVERB_COMBINATIONS[i], form) for i, form in enumerate([
        None, None, None
    ])])  # fmt: skip
    def test_irregularadverb_noadverb(self, adjective_declension212_noadverb, degree, expected):
        assert adjective_declension212_noadverb.get(degree=degree, adverb=True) == expected
