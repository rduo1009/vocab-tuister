"""Contains conversion functions for compatability with protobuf.

Hacky bridges between the original vocab-tuister classes and the new
protobuf-generated ones.
"""

from typing import TYPE_CHECKING, cast

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
from ..accido.misc import (
    Case as CaseOriginal,
    Degree as DegreeOriginal,
    EndingComponents as EndingComponentsOriginal,
    Gender as GenderOriginal,
    Mood as MoodOriginal,
    Number as NumberOriginal,
    Tense as TenseOriginal,
    Voice as VoiceOriginal,
)
from .question_classes import QuestionClasses

if TYPE_CHECKING:
    from ..accido.type_aliases import Person as PersonOriginal
    from .question_classes import Question as QuestionOriginal


def _convert_enum[PbEnum: betterproto2.Enum](
    accido_val_name: str, pb_enum_class: type[PbEnum]
) -> PbEnum:
    """Convert an accido enum value to its protobuf equivalent.

    Accido enums use plain member names (e.g. ``Voice.ACTIVE``), while the
    generated protobuf enums prefix each member with the enum's name
    (e.g. ``Voice.VOICE_ACTIVE``). This function handles that translation,
    and also maps ``None`` — used by accido to represent an unset field — to
    the protobuf convention of ``0`` for unspecified values.

    Parameters
    ----------
    accido_val_name
        The accido enum value string to convert, or ``""`` if the field was not set.
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
    if not accido_val_name:
        # Protobuf uses 0 as the sentinel "not set" / UNSPECIFIED value
        return pb_enum_class(0)

    # Build the prefixed name used in the wire-format mapping, e.g.:
    #   pb_enum_class=VoicePb  ->  prefix="VOICE_"
    #   accido_val.name="ACTIVE"  ->  lookup key="VOICE_ACTIVE"
    # Note: betterproto2 strips the prefix from actual member names, so
    # pb_enum_class["VOICE_ACTIVE"] would fail — the member is just "ACTIVE".
    # betterproto_renamed_proto_names_to_value() retains the prefixed names
    # as keys mapping to their integer values, so we go through that instead.
    #
    # aenum MultiValue members do have a .name attribute, but accido_val may
    # arrive as a bare int (e.g. if the value was serialised or compared
    # before being passed here). Coerce it back to the enum member first so
    # that .name is always available.

    prefix = pb_enum_class.__name__.upper() + "_"
    prefixed_name = prefix + accido_val_name
    value = pb_enum_class.betterproto_renamed_proto_names_to_value()[
        prefixed_name
    ]
    return pb_enum_class(value)


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
        case=_convert_enum(
            cast("CaseOriginal", x).name
            if (x := getattr(ending_components, "case", None)) is not None
            else "",
            CasePb,
        ),
        number=_convert_enum(
            cast("NumberOriginal", x).name
            if (x := getattr(ending_components, "number", None)) is not None
            else "",
            NumberPb,
        ),
        gender=_convert_enum(
            cast("GenderOriginal", x).name
            if (x := getattr(ending_components, "gender", None)) is not None
            else "",
            GenderPb,
        ),
        tense=_convert_enum(
            cast("TenseOriginal", x).name
            if (x := getattr(ending_components, "tense", None)) is not None
            else "",
            TensePb,
        ),
        voice=_convert_enum(
            cast("VoiceOriginal", x).name
            if (x := getattr(ending_components, "voice", None)) is not None
            else "",
            VoicePb,
        ),
        mood=_convert_enum(
            cast("MoodOriginal", x).name
            if (x := getattr(ending_components, "mood", None)) is not None
            else "",
            MoodPb,
        ),
        person=PersonPb(x)
        if (x := getattr(ending_components, "person", None)) is not None
        else PersonPb.UNSPECIFIED,
        degree=_convert_enum(
            cast("DegreeOriginal", x).name
            if (x := getattr(ending_components, "degree", None)) is not None
            else "",
            DegreePb,
        ),
        # string is always present on accido EndingComponents (defaults to "")
        string=ending_components.string,
    )


def ending_components_original(
    ending_components_pb: EndingComponentsPb,
) -> EndingComponentsOriginal:
    """Convert a protobuf ``EndingComponents`` to accido's representation.

    Protobuf stores every enum field, using ``*_UNSPECIFIED`` (numeric ``0``)
    when a field carries no information. Accido's ``EndingComponents``,
    however, omits irrelevant attributes entirely.

    This function performs the inverse transformation of
    ``ending_components_pb``: any protobuf enum whose value is
    ``UNSPECIFIED`` is converted to ``None`` and therefore not passed into
    the accido constructor.

    Parameters
    ----------
    ending_components_pb
        The protobuf ``EndingComponents`` instance to convert.

    Returns
    -------
    EndingComponentsOriginal
        The reconstructed accido ``EndingComponents`` instance, containing
        only meaningful grammatical attributes.
    """
    kwargs: dict[str, object] = {}

    if ending_components_pb.case != CasePb.UNSPECIFIED:
        kwargs["case"] = CaseOriginal[ending_components_pb.case.name]

    if ending_components_pb.number != NumberPb.UNSPECIFIED:
        kwargs["number"] = NumberOriginal[ending_components_pb.number.name]

    if ending_components_pb.gender != GenderPb.UNSPECIFIED:
        kwargs["gender"] = GenderOriginal[ending_components_pb.gender.name]

    if ending_components_pb.tense != TensePb.UNSPECIFIED:
        kwargs["tense"] = TenseOriginal[ending_components_pb.tense.name]

    if ending_components_pb.voice != VoicePb.UNSPECIFIED:
        kwargs["voice"] = VoiceOriginal[ending_components_pb.voice.name]

    if ending_components_pb.mood != MoodPb.UNSPECIFIED:
        kwargs["mood"] = MoodOriginal[ending_components_pb.mood.name]

    if ending_components_pb.person != PersonPb.UNSPECIFIED:
        kwargs["person"] = cast(
            "PersonOriginal", ending_components_pb.person.value
        )

    if ending_components_pb.degree != DegreePb.UNSPECIFIED:
        kwargs["degree"] = DegreeOriginal[ending_components_pb.degree.name]

    # string is always present in both representations
    kwargs["string"] = ending_components_pb.string

    return EndingComponentsOriginal(**kwargs)


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
