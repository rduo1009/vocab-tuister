"""Contains conversion functions for compatability with protobuf.

Hacky bridges between the original vocab-tuister classes and the new
protobuf-generated ones.
"""

from typing import TYPE_CHECKING

import betterproto2

from ...pb.vocab_tuister.v1 import (
    Case as CasePb,
    Degree as DegreePb,
    EndingComponents as EndingComponentsPb,
    Gender as GenderPb,
    Mood as MoodPb,
    Number as NumberPb,
    Person as PersonPb,
    Question as QuestionPb,
    Tense as TensePb,
    Voice as VoicePb,
)
from .question_classes import QuestionClasses

if TYPE_CHECKING:
    from ..accido.misc import (
        EndingComponents as EndingComponentsOriginal,
        _EndingComponentEnum as _EndingComponentEnumOriginal,
    )
    from .question_classes import Question as QuestionOriginal


def _convert_enum[PbEnum: betterproto2.Enum](
    accido_val: _EndingComponentEnumOriginal | None,
    pb_enum_class: type[PbEnum],
) -> PbEnum:
    """Convert an accido enum value to its protobuf equivalent.

    Accido enums use plain member names (e.g. ``Voice.ACTIVE``), while the
    generated protobuf enums prefix each member with the enum's name
    (e.g. ``Voice.VOICE_ACTIVE``). This function handles that translation,
    and also maps ``None`` — used by accido to represent an unset field — to
    the protobuf convention of ``0`` for unspecified values.

    Parameters
    ----------
    accido_val
        The accido enum value to convert, or ``None`` if the field was not set.
    pb_enum_class
        The target protobuf enum class to convert into.

    Returns
    -------
    PbEnum
        The corresponding protobuf enum member, or the ``UNSPECIFIED`` member
        (value ``0``) if ``accido_val`` is ``None``.

    Examples
    --------
    >>> _convert_enum(Voice.ACTIVE, VoicePb)
    VOICE_ACTIVE  # i.e. VoicePb(1)
    >>> _convert_enum(None, VoicePb)
    VOICE_UNSPECIFIED  # i.e. VoicePb(0)
    """
    if accido_val is None:
        # Protobuf uses 0 as the sentinel "not set" / UNSPECIFIED value
        return pb_enum_class(0)

    # Build the prefixed name expected by the pb enum, e.g.:
    #   pb_enum_class=VoicePb  ->  prefix="VOICE_"
    #   accido_val.name="ACTIVE"  ->  lookup key="VOICE_ACTIVE"
    prefix = pb_enum_class.__name__.upper() + "_"
    return pb_enum_class[prefix + accido_val.name]


def ending_components_pb(
    ending_components: EndingComponentsOriginal,
) -> EndingComponentsPb:
    """Convert an accido ``EndingComponents`` to its protobuf representation.

    Accido's ``EndingComponents`` only sets attributes that are relevant to a
    given ending type — for example, a noun will have ``case`` and ``number``
    but not ``tense`` or ``voice``. Unset attributes simply don't exist on the
    object. Protobuf, by contrast, requires every field to be present, using
    ``0`` / ``UNSPECIFIED`` for fields that carry no information.

    This function bridges that gap: it reads each possible field via
    ``getattr(..., None)`` so that missing attributes are safely treated as
    ``None``, then delegates each enum conversion to ``_convert_enum``.

    Parameters
    ----------
    ending_components
        The accido ``EndingComponents`` instance to convert.

    Returns
    -------
    EndingComponentsPb
        The populated protobuf message, with every unset accido field mapped
        to its ``UNSPECIFIED`` (``0``) protobuf counterpart.
    """
    return EndingComponentsPb(
        # getattr with a None default safely handles fields that accido
        # never set on this instance (e.g. tense on a noun ending)
        case=_convert_enum(getattr(ending_components, "case", None), CasePb),
        number=_convert_enum(
            getattr(ending_components, "number", None), NumberPb
        ),
        gender=_convert_enum(
            getattr(ending_components, "gender", None), GenderPb
        ),
        tense=_convert_enum(
            getattr(ending_components, "tense", None), TensePb
        ),
        voice=_convert_enum(
            getattr(ending_components, "voice", None), VoicePb
        ),
        mood=_convert_enum(getattr(ending_components, "mood", None), MoodPb),
        person=_convert_enum(
            getattr(ending_components, "person", None), PersonPb
        ),
        degree=_convert_enum(
            getattr(ending_components, "degree", None), DegreePb
        ),
        # string is always present on accido EndingComponents (defaults to "")
        string=ending_components.string,
    )


QUESTION_FIELD_MAP = {
    QuestionClasses.TYPEIN_ENGTOLAT: "type_in_eng_to_lat",
    QuestionClasses.TYPEIN_LATTOENG: "type_in_lat_to_eng",
    QuestionClasses.PARSEWORD_LATTOCOMP: "parse_lat_to_comp",
    QuestionClasses.PARSEWORD_COMPTOLAT: "parse_comp_to_lat",
    QuestionClasses.PRINCIPAL_PARTS: "principal_parts",
    QuestionClasses.MULTIPLECHOICE_ENGTOLAT: "mc_eng_to_lat",
    QuestionClasses.MULTIPLECHOICE_LATTOENG: "mc_lat_to_eng",
}


def question_pb(
    question_class: QuestionClasses, question_object: QuestionOriginal
) -> QuestionPb:
    field = QUESTION_FIELD_MAP[question_class]
    kwargs = {field: question_object}
    return QuestionPb(**kwargs)  # pyright: ignore[reportArgumentType]
