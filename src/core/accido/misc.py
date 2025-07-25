"""Contains miscellaneous functions, classes and constants used by ``accido``."""

# pyright: reportUninitializedInstanceVariable=false, reportAny=false

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, auto
from functools import total_ordering
from types import SimpleNamespace
from typing import TYPE_CHECKING, Final, overload

from aenum import MultiValue

if TYPE_CHECKING:
    # To avoid mypy errors.
    from enum import Enum

    from .type_aliases import Person

else:
    from aenum import Enum

if TYPE_CHECKING:

    @total_ordering
    class _EndingComponentEnum(Enum):
        # This is not actually the structure of the enum, but it helps with type
        # hinting. Each enum value has a regular value and a shorthand value.
        regular: str
        shorthand: str

        def __str__(self) -> str: ...

        def __lt__(self, other: object) -> bool: ...


else:

    @total_ordering
    class _EndingComponentEnum(Enum):
        """Represents an enum used in an ``EndingComponents`` object."""

        def __str__(self) -> str:
            # HACK: Makes formatting log messages easier.
            return self.regular

        def __lt__(self, other: object) -> bool:
            if not isinstance(other, _EndingComponentEnum):
                return NotImplemented

            return str(self) < str(other)


class Number(
    _EndingComponentEnum, settings=MultiValue, init="regular shorthand"
):
    """Represents the grammatical number."""

    SINGULAR = "singular", "sg"
    PLURAL = "plural", "pl"


class Tense(
    _EndingComponentEnum, settings=MultiValue, init="regular shorthand"
):
    """Represents the tense of a verb."""

    PRESENT = "present", "pre"
    IMPERFECT = "imperfect", "imp"
    FUTURE = "future", "fut"
    PERFECT = "perfect", "per"
    PLUPERFECT = "pluperfect", "plp"
    FUTURE_PERFECT = "future perfect", "fpr"


class Voice(
    _EndingComponentEnum, settings=MultiValue, init="regular shorthand"
):
    """Represents the voice of a verb."""

    ACTIVE = "active", "act"
    PASSIVE = "passive", "pas"
    DEPONENT = "deponent", "dep"
    SEMI_DEPONENT = "semi-deponent", "sdp"


class Mood(
    _EndingComponentEnum, settings=MultiValue, init="regular shorthand"
):
    """Represents the mood of a verb."""

    INDICATIVE = "indicative", "ind"
    SUBJUNCTIVE = "subjunctive", "sbj"
    IMPERATIVE = "imperative", "ipe"
    INFINITIVE = "infinitive", "inf"
    PARTICIPLE = "participle", "ptc"
    GERUND = "gerund", "ger"
    SUPINE = "supine", "sup"


class Case(
    _EndingComponentEnum, settings=MultiValue, init="regular shorthand"
):
    """Represents the case of a noun."""

    NOMINATIVE = "nominative", "nom"
    VOCATIVE = "vocative", "voc"
    ACCUSATIVE = "accusative", "acc"
    GENITIVE = "genitive", "gen"
    DATIVE = "dative", "dat"
    ABLATIVE = "ablative", "abl"


class Gender(
    _EndingComponentEnum, settings=MultiValue, init="regular shorthand"
):
    """Represents the gender of a noun or adjective."""

    MASCULINE = "masculine", "m"
    FEMININE = "feminine", "f"
    NEUTER = "neuter", "n"


class Degree(
    _EndingComponentEnum, settings=MultiValue, init="regular shorthand"
):
    """Represents the degree of an adjective."""

    POSITIVE = "positive", "pos"
    COMPARATIVE = "comparative", "cmp"
    SUPERLATIVE = "superlative", "spr"


"""Mapping of person values to their more concise abbreviated forms."""
PERSON_SHORTHAND: Final[tuple[str, str, str, str]] = (
    "",
    "1st person",
    "2nd person",
    "3rd person",
)


class ComponentsType(StrEnum):
    """Represents the type of an ``EndingComponents`` object."""

    ADJECTIVE = auto()
    NOUN = auto()
    PRONOUN = auto()
    REGULARWORD = auto()
    VERB = auto()


class ComponentsSubtype(StrEnum):
    """Represents the subtype of an ``EndingComponents`` object."""

    INFINITIVE = auto()
    PARTICIPLE = auto()
    VERBAL_NOUN = auto()
    ADVERB = auto()
    PRONOUN = auto()


class EndingComponents:
    """A container for the grammatical components of an ending.

    Examples
    --------
    >>> foo = EndingComponents(
    ...     case=Case.NOMINATIVE,
    ...     number=Number.SINGULAR,
    ...     string="nominative singular",
    ... )
    >>> foo.number.regular
    'singular'

    For nouns.

    >>> foo = EndingComponents(
    ...     case=Case.NOMINATIVE,
    ...     gender=Gender.MASCULINE,
    ...     number=Number.SINGULAR,
    ...     string="nominative singular masculine",
    ... )
    >>> foo.case.regular
    'nominative'

    For pronouns.

    >>> foo = EndingComponents(
    ...     case=Case.NOMINATIVE,
    ...     gender=Gender.MASCULINE,
    ...     number=Number.SINGULAR,
    ...     degree=Degree.SUPERLATIVE,
    ...     string="nominative singular masculine superlative",
    ... )
    >>> foo.case.regular
    'nominative'

    For adjectives.

    >>> foo = EndingComponents(degree=Degree.SUPERLATIVE, string="superlative")
    >>> foo.degree.regular
    'superlative'

    For adverbs.

    >>> foo = EndingComponents(
    ...     tense=Tense.IMPERFECT,
    ...     voice=Voice.ACTIVE,
    ...     mood=Mood.INDICATIVE,
    ...     number=Number.SINGULAR,
    ...     person=1,
    ...     string="imperfect active indicative singular 1st person",
    ... )
    >>> foo.person
    1

    For verbs.

    >>> foo = EndingComponents(
    ...     tense=Tense.PERFECT,
    ...     voice=Voice.PASSIVE,
    ...     mood=Mood.PARTICIPLE,
    ...     gender=Gender.MASCULINE,
    ...     case=Case.NOMINATIVE,
    ...     number=Number.SINGULAR,
    ...     string="perfect passive participle masculine nominative singular",
    ... )
    >>> foo.tense.regular
    'perfect'

    For participles.

    >>> foo = EndingComponents(
    ...     tense=Tense.PERFECT,
    ...     voice=Voice.ACTIVE,
    ...     mood=Mood.INFINITIVE,
    ...     string="perfect active infinitive",
    ... )
    >>> foo.mood.regular
    'infinitive'

    For infinitives.

    >>> foo = EndingComponents(string="")
    >>> foo.string
    ''

    For regular words.
    """

    # fmt: off
    @overload
    def __init__(self, *, case: Case, number: Number, string: str = "") -> None: ...
    @overload
    def __init__(self, *, case: Case, number: Number, gender: Gender, string: str = "") -> None: ...
    @overload
    def __init__(self, *, case: Case, number: Number, gender: Gender, degree: Degree, string: str = "") -> None: ...
    @overload
    def __init__(self, *, degree: Degree, string: str = "") -> None: ... 
    @overload
    def __init__(self, *, tense: Tense, voice: Voice, mood: Mood, number: Number, person: Person, string: str = "") -> None: ...
    @overload
    def __init__(self, *, tense: Tense, voice: Voice, mood: Mood, gender: Gender, case: Case, number: Number, string: str = "") -> None: ...
    @overload
    def __init__(self, *, tense: Tense, voice: Voice, mood: Mood, string: str = "") -> None: ...
    @overload
    def __init__(self, *, mood: Mood, case: Case, string: str = "") -> None: ...
    @overload
    def __init__(self, *, string: str = "") -> None: ...  
    # fmt: on

    def __init__(
        self,
        *,
        case: Case | None = None,
        number: Number | None = None,
        gender: Gender | None = None,
        tense: Tense | None = None,
        voice: Voice | None = None,
        mood: Mood | None = None,
        person: Person | None = None,
        degree: Degree | None = None,
        string: str = "",
    ) -> None:
        """Initialise ``EndingComponents``.

        Determines the type and subtype of the ending.

        Parameters
        ----------
        case : Case | None, optional
            The case of the ending.
        number : Number | None, optional
            The number of the ending.
        gender : Gender | None, optional
            The gender of the ending
        tense : Tense | None, optional
            The tense of the ending.
        voice : Voice | None, optional
            The voice of the ending.
        mood : Mood | None, optional
            The mood of the ending.
        person : Person | None, optional
            The person of the ending.
        degree : Degree | None, optional
            The degree of the ending.
        string : str
            The string representation of the ending, if needed.
            Defaults to "".
        """
        if case:
            self.case: Case = case
        if number:
            self.number: Number = number
        if gender:
            self.gender: Gender = gender
        if tense:
            self.tense: Tense = tense
        if voice:
            self.voice: Voice = voice
        if mood:
            self.mood: Mood = mood
        if degree:
            self.degree: Degree = degree
        if person:
            self.person: Person = person
        self.string: str = string

        self.type: ComponentsType
        self.subtype: ComponentsSubtype | None
        self.type, self.subtype = self._determine_type()

    def _get_non_null_attributes(self) -> list[str]:
        return [
            attr
            for attr, value in vars(self).items()
            if value is not None and attr != "string"
        ]

    def _determine_type(
        self,
    ) -> tuple[ComponentsType, ComponentsSubtype | None]:
        attributes = self._get_non_null_attributes()

        if set(attributes) == {"tense", "voice", "mood", "person", "number"}:
            return (ComponentsType.VERB, None)

        if set(attributes) == {"tense", "voice", "mood"}:
            return (ComponentsType.VERB, ComponentsSubtype.INFINITIVE)

        if set(attributes) == {
            "tense",
            "voice",
            "mood",
            "number",
            "gender",
            "case",
        }:
            return (ComponentsType.VERB, ComponentsSubtype.PARTICIPLE)

        if set(attributes) == {"mood", "case"}:
            return (ComponentsType.VERB, ComponentsSubtype.VERBAL_NOUN)

        if set(attributes) == {"degree"}:
            return (ComponentsType.ADJECTIVE, ComponentsSubtype.ADVERB)

        if set(attributes) == {"number", "gender", "case", "degree"}:
            return (ComponentsType.ADJECTIVE, None)

        if set(attributes) == {"number", "gender", "case"}:
            return (ComponentsType.PRONOUN, None)

        if set(attributes) == {"number", "case"}:
            return (ComponentsType.NOUN, None)

        return (ComponentsType.REGULARWORD, None)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EndingComponents):
            return NotImplemented

        self_attrs = self._get_non_null_attributes()
        other_attrs = other._get_non_null_attributes()

        if set(self_attrs) != set(other_attrs):
            return False

        return all(
            getattr(self, attr) == getattr(other, attr) for attr in self_attrs
        )

    @staticmethod
    def _int_verb_subtypes(subtype: ComponentsSubtype | None) -> int:
        return ({
            None: 3,
            ComponentsSubtype.INFINITIVE: 2,
            ComponentsSubtype.PARTICIPLE: 1,
            ComponentsSubtype.VERBAL_NOUN: 0,
        })[subtype]

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, EndingComponents):
            return NotImplemented

        if self.type != other.type or self.subtype != other.subtype:
            # adjectives > adverbs
            if (self.type, other.type) == (ComponentsType.ADJECTIVE,) * 2:
                # NOTE: subtype can only be ADVERB or None
                # if self.subtype is not None, then other.subtype
                # must be None, because self.subtype != other.subtype
                return self.subtype is not None

            # normal verb > infinitive > participle > verbal noun
            if (self.type, other.type) == (ComponentsType.VERB,) * 2:
                return self.subtype != max(
                    self.subtype, other.subtype, key=self._int_verb_subtypes
                )

            return NotImplemented

        priority_order = [
            "tense",
            "voice",
            "mood",
            "person",
            "case",
            "number",
            "gender",
            "degree",
        ]

        for attr in priority_order:
            self_value = getattr(self, attr, None)
            other_value = getattr(other, attr, None)

            if self_value is None and other_value is None:
                continue

            if self_value != other_value:
                assert self_value is not None
                assert other_value is not None

                if attr == "person":
                    return self_value > other_value

                enum_class = self_value.__class__
                enum_members = list(enum_class)
                self_index = enum_members.index(self_value)
                other_index = enum_members.index(other_value)

                return self_index > other_index

        return False

    def __repr__(self) -> str:
        return self.string

    def __hash__(self) -> int:
        return hash(
            tuple(
                getattr(self, attr) for attr in self._get_non_null_attributes()
            )
        )


@dataclass(init=True)
class MultipleMeanings:
    """Represents multiple meanings, with a main meaning and other meanings.

    Attributes
    ----------
    meanings : tuple[str, ...]
        The meanings.

    Notes
    -----
    This class allows for there to be several English definitions of one
    Latin word. This means for Latin-to-English questions, synonyms can
    be accepted, but not vice versa.

    Examples
    --------
    >>> foo = MultipleMeanings(("hide", "conceal"))
    >>> foo.meanings
    ('hide', 'conceal')

    >>> foo.__str__()
    'hide'
    """

    meanings: tuple[str, ...]

    def __str__(self) -> str:
        return self.meanings[0]

    def __repr__(self) -> str:
        return f"MultipleMeanings({', '.join(self.meanings)})"

    def __add__(self, other: object) -> MultipleMeanings:
        if isinstance(other, MultipleMeanings):
            return MultipleMeanings(self.meanings + other.meanings)
        if isinstance(other, str):
            return MultipleMeanings((*self.meanings, other))

        return NotImplemented

    def __radd__(self, other: object) -> MultipleMeanings:
        return self.__add__(other)


class MultipleEndings(SimpleNamespace):
    """Represents multiple endings for a word.

    The fact that the attribute names can be customised means that this
    class can be used for many use cases.
    e.g. `MultipleEndings(regular="nostri", partitive="nostrum")`
    would allow for "nostrum" being the partitive genitive, while
    "nostri" being for the rest of the genitive uses.

    Attributes
    ----------
    value : str
    etc.

    Examples
    --------
    >>> foo = MultipleEndings(regular="nostri", partitive="nostrum")
    >>> foo.regular
    'nostri'

    >>> foo.__str__()
    'nostri/nostrum'

    >>> foo.get_all()
    ('nostri', 'nostrum')
    """

    def get_all(self) -> tuple[str, ...]:
        """Return a list of all the possible endings.

        Returns
        -------
        tuple[str, ...]
            The endings.
        """
        return tuple(self.__dict__.values())

    def __str__(self) -> str:
        return "/".join(self.__dict__.values())

    def __add__(self, val2: str) -> str:
        return self.__str__() + val2

    # Allows for a prefix to be added to all of the endings.
    def __radd__(self, val2: str) -> MultipleEndings:
        prefixed = {
            key: f"{val2}{value}" for key, value in self.__dict__.items()
        }
        return MultipleEndings(**prefixed)
