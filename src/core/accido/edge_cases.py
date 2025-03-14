"""Contains edge case endings."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from .misc import MultipleEndings

if TYPE_CHECKING:
    from .type_aliases import Endings

#  NOTE: There are deponents, but am keeping them for future
# TODO: Expand these
MIXED_CONJUGATION_VERBS: Final[set[str]] = {
    "abicio",
    "adicio",
    "aggredior",
    "capio",
    "concutio",
    "confugio",
    "conicio",
    "cupio",
    "deicio",
    "diripio",
    "disicio",
    "effugio",
    "eicio",
    "eripio",
    "facio",
    "fugio",
    "gradior",
    "iacio",
    "illicio",
    "ingredior",
    "inicio",
    "mori",
    "obicio",
    "patior",
    "percutio",
    "perfugio",
    "profugio",
    "proicio",
    "quatere",
    "rapio",
    "refugio",
    "reicio",
    "sapio",
    "subicio",
    "traicio",
    "occipio",
}


def check_mixed_conjugation_verb(present: str) -> bool:
    """Check if the given word is a mixed conjugation verb.

    Parameters
    ----------
    present : str
        The present form verb to check.

    Returns
    -------
    bool
        If the prefix matches a mixed conjugation verb.
    """
    return any(
        present.endswith(io_verb) for io_verb in MIXED_CONJUGATION_VERBS
    )


# TODO: Expand these
IRREGULAR_VERBS: Final[dict[str, Endings]] = {
    "sum": {
        "Vpreactindsg1": "sum",
        "Vpreactindsg2": "es",
        "Vpreactindsg3": "est",
        "Vpreactindpl1": "sumus",
        "Vpreactindpl2": "estis",
        "Vpreactindpl3": "sunt",
        "Vimpactindsg1": "eram",
        "Vimpactindsg2": "eras",
        "Vimpactindsg3": "erat",
        "Vimpactindpl1": "eramus",
        "Vimpactindpl2": "eratis",
        "Vimpactindpl3": "erant",
        "Vperactindsg1": "fui",
        "Vperactindsg2": "fuisti",
        "Vperactindsg3": "fuit",
        "Vperactindpl1": "fuimus",
        "Vperactindpl2": "fuistis",
        "Vperactindpl3": "fuerunt",
        "Vplpactindsg1": "fueram",
        "Vplpactindsg2": "fueras",
        "Vplpactindsg3": "fuerat",
        "Vplpactindpl1": "fueramus",
        "Vplpactindpl2": "fueratis",
        "Vplpactindpl3": "fuerant",
        "Vpreactinf   ": "esse",
        "Vpreactipesg2": "es",
        "Vpreactipepl2": "este",
        "Vimpactsbjsg1": "essem",
        "Vimpactsbjsg2": "esses",
        "Vimpactsbjsg3": "esset",
        "Vimpactsbjpl1": "essemus",
        "Vimpactsbjpl2": "essetis",
        "Vimpactsbjpl3": "essent",
        "Vplpactsbjsg1": "fuissem",
        "Vplpactsbjsg2": "fuisses",
        "Vplpactsbjsg3": "fuisset",
        "Vplpactsbjpl1": "fuissemus",
        "Vplpactsbjpl2": "fuissetis",
        "Vplpactsbjpl3": "fuissent",
    },
    "possum": {  # no imperatives
        "Vpreactindsg1": "possum",
        "Vpreactindsg2": "potes",
        "Vpreactindsg3": "potest",
        "Vpreactindpl1": "possumus",
        "Vpreactindpl2": "potestis",
        "Vpreactindpl3": "possunt",
        "Vimpactindsg1": "poteram",
        "Vimpactindsg2": "poteras",
        "Vimpactindsg3": "poterat",
        "Vimpactindpl1": "poteramus",
        "Vimpactindpl2": "poteratis",
        "Vimpactindpl3": "poterant",
        "Vperactindsg1": "potui",
        "Vperactindsg2": "potuisti",
        "Vperactindsg3": "potuit",
        "Vperactindpl1": "potuimus",
        "Vperactindpl2": "potuistis",
        "Vperactindpl3": "potuerunt",
        "Vplpactindsg1": "potueram",
        "Vplpactindsg2": "potueras",
        "Vplpactindsg3": "potuerat",
        "Vplpactindpl1": "potueramus",
        "Vplpactindpl2": "potueratis",
        "Vplpactindpl3": "potuerant",
        "Vpreactinf   ": "posse",
        "Vimpactsbjsg1": "possem",
        "Vimpactsbjsg2": "posses",
        "Vimpactsbjsg3": "posset",
        "Vimpactsbjpl1": "possemus",
        "Vimpactsbjpl2": "possetis",
        "Vimpactsbjpl3": "possent",
        "Vplpactsbjsg1": "potuissem",
        "Vplpactsbjsg2": "potuisses",
        "Vplpactsbjsg3": "potuisset",
        "Vplpactsbjpl1": "potuissemus",
        "Vplpactsbjpl2": "potuissetis",
        "Vplpactsbjpl3": "potuissent",
    },
    "volo": {  # no imperatives
        "Vpreactindsg1": "volo",
        "Vpreactindsg2": "vis",
        "Vpreactindsg3": "vult",
        "Vpreactindpl1": "volumus",
        "Vpreactindpl2": "vultis",
        "Vpreactindpl3": "volunt",
        "Vimpactindsg1": "volebam",
        "Vimpactindsg2": "volebas",
        "Vimpactindsg3": "volebat",
        "Vimpactindpl1": "volebamus",
        "Vimpactindpl2": "volebatis",
        "Vimpactindpl3": "volebant",
        "Vperactindsg1": "volui",
        "Vperactindsg2": "voluisti",
        "Vperactindsg3": "voluit",
        "Vperactindpl1": "voluimus",
        "Vperactindpl2": "voluistis",
        "Vperactindpl3": "voluerunt",
        "Vplpactindsg1": "volueram",
        "Vplpactindsg2": "volueras",
        "Vplpactindsg3": "voluerat",
        "Vplpactindpl1": "volueramus",
        "Vplpactindpl2": "volueratis",
        "Vplpactindpl3": "voluerant",
        "Vpreactinf   ": "velle",
        "Vimpactsbjsg1": "vellem",
        "Vimpactsbjsg2": "velles",
        "Vimpactsbjsg3": "vellet",
        "Vimpactsbjpl1": "vellemus",
        "Vimpactsbjpl2": "velletis",
        "Vimpactsbjpl3": "vellent",
        "Vplpactsbjsg1": "voluissem",
        "Vplpactsbjsg2": "voluisses",
        "Vplpactsbjsg3": "voluisset",
        "Vplpactsbjpl1": "voluissemus",
        "Vplpactsbjpl2": "voluissetis",
        "Vplpactsbjpl3": "voluissent",
    },
    "nolo": {  # no imperatives
        "Vpreactindsg1": "nolo",
        "Vpreactindsg2": "non vis",
        "Vpreactindsg3": "non vult",
        "Vpreactindpl1": "nolumus",
        "Vpreactindpl2": "non vultis",
        "Vpreactindpl3": "nolunt",
        "Vimpactindsg1": "nolebam",
        "Vimpactindsg2": "nolebas",
        "Vimpactindsg3": "nolebat",
        "Vimpactindpl1": "nolebamus",
        "Vimpactindpl2": "nolebatis",
        "Vimpactindpl3": "nolebant",
        "Vperactindsg1": "nolui",
        "Vperactindsg2": "noluisti",
        "Vperactindsg3": "noluit",
        "Vperactindpl1": "noluimus",
        "Vperactindpl2": "noluistis",
        "Vperactindpl3": "noluerunt",
        "Vplpactindsg1": "nolueram",
        "Vplpactindsg2": "nolueras",
        "Vplpactindsg3": "noluerat",
        "Vplpactindpl1": "nolueramus",
        "Vplpactindpl2": "nolueratis",
        "Vplpactindpl3": "noluerant",
        "Vpreactinf   ": "nolle",
        "Vimpactsbjsg1": "nollem",
        "Vimpactsbjsg2": "nolles",
        "Vimpactsbjsg3": "nollet",
        "Vimpactsbjpl1": "nollemus",
        "Vimpactsbjpl2": "nolletis",
        "Vimpactsbjpl3": "nollent",
        "Vplpactsbjsg1": "noluissem",
        "Vplpactsbjsg2": "noluisses",
        "Vplpactsbjsg3": "noluisset",
        "Vplpactsbjpl1": "noluissemus",
        "Vplpactsbjpl2": "noluissetis",
        "Vplpactsbjpl3": "noluissent",
    },
    "fero": {
        "Vpreactindsg1": "fero",
        "Vpreactindsg2": "fers",
        "Vpreactindsg3": "fert",
        "Vpreactindpl1": "ferimus",
        "Vpreactindpl2": "fertis",
        "Vpreactindpl3": "ferunt",
        "Vimpactindsg1": "ferebam",
        "Vimpactindsg2": "ferebas",
        "Vimpactindsg3": "ferebat",
        "Vimpactindpl1": "ferebamus",
        "Vimpactindpl2": "ferebatis",
        "Vimpactindpl3": "ferebant",
        "Vperactindsg1": "tuli",
        "Vperactindsg2": "tulisti",
        "Vperactindsg3": "tulit",
        "Vperactindpl1": "tulimus",
        "Vperactindpl2": "tulistis",
        "Vperactindpl3": "tulerunt",
        "Vplpactindsg1": "tuleram",
        "Vplpactindsg2": "tuleras",
        "Vplpactindsg3": "tulerat",
        "Vplpactindpl1": "tuleramus",
        "Vplpactindpl2": "tuleratis",
        "Vplpactindpl3": "tulerant",
        "Vpreactinf   ": "ferre",
        "Vpreactipesg2": "fer",
        "Vpreactipepl2": "ferte",
        "Vimpactsbjsg1": "ferrem",
        "Vimpactsbjsg2": "ferres",
        "Vimpactsbjsg3": "ferret",
        "Vimpactsbjpl1": "ferremus",
        "Vimpactsbjpl2": "ferretis",
        "Vimpactsbjpl3": "ferrent",
        "Vplpactsbjsg1": "tulissem",
        "Vplpactsbjsg2": "tulisses",
        "Vplpactsbjsg3": "tulisset",
        "Vplpactsbjpl1": "tulissemus",
        "Vplpactsbjpl2": "tulissetis",
        "Vplpactsbjpl3": "tulissent",
    },
    "eo": {
        "Vpreactindsg1": "eo",
        "Vpreactindsg2": "is",
        "Vpreactindsg3": "it",
        "Vpreactindpl1": "imus",
        "Vpreactindpl2": "itis",
        "Vpreactindpl3": "eunt",
        "Vimpactindsg1": "ibam",
        "Vimpactindsg2": "ibas",
        "Vimpactindsg3": "ibat",
        "Vimpactindpl1": "ibamus",
        "Vimpactindpl2": "ibatis",
        "Vimpactindpl3": "ibant",
        "Vperactindsg1": "ii",
        "Vperactindsg2": "iisti",
        "Vperactindsg3": "iit",
        "Vperactindpl1": "iimus",
        "Vperactindpl2": "iistis",
        "Vperactindpl3": "ierunt",
        "Vplpactindsg1": "ieram",
        "Vplpactindsg2": "ieras",
        "Vplpactindsg3": "ierat",
        "Vplpactindpl1": "ieramus",
        "Vplpactindpl2": "ieratis",
        "Vplpactindpl3": "ierant",
        "Vpreactinf   ": "ire",
        "Vpreactipesg2": "i",
        "Vpreactipepl2": "ite",
        "Vimpactsbjsg1": "irem",
        "Vimpactsbjsg2": "ires",
        "Vimpactsbjsg3": "iret",
        "Vimpactsbjpl1": "iremus",
        "Vimpactsbjpl2": "iretis",
        "Vimpactsbjpl3": "irent",
        "Vplpactsbjsg1": "iissem",
        "Vplpactsbjsg2": "iisses",
        "Vplpactsbjsg3": "iisset",
        "Vplpactsbjpl1": "iissemus",
        "Vplpactsbjpl2": "iissetis",
        "Vplpactsbjpl3": "iissent",
    },
    "absum": {  # no imperatives
        "Vpreactindsg1": "absum",
        "Vpreactindsg2": "abes",
        "Vpreactindsg3": "abest",
        "Vpreactindpl1": "absumus",
        "Vpreactindpl2": "abestis",
        "Vpreactindpl3": "absunt",
        "Vimpactindsg1": "aberam",
        "Vimpactindsg2": "aberas",
        "Vimpactindsg3": "aberat",
        "Vimpactindpl1": "aberamus",
        "Vimpactindpl2": "aberatis",
        "Vimpactindpl3": "aberant",
        "Vperactindsg1": "afui",
        "Vperactindsg2": "afuisti",
        "Vperactindsg3": "afuit",
        "Vperactindpl1": "afuimus",
        "Vperactindpl2": "afuistis",
        "Vperactindpl3": "afuerunt",
        "Vplpactindsg1": "afueram",
        "Vplpactindsg2": "afueras",
        "Vplpactindsg3": "afuerat",
        "Vplpactindpl1": "afueramus",
        "Vplpactindpl2": "afueratis",
        "Vplpactindpl3": "afuerant",
        "Vpreactinf   ": "abesse",
        "Vimpactsbjsg1": "abessem",
        "Vimpactsbjsg2": "abesses",
        "Vimpactsbjsg3": "abesset",
        "Vimpactsbjpl1": "abessemus",
        "Vimpactsbjpl2": "abessetis",
        "Vimpactsbjpl3": "abessent",
        "Vplpactsbjsg1": "afuissem",
        "Vplpactsbjsg2": "afuisses",
        "Vplpactsbjsg3": "afuisset",
        "Vplpactsbjpl1": "afuissemus",
        "Vplpactsbjpl2": "afuissetis",
        "Vplpactsbjpl3": "afuissent",
    },
    "adsum": {  # no imperatives
        "Vpreactindsg1": "adsum",
        "Vpreactindsg2": "ades",
        "Vpreactindsg3": "adest",
        "Vpreactindpl1": "adsumus",
        "Vpreactindpl2": "adestis",
        "Vpreactindpl3": "adsunt",
        "Vimpactindsg1": "aderam",
        "Vimpactindsg2": "aderas",
        "Vimpactindsg3": "aderat",
        "Vimpactindpl1": "aderamus",
        "Vimpactindpl2": "aderatis",
        "Vimpactindpl3": "aderant",
        "Vperactindsg1": "adfui",
        "Vperactindsg2": "adfuisti",
        "Vperactindsg3": "adfuit",
        "Vperactindpl1": "adfuimus",
        "Vperactindpl2": "adfuistis",
        "Vperactindpl3": "adfuerunt",
        "Vplpactindsg1": "adfueram",
        "Vplpactindsg2": "adfueras",
        "Vplpactindsg3": "adfuerat",
        "Vplpactindpl1": "adfueramus",
        "Vplpactindpl2": "adfueratis",
        "Vplpactindpl3": "adfuerant",
        "Vpreactinf   ": "adesse",
        "Vimpactsbjsg1": "adessem",
        "Vimpactsbjsg2": "adesses",
        "Vimpactsbjsg3": "adesset",
        "Vimpactsbjpl1": "adessemus",
        "Vimpactsbjpl2": "adessetis",
        "Vimpactsbjpl3": "adessent",
        "Vplpactsbjsg1": "adfuissem",
        "Vplpactsbjsg2": "adfuisses",
        "Vplpactsbjsg3": "adfuisset",
        "Vplpactsbjpl1": "adfuissemus",
        "Vplpactsbjpl2": "adfuissetis",
        "Vplpactsbjpl3": "adfuissent",
    },
    "inquam": {  # defective conjugation
        "Vpreactindsg1": "inquam",
        "Vpreactindsg2": "inquis",
        "Vpreactindsg3": "inquit",
        "Vpreactindpl1": "inquimus",
        "Vpreactindpl2": "inquitis",
        "Vpreactindpl3": "inquint",
        "Vimpactindsg3": "inquiebat",
        "Vperactindsg1": "inquii",
        "Vperactindsg2": "inquisti",
        "Vperactindsg3": "inquit",
        "Vpreactipesg2": "inque",
    },
}


# Contains verbs that are derived from the main irregular verbs (usually
# having a prefix)
DERIVED_IRREGULAR_VERBS: Final[dict[str, set[str]]] = {
    "eo": {
        "abeo",
        "adeo",
        "ambeo",
        "circumeo",
        "coeo",
        "deeo",
        "dispereo",
        "exeo",
        "ineo",
        "intereo",
        "introeo",
        "nequeo",
        "obeo",
        "pereo",
        "praetereo",
        "prodeo",
        "queo",
        "redeo",
        "subeo",
        "transabeo",
        "transeo",
        "veneo",
    },
    "fero": {
        "affero",
        "aufero",
        "circumfero",
        "confero",
        "defero",
        "differo",
        "effero",
        "infero",
        "interfero",
        "introfero",
        "offero",
        "perfero",
        "postfero",
        "praefero",
        "profero",
        "refero",
        "suffero",
        "transfero",
    },
}


# NOTE: This entire thing will probably need to be reworked at some point
# Notably allowing the given perfect stem to be used so that I don't have
# to write everything manually
DERIVED_IRREGULAR_ENDINGS: Final[dict[str, Endings]] = {
    "eo": {
        "Vpreactindsg1": "eo",
        "Vpreactindsg2": "is",
        "Vpreactindsg3": "it",
        "Vpreactindpl1": "imus",
        "Vpreactindpl2": "itis",
        "Vpreactindpl3": "eunt",
        "Vimpactindsg1": "ibam",
        "Vimpactindsg2": "ibas",
        "Vimpactindsg3": "ibat",
        "Vimpactindpl1": "ibamus",
        "Vimpactindpl2": "ibatis",
        "Vimpactindpl3": "ibant",
        "Vperactindsg1": "ii",
        "Vperactindsg2": "isti",
        "Vperactindsg3": "iit",
        "Vperactindpl1": "iimus",
        "Vperactindpl2": "istis",
        "Vperactindpl3": "ierunt",
        "Vplpactindsg1": "ieram",
        "Vplpactindsg2": "ieras",
        "Vplpactindsg3": "ierat",
        "Vplpactindpl1": "ieramus",
        "Vplpactindpl2": "ieratis",
        "Vplpactindpl3": "ierant",
        "Vpreactinf   ": "ire",
        "Vpreactipesg2": "i",
        "Vpreactipepl2": "ite",
        "Vimpactsbjsg1": "irem",
        "Vimpactsbjsg2": "ires",
        "Vimpactsbjsg3": "iret",
        "Vimpactsbjpl1": "iremus",
        "Vimpactsbjpl2": "iretis",
        "Vimpactsbjpl3": "irent",
        "Vplpactsbjsg1": "issem",
        "Vplpactsbjsg2": "isses",
        "Vplpactsbjsg3": "isset",
        "Vplpactsbjpl1": "issemus",
        "Vplpactsbjpl2": "issetis",
        "Vplpactsbjpl3": "issent",
    },
    "fero": {
        "Vpreactindsg1": "fero",
        "Vpreactindsg2": "fers",
        "Vpreactindsg3": "fert",
        "Vpreactindpl1": "ferimus",
        "Vpreactindpl2": "fertis",
        "Vpreactindpl3": "ferunt",
        "Vimpactindsg1": "ferebam",
        "Vimpactindsg2": "ferebas",
        "Vimpactindsg3": "ferebat",
        "Vimpactindpl1": "ferebamus",
        "Vimpactindpl2": "ferebatis",
        "Vimpactindpl3": "ferebant",
        "Vperactindsg1": "tuli",
        "Vperactindsg2": "tulisti",
        "Vperactindsg3": "tulit",
        "Vperactindpl1": "tulimus",
        "Vperactindpl2": "tulistis",
        "Vperactindpl3": "tulerunt",
        "Vplpactindsg1": "tuleram",
        "Vplpactindsg2": "tuleras",
        "Vplpactindsg3": "tulerat",
        "Vplpactindpl1": "tuleramus",
        "Vplpactindpl2": "tuleratis",
        "Vplpactindpl3": "tulerant",
        "Vpreactinf   ": "ferre",
        "Vpreactipesg2": "fer",
        "Vpreactipepl2": "ferte",
        "Vimpactsbjsg1": "ferrem",
        "Vimpactsbjsg2": "ferres",
        "Vimpactsbjsg3": "ferret",
        "Vimpactsbjpl1": "ferremus",
        "Vimpactsbjpl2": "ferretis",
        "Vimpactsbjpl3": "ferrent",
        "Vplpactsbjsg1": "tulissem",
        "Vplpactsbjsg2": "tulisses",
        "Vplpactsbjsg3": "tulisset",
        "Vplpactsbjpl1": "tulissemus",
        "Vplpactsbjpl2": "tulissetis",
        "Vplpactsbjpl3": "tulissent",
    },
}


def find_irregular_endings(present: str) -> Endings | None:
    """Detect if a verb is irregular and return its endings.

    Parameters
    ----------
    present : str
        The present form verb to check.

    Returns
    -------
    Endings | None
        The endings. ``None`` if the verb is not irregular.
    """

    def _prefix(
        pre: str, endings: Endings
    ) -> dict[str, str | MultipleEndings]:
        return {key: pre + value for key, value in endings.items()}

    if present in IRREGULAR_VERBS:
        return IRREGULAR_VERBS[present]

    for irregular_suffix, suffix_list in DERIVED_IRREGULAR_VERBS.items():
        if present in suffix_list:
            return _prefix(
                present.rstrip(irregular_suffix),
                DERIVED_IRREGULAR_ENDINGS[irregular_suffix],
            )

    return None


IRREGULAR_NOUNS: Final[dict[str, Endings]] = {
    "ego": {
        "Nnomsg": "ego",
        "Nvocsg": "ego",
        "Naccsg": "me",
        "Ngensg": "mei",
        "Ndatsg": "mihi",
        "Nablsg": "me",
        "Nnompl": "nos",
        "Nvocpl": "nos",
        "Naccpl": "nos",
        "Ngenpl": MultipleEndings(regular="nostri", partitive="nostrum"),
        "Ndatpl": "nobis",
        "Nablpl": "nobis",
    },
    "tu": {
        "Nnomsg": "tu",
        "Nvocsg": "tu",
        "Naccsg": "te",
        "Ngensg": "tui",
        "Ndatsg": "tibi",
        "Nablsg": "te",
        "Nnompl": "vos",
        "Nvocpl": "vos",
        "Naccpl": "vos",
        "Ngenpl": MultipleEndings(regular="vestri", partitive="vestrum"),
        "Ndatpl": "vobis",
        "Nablpl": "vobis",
    },
    "se": {
        "Naccsg": "se",
        "Ngensg": "sui",
        "Ndatsg": "sibi",
        "Nablsg": "se",
        "Naccpl": "se",
        "Ngenpl": "sui",
        "Ndatpl": "sibi",
        "Nablpl": "se",
    },
}

LIS_ADJECTIVES: Final[set[str]] = {
    "facilis",
    "difficilis",
    "similis",
    "dissimilis",
    "gracilis",
    "humilis",
}

# Contains adjectives that have irregular forms in the comparative,
# superlative and adverb forms.
# Note that some of these adjectives do not have adverb forms, so the adverb
# forms are given a None value instead.
IRREGULAR_ADJECTIVES: Final[
    dict[str, tuple[str, str, str | None, str | None, str | None]]
] = {
    "bonus": ("melior", "optim", "bene", "melius", "optime"),
    "malus": ("peior", "pessim", "male", "peius", "pessime"),
    "magnus": ("maior", "maxim", None, None, None),
    "parvus": ("minor", "minim", None, None, None),
    # multo (adverb) exists but that would very much stuff up things
    "multus": ("plus", "plurim", None, None, None),
    # nequam should probably just be put in as a regular
    "nequam": ("nequior", "nequissim", None, None, None),
    "frugi": (
        "frugalior",
        "frugalissim",
        "frugaliter",
        "frugalius",
        "frugalissime",
    ),
    "dexter": ("dexterior", "dextim", None, None, None),
}

# TODO: Add to this
NO_ADVERB_ADJECTIVES = {"ingens"}

PRONOUNS: Final[dict[str, Endings]] = {
    "hic": {
        "Pmnomsg": "hic",
        "Pmaccsg": "hunc",
        "Pmgensg": "huius",
        "Pmdatsg": "huic",
        "Pmablsg": "hoc",
        "Pmnompl": "hi",
        "Pmaccpl": "hos",
        "Pmgenpl": "horum",
        "Pmdatpl": "his",
        "Pmablpl": "his",
        "Pfnomsg": "haec",
        "Pfaccsg": "hanc",
        "Pfgensg": "huius",
        "Pfdatsg": "huic",
        "Pfablsg": "hac",
        "Pfnompl": "hae",
        "Pfaccpl": "has",
        "Pfgenpl": "harum",
        "Pfdatpl": "his",
        "Pfablpl": "his",
        "Pnnomsg": "hoc",
        "Pnaccsg": "hoc",
        "Pngensg": "huius",
        "Pndatsg": "huic",
        "Pnablsg": "hoc",
        "Pnnompl": "haec",
        "Pnaccpl": "haec",
        "Pngenpl": "horum",
        "Pndatpl": "his",
        "Pnablpl": "his",
    },
    "ille": {
        "Pmnomsg": "ille",
        "Pmaccsg": "illum",
        "Pmgensg": "illius",
        "Pmdatsg": "illi",
        "Pmablsg": "illo",
        "Pmnompl": "illi",
        "Pmaccpl": "illos",
        "Pmgenpl": "illorum",
        "Pmdatpl": "illis",
        "Pmablpl": "illis",
        "Pfnomsg": "illa",
        "Pfaccsg": "illam",
        "Pfgensg": "illius",
        "Pfdatsg": "illi",
        "Pfablsg": "illa",
        "Pfnompl": "illae",
        "Pfaccpl": "illas",
        "Pfgenpl": "illarum",
        "Pfdatpl": "illis",
        "Pfablpl": "illis",
        "Pnnomsg": "illud",
        "Pnaccsg": "illud",
        "Pngensg": "illius",
        "Pndatsg": "illi",
        "Pnablsg": "illo",
        "Pnnompl": "illa",
        "Pnaccpl": "illa",
        "Pngenpl": "illorum",
        "Pndatpl": "illis",
        "Pnablpl": "illis",
    },
    "is": {
        "Pmnomsg": "is",
        "Pmaccsg": "eum",
        "Pmgensg": "eius",
        "Pmdatsg": "ei",
        "Pmablsg": "eo",
        "Pmnompl": "ei",
        "Pmaccpl": "eos",
        "Pmgenpl": "eorum",
        "Pmdatpl": "eis",
        "Pmablpl": "eis",
        "Pfnomsg": "ea",
        "Pfaccsg": "eam",
        "Pfgensg": "eius",
        "Pfdatsg": "ei",
        "Pfablsg": "ea",
        "Pfnompl": "eae",
        "Pfaccpl": "eas",
        "Pfgenpl": "earum",
        "Pfdatpl": "eis",
        "Pfablpl": "eis",
        "Pnnomsg": "id",
        "Pnaccsg": "id",
        "Pngensg": "eius",
        "Pndatsg": "ei",
        "Pnablsg": "eo",
        "Pnnompl": "ea",
        "Pnaccpl": "ea",
        "Pngenpl": "eorum",
        "Pndatpl": "eis",
        "Pnablpl": "eis",
    },
    "ipse": {
        "Pmnomsg": "ipse",
        "Pmaccsg": "ipsum",
        "Pmgensg": "ipsius",
        "Pmdatsg": "ipsi",
        "Pmablsg": "ipso",
        "Pmnompl": "ipsi",
        "Pmaccpl": "ipsos",
        "Pmgenpl": "ipsorum",
        "Pmdatpl": "ipsis",
        "Pmablpl": "ipsis",
        "Pfnomsg": "ipsa",
        "Pfaccsg": "ipsam",
        "Pfgensg": "ipsius",
        "Pfdatsg": "ipsi",
        "Pfablsg": "ipsa",
        "Pfnompl": "ipsae",
        "Pfaccpl": "ipsas",
        "Pfgenpl": "ipsarum",
        "Pfdatpl": "ipsis",
        "Pfablpl": "ipsis",
        "Pnnomsg": "ipsum",
        "Pnaccsg": "ipsum",
        "Pngensg": "ipsius",
        "Pndatsg": "ipsi",
        "Pnablsg": "ipso",
        "Pnnompl": "ipsa",
        "Pnaccpl": "ipsa",
        "Pngenpl": "ipsorum",
        "Pndatpl": "ipsis",
        "Pnablpl": "ipsis",
    },
    "idem": {
        "Pmnomsg": "idem",
        "Pmaccsg": "eundem",
        "Pmgensg": "eiusdem",
        "Pmdatsg": "eidem",
        "Pmablsg": "eodem",
        "Pmnompl": "eidem",
        "Pmaccpl": "eosdem",
        "Pmgenpl": "eorundem",
        "Pmdatpl": "eisdem",
        "Pmablpl": "eisdem",
        "Pfnomsg": "eadem",
        "Pfaccsg": "eandem",
        "Pfgensg": "eiusdem",
        "Pfdatsg": "eidem",
        "Pfablsg": "eadem",
        "Pfnompl": "eaedem",
        "Pfaccpl": "easdem",
        "Pfgenpl": "earundem",
        "Pfdatpl": "eisdem",
        "Pfablpl": "eisdem",
        "Pnnomsg": "idem",
        "Pnaccsg": "idem",
        "Pngensg": "eiusdem",
        "Pndatsg": "eidem",
        "Pnablsg": "eodem",
        "Pnnompl": "eadem",
        "Pnaccpl": "eadem",
        "Pngenpl": "eorundem",
        "Pndatpl": "eisdem",
        "Pnablpl": "eisdem",
    },
    "qui": {
        "Pmnomsg": "qui",
        "Pmaccsg": "quem",
        "Pmgensg": "cuius",
        "Pmdatsg": "cui",
        "Pmablsg": "quo",
        "Pmnompl": "qui",
        "Pmaccpl": "quos",
        "Pmgenpl": "quorum",
        "Pmdatpl": "quibus",
        "Pmablpl": "quibus",
        "Pfnomsg": "quae",
        "Pfaccsg": "quam",
        "Pfgensg": "cuius",
        "Pfdatsg": "cui",
        "Pfablsg": "qua",
        "Pfnompl": "quae",
        "Pfaccpl": "quas",
        "Pfgenpl": "quarum",
        "Pfdatpl": "quibus",
        "Pfablpl": "quibus",
        "Pnnomsg": "quod",
        "Pnaccsg": "quod",
        "Pngensg": "cuius",
        "Pndatsg": "cui",
        "Pnablsg": "quo",
        "Pnnompl": "quae",
        "Pnaccpl": "quae",
        "Pngenpl": "quorum",
        "Pndatpl": "quibus",
        "Pnablpl": "quibus",
    },
    "quidam": {
        "Pmnomsg": "quidam",
        "Pmaccsg": "quendam",
        "Pmgensg": "cuiusdam",
        "Pmdatsg": "cuidam",
        "Pmablsg": "quodam",
        "Pmnompl": "quidam",
        "Pmaccpl": "quosdam",
        "Pmgenpl": "quorundam",
        "Pmdatpl": "quibusdam",
        "Pmablpl": "quibusdam",
        "Pfnomsg": "quaedam",
        "Pfaccsg": "quandam",
        "Pfgensg": "cuiusdam",
        "Pfdatsg": "cuidam",
        "Pfablsg": "quadam",
        "Pfnompl": "quaedam",
        "Pfaccpl": "quasdam",
        "Pfgenpl": "quarundam",
        "Pfdatpl": "quibusdam",
        "Pfablpl": "quibusdam",
        "Pnnomsg": "quoddam",
        "Pnaccsg": "quoddam",
        "Pngensg": "cuiusdam",
        "Pndatsg": "cuidam",
        "Pnablsg": "quodam",
        "Pnnompl": "quaedam",
        "Pnaccpl": "quaedam",
        "Pngenpl": "quorundam",
        "Pndatpl": "quibusdam",
        "Pnablpl": "quibusdam",
    },
}
