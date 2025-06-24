"""Contains edge case endings."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Annotated, Final, Literal, TypeIs, cast

from ...utils.dict_changes import DictChanges
from .misc import MultipleEndings

if TYPE_CHECKING:
    from collections.abc import Callable

    from .type_aliases import Conjugation, Ending, Endings

# -----------------------------------------------------------------------------
# MIXED CONJUGATION VERBS

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


# -----------------------------------------------------------------------------
# VERBS WITH DIFFERENT PRINCIPAL PARTS

# FIXME: These lists are incorrect in places. If a verb has multiple etymologies,
# and one of those is defective, then the word will show up here even the other
# etymologies are not defective.

# Taken from https://en.wiktionary.org/wiki/Category:Latin_active-only_verbs
ACTIVE_ONLY_VERBS: Final[set[str]] = {
    "abaeto", "abbaeto", "abbatizo", "abbito", "abito", "abluo", "abnumero", "abnuto", "abolesco", "abrenuntio", "absum",
    "abundo", "accedo", "accersio", "accieo", "accino", "accipitro", "accresco", "aceo", "acesco", "acontizo", "acquiesco",
    "adaestuo", "adambulo", "adaugesco", "adbito", "adcedo", "adcresco", "addecet", "addisco", "addormio", "addormisco",
    "adequito", "aderro", "adesurio", "adfleo", "adfremo", "adfrio", "adfulgeo", "adhaereo", "adhaeresco", "adheresco",
    "adhinnio", "adiaceo", "adincresco", "adito", "adjaceo", "adlubesco", "adluceo", "adludio", "adluo", "admeo", "admigro",
    "admugio", "admurmuro", "adnato", "adnavigo", "adno", "adnullo", "adnuto", "adoleo", "adolesco", "adpertineo", "adploro",
    "adquiesco", "adremigo", "adrepo", "adsibilo", "adsideo", "adsido", "adsisto", "adstrepo", "adstupeo", "adsum", "advento",
    "advesperascit", "advigilo", "aegresco", "aegroto", "aequivaleo", "aerugino", "aerusco", "aestivo", "affremo", "affugio",
    "affulgeo", "aiio", "aio", "albeo", "albesco", "alesco", "algeo", "algesco", "allegorizo", "alluceo", "amaresco", "amtruo",
    "annato", "annavigo", "annicto", "anno", "annuto", "antesto", "antevolo", "antisto", "apage", "apparesco", "appertineo",
    "apploro", "apposco", "arboresco", "ardesco", "areo", "aresco", "arguto", "arrepo", "assenesco", "assibilo", "assideo",
    "assido", "assisto", "assum", "astrepo", "astupeo", "augesco", "auresco", "auroresco", "aurugino", "autumnascit",
    "autumnescit", "autumno", "auxilio", "aveo", "babello", "baeto", "balbutio", "balo", "barbio", "barrio", "baulo", "bebo",
    "bello", "beneplaceo", "beto", "blatero", "bombio", "bombizo", "bubo", "bubulcito", "bullesco", "cacaturio", "calefacto",
    "caleo", "calesco", "calleo", "calveo", "cambio", "candeo", "candesco", "caneo", "canesco", "casso", "catulio", "caurio",
    "caverno", "cedo", "celebresco", "cenaturio", "ceveo", "cineresco", "circo", "circumcurso", "circumdoleo", "circumerro",
    "circumfulgeo", "circumgesto", "circumiaceo", "circumluceo", "circumluo", "circumpendeo", "circumsideo", "circumsido",
    "circumsilio", "circumstupeo", "circumvestio", "claresco", "clocito", "clueo", "cluo", "coacesco", "coalesco", "coest",
    "cohaereo", "cohaeresco", "cohereo", "colliquesco", "colluceo", "colludo", "commadeo", "commaneo", "commarceo", "commeto",
    "commiseresco", "commitigo", "commurmuro", "compareo", "compluit", "computresco", "concaleo", "concido", "concresco",
    "condecet", "condisco", "condoleo", "condormio", "condormisco", "confluo", "confulgeo", "congruo", "coniveo", "conluceo",
    "conludo", "conniveo", "conputresco", "conquiesco", "conquinisco", "conresurgo", "consanesco", "conscio", "consenesco",
    "consilesco", "consipio", "consono", "conspiro", "conspondeo", "consto", "constupeo", "consuadeo", "consurgo", "contabesco",
    "contenebresco", "conticeo", "contrasto", "contremesco", "contremo", "contumulo", "convaleo", "convalesco", "convecto", 
    "conviso", "cornesco", "correpo", "correspondeo", "corresurgo", "corrideo", "corusco", "crebesco", "crebresco", "crepo",
    "cresco", "crispio", "crocio", "crocito", "crotolo", "crudesco", "cubo", "cucio", "cucubo", "cucurio", "cursito", "decet",
    "decido", "decresco", "dedecet", "dedisco", "dedoleo", "deeo", "deferveo", "defervesco", "defloresco", "dego", "dehisco",
    "deliquesco", "deliro", "delitesco", "delitisco", "demano", "denarro", "denormo", "dependeo", "depropero", "derigeo",
    "desaevio", "descisco", "desenesco", "deserpo", "desideo", "desipio", "desisto", "destico", "desum", "desurgo", "devigesco",
    "diffingo", "diffleo", "diffluo", "diluceo", "dilucesco", "diluculat", "disconvenio", "discrepo", "dishiasco", "dispereo",
    "disserpo", "dissono", "dissuadeo", "dissulto", "distaedet", "disto", "ditesco", "doleo", "dormisco", "drenso", "drindio",
    "drivoro", "dulcesco", "duresco", "edisco", "edormio", "eduro", "effervesco", "effervo", "effloreo", "effloresco", "effulgeo",
    "egeo", "elanguesco", "elatro", "eluceo", "elucesco", "elugeo", "emacresco", "emaneo", "emarcesco", "emeto", "emineo",
    "enitesco", "equio", "equito", "erepo", "erugino", "escado", "eschado", "evanesco", "exacerbesco", "exalbesco", "exardesco",
    "exaresco", "exaugeo", "excado", "excandesco", "excido", "excresco", "exhorreo", "exilio", "existo", "exolesco", "expectoro",
    "exposco", "exserto", "exsilio", "exsisto", "exsolesco", "exsono", "exsto", "exsurgo", "extabesco", "exto", "exurgo",
    "fabrio", "fatisco", "felio", "fervesco", "fetesco", "fetifico", "fistulesco", "flaccesco", "flagro", "flaveo", "flavesco",
    "floreo", "floresco", "fluo", "folleo", "formico", "fraceo", "fracesco", "fraglo", "fragro", "frendesco", "frigeo",
    "frigesco", "frigutio", "frondeo", "frondesco", "frugesco", "fulgeo", "fulgesco", "fulgo", "furo", "gannio", "gestio",
    "gingrio", "glabresco", "glattio", "glaucio", "glisco", "glocio", "gloctoro", "glottoro", "gracillo", "grandesco",
    "grandinat", "gravesco", "grundio", "grunnio", "hebeo", "hebesco", "herbesco", "hilaresco", "hinnio", "hio", "hirrio",
    "hittio", "hiulco", "horripilo", "humeo", "iaceo", "ignesco", "illuceo", "immaneo", "immigro", "immineo", "immugio",
    "immurmuro", "inacesco", "inaestuo", "inalbeo", "inalbesco", "inambulo", "inaresco", "incalesco", "incalfacio", "incandesco",
    "incanesco", "incido", "incino", "inclaresco", "increbesco", "increbresco", "incresco", "incubo", "incumbo", "incurvesco",
    "indecoro", "induresco", "ineptio", "inerro", "infenso", "inferveo", "infervesco", "infremo", "ingravesco", "ingruo",
    "inhaereo", "inhaeresco", "inhorreo", "inhorresco", "inluceo", "inmaneo", "inmineo", "inquilino", "inscendo", "insenesco",
    "inserpo", "insibilo", "insilio", "insolesco", "insono", "instupeo", "insum", "intabesco", "intepeo", "interaresco",
    "interbito", "intercido", "intereo", "interequito", "interfugio", "interfulgeo", "interiaceo", "interjaceo", "interluceo",
    "intermaneo", "internecto", "interniteo", "intersono", "intersum", "intervolito", "intervolo", "intremo", "intribuo",
    "intumesco", "invaleo", "invalesco", "invergo", "inveterasco", "involito", "iuvenesco", "jaceo", "juvenesco", "labasco",
    "lactesco", "lallo", "lampo", "languesco", "lapidesco", "lassesco", "lateo", "latesco", "lentesco", "liceo", "limo", "lipio",
    "lippio", "liqueo", "liquesco", "longisco", "loretho", "luceo", "lucesco", "lucisco", "luo", "lutesco", "maceo", "maceresco",
    "macesco", "macresco", "madeo", "madesco", "malo", "marceo", "marcesco", "matresco", "maturesco", "maumo", "mellifico",
    "miccio", "mico", "mintrio", "minurrio", "miseresco", "miseret", "mitesco", "mitilo", "mollesco", "morigero", "muceo",
    "mucesco", "mugio", "murrio", "mutio", "muttio", "nausco", "nigresco", "ningit", "ninguit", "ninguo", "niteo", "nitesco",
    "nivesco", "no", "noctesco", "nolo", "notesco", "nupturio", "obaresco", "obatresco", "obbrutesco", "obdormisco", "obdulcesco",
    "obduresco", "obfulgeo", "obhorreoobiaceo", "objaceo", "oblitesco", "obmutesco", "oboleo", "obrigesco", "obsido", "obsolesco",
    "obsordesco", "obstipesco", "obstupesco", "obsum", "obsurdesco", "obtenebresco", "obticeo", "obtorpeo", "obvio", "occallesco",
    "occido", "offulgeo", "oggannio", "*oleo", "oleo", "olesco", "olo", "onco", "oportet", "oppedo", "oscito", "palleo",
    "pallesco", "palpebro", "palpito", "papo", "pappo", "passito", "pateo", "patesco", "pauperasco", "paupulo", "pauso", "pedo",
    "pelluceo", "pendeo", "percalleo", "percrebesco", "percrebresco", "perdo", "perdormisco", "pereffluo", "perferveo",
    "perhorreo", "perlateo", "perluceo", "permaneo", "permereo", "perniteo", "peroleo", "persedeo", "perserpo", "persilio",
    "persisto", "pertimeo", "pertineo", "pervaleo", "pervigeo", "pervolo", "pilpito", "pinguesco", "pipilo", "pipio", "pipo",
    "pisito", "plipio", "pluit", "plumesco", "pluo", "praeambulo", "praeemineo", "praefloreo", "praefugio", "praefulgeo",
    "praegestio", "praeiaceo", "praejaceo", "praeluceo", "praeniteo", "praeoleo", "praependeo", "praepolleo", "praesideo",
    "praesono", "praesum", "praeterfugio", "praetimeo", "praevaleo", "praevalesco", "procido", "prodeo", "profluo", "proluceo",
    "promineo", "propendeo", "proprio", "prorepo", "proserpo", "prosto", "prosum", "prurio", "pubesco", "pulpo", "purpurasco",
    "putesco", "putreo", "putresco", "quaxo", "quiesco", "quirrito", "rabio", "racco", "radicesco", "ranceo", "rancesco", "ranco",
    "ravio", "rebello", "recaleo", "recido", "recrepo", "recumbo", "redintegrasco", "redoleo", "redormio", "refert", "refloreo",
    "refluo", "refrigesco", "refulgeo", "relanguesco", "reluceo", "remaneo", "remollesco", "remugio", "renideo", "reniteo",
    "repauso", "repo", "repto", "resido", "resipisco", "resplendeo", "resurgo", "retono", "reviresco", "revivesco", "revivisco",
    "revivo", "ricio", "ricto", "rigesco", "rubesco", "rufesco", "rugio", "rumino", "sagio", "salveo", "sanesco", "sanguino",
    "sapio", "scabo", "scateo", "scato", "scaturio", "scaturrio", "scripturio", "secubo", "senesco", "seresco", "serpo", "sevio",
    "siccesco", "sido", "silesco", "soccito", "sordeo", "sordesco", "splendeo", "splendesco", "spumesco", "squaleo", "sternuo",
    "stinguo", "strideo", "strido", "stritto", "studeo", "stupeo", "stupesco", "subfulgeo", "subiaceo", "subjaceo", "subluceo",
    "suboleo", "subrepo", "subrubeo", "subsilio", "subsisto", "subsum", "subterfugio", "subteriaceo", "subterjaceo", "subtimeo",
    "succido", "succino", "succresco", "succubo", "sufferveo", "suffugio", "suffulgeo", "sugglutio", "sullaturio", "sum",
    "superbio", "supercresco", "supereffluo", "superemineo", "superfugio", "superiaceo", "superimmineo", "superjaceo",
    "superluceo", "superoccupo", "supersapio", "supersideo", "supersto", "supersum", "suprasedeo", "supterfugio", "surio",
    "tabeo", "tabesco", "tenebresco", "tenebrico", "tepeo", "tepesco", "tetrinnio", "tinnipo", "tintino", "torpeo", "torpesco",
    "traluceo", "transfluo", "transfugio", "transfulgeo", "transilio", "transluceo", "transpareo", "transvado", "transvenio",
    "trico", "trittilo", "trucilo", "tumeo", "tumesco", "turgeo", "turgesco", "tussio", "umbresco", "umeo", "umesco", "unco",
    "urco", "urvo", "vado", "vagio", "vago", "valeo", "valesco", "vanesco", "varico", "vento", "vero", "vesanio", "vesico",
    "vesperascit", "veterasco", "veteresco", "vigeo", "vigesco", "vireo", "viresco", "viridesco", "volito", "volo",
}  # fmt: skip

# Taken from https://en.wiktionary.org/wiki/Category:Latin_verbs_with_missing_supine_stem
# additions: possum (defective), nolo (defective)
# deletions: accido (two meanings), incumbo (probably mistake)
MISSING_PPP_VERBS: Final[set[str]] = {
    "abaeto", "abago", "abarceo", "abbaeto", "abbatizo", "abbito", "abequito", "aberceo", "abhorresco", "abito", "abiturio",
    "abnato", "abnumero", "abnuto", "abolesco", "aboriscor", "aborto", "abrenuntio", "absilio", "absisto", "absono", "absto",
    "abstulo", "accano", "accersio", "accessito", "accieo", "accipitro", "accubo", "aceo", "acesco", "acetasco",
    "acontizo", "adaestuo", "adambulo", "adaugesco", "adbello", "adbito", "adcubo", "addecet", "addenseo", "addisco", "addormio",
    "addormisco", "aderro", "adesurio", "adfleo", "adformido", "adfremo", "adfrio", "adfulgeo", "adgemo", "adgravesco", "adiaceo",
    "adincresco", "adjaceo", "adlubesco", "adluceo", "adludio", "adluo", "admeo", "admigro", "admugio", "adnicto", "adnubilo",
    "adnullo", "adnuto", "adnutrio", "adoleo", "adolesco", "adpertineo", "adploro", "adpostulo", "adprenso", "adremigo", "adrepo",
    "adservio", "adsibilo", "adsido", "adsisto", "adsono", "adsto", "adstrepo", "adstupeo", "adtolero", "adtollo", "adtorqueo",
    "adurgeo", "advecto", "advesperascit", "advivo", "aegreo", "aegresco", "aerusco", "affleo", "afformido", "affremo", "affrio",
    "affugio", "affulgeo", "aiio", "aio", "albeo", "albesco", "albicasco", "alesco", "algeo", "algesco", "allegorizo", "alluceo",
    "alludio", "alluo", "alto", "amaresco", "ambigo", "amtruo", "amylo", "annicto", "anno", "annubilo", "annuto", "annutrio",
    "antecello", "antecurro", "antepolleo", "antesto", "antevio", "antisto", "apage", "aperto", "apolactizo", "apotheco",
    "apozymo", "apparesco", "appertineo", "apploro", "apposco", "appostulo", "apprenso", "apricor", "arboresco", "ardesco",
    "areo", "aresco", "arguto", "arrepo", "assenesco", "asservio", "assibilo", "assido", "assisto", "assono", "astituo", "asto",
    "astrepo", "astrifico", "astupeo", "attolero", "attollo", "attorqueo", "attorreo", "aufugio", "augesco", "augifico",
    "auresco", "auroresco", "auroro", "aurugino", "autumnascit", "autumnescit", "autumno", "aveo", "baeto", "balbutio", "barbio",
    "batto", "battuo", "batuo", "baulo", "bebo", "bellor", "beto", "blatio", "bombio", "bovinor", "bubo", "bubulcito", "bullesco",
    "cacaturio", "calefacto", "calesco", "calleo", "calveo", "calvor", "cambio", "candeo", "candesco", "candico", "candifico",
    "caneo", "canesco", "carro", "casso", "catulio", "caumo", "caurio", "caverno", "cedo", "celebresco", "cenaturio", "ceveo",
    "cineresco", "cio", "circito", "circumcurro", "circumcurso", "circumdoleo", "circumerro", "circumfulgeo", "circumgesto",
    "circumiaceo", "circumluceo", "circumluo", "circumpendeo", "circumsido", "circumsilio", "circumsisto", "circumsto",
    "circumstupeo", "circumtergeo", "circumtono", "circumtorqueo", "circumtueor", "circumvado", "circumverto", "circumvestio",
    "circumvorto", "clango", "clareo", "claresco", "claudeo", "clocito", "clueo", "clueor", "cluo", "coacesco", "coexsisto",
    "cohaeresco", "cohorresco", "collineo", "colliquesco", "colluceo", "commadeo", "commaneo", "commarceo", "commemini",
    "commeto", "commiseresco", "commitigo", "compalpo", "comparco", "compasco", "compendo", "comperco", "compesco", "compluit",
    "comprecor", "computresco", "concaleo", "concalesco", "concallesco", "concido", "concupio", "condecet", "condenseo",
    "condisco", "condoleo", "condolesco", "condormio", "condormisco", "conferveo", "confervesco", "confluo", "conforio",
    "confremo", "confulgeo", "congemo", "congruo", "coniveo", "conluceo", "conniveo", "conpesco", "conputresco", "conquinisco",
    "conresurgo", "conrideo", "consanesco", "consarrio", "consenesco", "consilesco", "consimilo", "consipio", "consono",
    "constupeo", "consuadeo", "contabesco", "contenebresco", "conticeo", "conticesco", "conticisco", "continor", "contollo",
    "contrasto", "contremesco", "contremisco", "contremo", "contumulo", "convaleo", "convecto", "convergo", "converro",
    "convescor", "conviso", "convomo", "convorro", "cornesco", "correpo", "corresurgo", "corrideo", "cratio", "crebesco",
    "crebresco", "crispio", "crocio", "crotolo", "crudesco", "cucio", "cucubo", "cucurio", "cunio", "cupisco", "cursito",
    "decet", "decido", "decumbo", "dedecet", "dedisco", "dedoleo", "deeo", "defervesco", "defloreo", "defloresco", "defugio",
    "dego", "degulo", "dehisco", "delambo", "deliquesco", "deliro", "delitesco", "delitisco", "delumbo", "demadesco", "demolio",
    "denarro", "denormo", "denseo", "dependeo", "deposco", "depropero", "depudet", "derepo", "derigeo", "derigesco", "deruo",
    "desenesco", "deserpo", "desideo", "desido", "desipio", "desorbeo", "despecto", "despuo", "destico", "desuesco", "desurgo",
    "devigesco", "dicturio", "diffingo", "diffiteor", "diluceo", "dilucesco", "diluculat", "disconvenio", "discupio", "dishiasco",
    "dispecto", "dispereo", "disquiro", "dissero", "disserpo", "dissideo", "dissono", "dissulto", "distaedet", "disto", "ditesco",
    "divergo", "dormisco", "drenso", "drindio", "drivoro", "dulcesco", "duplo", "duresco", "edisco", "edormisco", "eduro",
    "effervesco", "effervo", "effloreo", "effloresco", "effluo", "effulgeo", "elanguesco", "elatro", "elego", "eluceo",
    "elucesco", "elugeo", "emacresco", "emarcesco", "ematuresco", "emeto", "emineo", "emolo", "eniteo", "enitesco", "enotesco",
    "equio", "ercisco", "erubesco", "erudero", "escado", "eschado", "evalesco", "evanesco", "evilesco", "exacerbesco",
    "exalbesco", "exaresco", "excado", "excandesco", "excido", "excommunico", "exhorreo", "exhorresco", "exilio", "existo",
    "exolesco", "expallesco", "expaveo", "expavesco", "expectoro", "expetesso", "expetisso", "exposco", "exserto", "exsilio",
    "exsolesco", "exsono", "exsplendesco", "extabesco", "extimesco", "extollo", "exurgeo", "fabrio", "faeteo", "fatisco", "felio",
    "fervesco", "feteo", "fetesco", "fetifico", "fistulesco", "flacceo", "flaccesco", "flagro", "flaveo", "flavesco", "floreo",
    "floresco", "foeteo", "folleo", "forio", "formico", "fraceo", "fracesco", "fraglo", "fragro", "frendesco", "frigefacto",
    "frigeo", "frigesco", "frigutio", "fritinnio", "frondeo", "frondesco", "frugesco", "frutesco", "fulgeo", "fulgesco", "fulgo",
    "furo", "furvesco", "gannio", "gingrio", "glabresco", "glabro", "glattio", "glaucio", "glisco", "glocio", "gloctoro",
    "glottoro", "gracillo", "graduo", "grandesco", "grandinat", "gravesco", "hebeo", "hebesco", "herbesco", "hercisco", "hiasco",
    "hilaresco", "hinnio", "hirrio", "hisco", "hittio", "horior", "horreo", "horresco", "horripilo", "humeo", "ignesco",
    "illuceo", "illucesco", "imbibo", "immadesco", "immaneo", "immineo", "immurmuro", "impedico", "impendeo", "inacesco",
    "inaestuo", "inalbeo", "inalbesco", "inambulo", "inardesco", "inaresco", "incalesco", "incalfacio", "incandesco", "incanesco",
    "incino", "inclaresco", "incolo", "increbesco", "increbresco", "incresco", "inculpo", "incurvesco", "indecoro", 
    "indigeo", "indolesco", "induresco", "ineptio", "infenso", "infervesco", "infindo", "infit", "infremo", "infrendo",
    "ingemesco", "ingemisco", "ingravesco", "ingruo", "inhaeresco", "inhorreo", "inhorresco", "inluceo", "inlucesco", "inmaneo",
    "inmineo", "innotesco", "inoboedio", "inquilino", "insenesco", "inserto", "insisto", "insolesco", "insono", "instabilio",
    "instimulo", "instupeo", "intabesco", "intepeo", "intepesco", "interaresco", "interbito", "intercido", "interequito",
    "interfluo", "interfugio", "interfulgeo", "interiaceo", "interjaceo", "interluceo", "intermaneo", "internecto", "interniteo",
    "interquiesco", "intersono", "intersto", "intervolito", "intollo", "intremo", "intribuo", "intumesco", "inurgeo", "invalesco",
    "invergo", "invesperascit", "inveterasco", "ito", "iuvenesco", "labasco", "lacteo", "lactesco", "lallo", "lampo", "lanceo",
    "lancio", "langueo", "languesco", "lapidesco", "lassesco", "lateo", "latesco", "lentesco", "lipio", "liqueo", "liquesco",
    "liquor", "liveo", "livido", "longisco", "loretho", "luceo", "lucesco", "lucisco", "luo", "lutesco", "maceo", "maceresco",
    "macesco", "macresco", "madeo", "madesco", "maereo", "maledictito", "mammo", "marceo", "marcesco", "matresco", "maturesco",
    "maumo", "medeor", "mellifico", "memini", "miccio", "mico", "mintrio", "minurrio", "miseresco", "miseret", "mitesco",
    "mitilo", "moereo", "molio", "mollesco", "moror", "muceo", "mucesco", "murrio", "mutio", "muttio", "nauculor", "nausco",
    "naviculor", "nigreo", "nigresco", "ningit", "ningo", "ninguit", "ninguo", "niteo", "nitesco", "nivesco", "no", "noctesco",
    "nominito", "notesco", "nubilo", "nupturio", "obaresco", "obatresco", "obaudio", "obbrutesco", "obducto", "obdulcesco",
    "obduresco", "obfulgeo", "obhorreo", "obiaceo", "objaceo", "oblanguesco", "oblitesco", "obmordeo", "obmutesco", "obnoxio",
    "oboleo", "obrigesco", "obsido", "obsono", "obsordesco", "obstipesco", "obstupesco", "obsurdesco", "obtenebresco", "obtexo",
    "obticeo", "obticesco", "obtingo", "obtorpeo", "obtorpesco", "obtueor", "occallesco", "occino", "offulgeo", "oleo", "olesco",
    "olo", "onco", "oporteo", "oportet", "oppedo", "optingo", "oscitor", "paedagogo", "palleo", "pallesco", "palpebro", "pangito",
    "papo", "pappo", "parturio", "passito", "pateo", "patesco", "patio", "patrisso", "patrizo", "pauperasco", "paveo", "pavesco",
    "pelluceo", "pendeo", "percalleo", "percrebesco", "percrebresco", "perdisco", "perdo", "perdormisco", "perducto", "pereffluo",
    "perferveo", "perfugio", "perhorreo", "perhorresco", "perlateo", "perlinio", "perluceo", "permereo", "perniteo", "peroleo",
    "perpetuito", "perscisco", "persedeo", "perserpo", "persilio", "persisto", "pertimeo", "pertimesco", "pertineo", "pertingo",
    "pertorqueo", "perurgeo", "perurgueo", "pervaleo", "pervigeo", "petesso", "petisso", "pilpito", "pinguesco", "pipilo",
    "pipio", "pipo", "pisito", "plecto", "plipio", "pluit", "plumesco", "pluo", "polleo", "populo", "porceo", "posco", "posteo",
    "praeambulo", "praeemineo", "praefloreo", "praefluo", "praefugio", "praefulgeo", "praegestio", "praeiaceo", "praejaceo",
    "praeluceo", "praemando", "praeniteo", "praeoleo", "praependeo", "praepolleo", "praesagio", "praeservio", "praesipio",
    "praesono", "praeterfluo", "praeterfugio", "praetimeo", "praevalesco", "procello", "procido", "profugio", "proluceo",
    "promineo", "propalo", "prurio", "psallo", "pubesco", "pulpo", "purgito", "purpurasco", "puteo", "putesco", "putreo",
    "putresco", "quirrito", "rabio", "racco", "radicesco", "ranceo", "rancesco", "ranco", "ravio", "rebullio", "recaleo",
    "recommoneo", "recrepo", "recumbo", "redintegrasco", "redoleo", "redormio", "reducto", "refello", "refert", "referveo",
    "refingo", "refloreo", "refrigesco", "refugio", "refulgeo", "relanguesco", "reluceo", "rememini", "reminisco", "reminiscor",
    "remollesco", "remugio", "reneo", "renideo", "reniteo", "rennuo", "renuo", "reporrigo", "reposco", "resipisco", "resisto",
    "resplendeo", "resto", "reticeo", "retono", "revindico", "reviresco", "revivesco", "revivisco", "revivo", "ricio", "ricto",
    "rigeo", "rigesco", "rubeo", "rubesco", "rufesco", "rugio", "ruo", "sacio", "sagio", "salveo", "sanesco", "sanguino", "sapio",
    "sardo", "satago", "scabo", "scateo", "scato", "scaturio", "scaturrio", "scopo", "scripturio", "seneo", "senesco", "sentisco",
    "seresco", "sevio", "siccesco", "sicilio", "sido", "sileo", "silesco", "singultio", "soccito", "sordeo", "sordesco",
    "sospito", "splendeo", "splendesco", "spumesco", "squaleo", "stabulo", "sternuo", "sterto", "stinguo", "stipendio",
    "strideo", "strido", "stritto", "studeo", "stupeo", "stupesco", "subdoceo", "subedo", "subfulgeo", "subiaceo", "subjaceo",
    "subluceo", "suboleo", "subrubeo", "subservio", "subsilio", "subsisto", "subsono", "subterfluo", "subterfugio", "subteriaceo",
    "subterjaceo", "subtimeo", "suburgeo", "subvolo", "subvolvo", "succido", "succino", "succubo", "sufferveo", "suffringo",
    "suffugio", "suffulgeo", "sugglutio", "sullaturio", "superbio", "supercresco", "supereffluo", "superemineo", "superextollo",
    "superfluo", "superfugio", "superfulgeo", "superiaceo", "superimmineo", "superjaceo", "superluceo", "superobruo",
    "supersapio", "supersto", "supertraho", "supervaleo", "supervivo", "supo", "suppedo", "supterfugio", "surio", "sustollo",
    "tabeo", "tabesco", "temno", "tenebresco", "tenebrico", "tenerasco", "tepeo", "tepesco", "tetrinnio", "tibicino", "timeo",
    "tinnipo", "tintino", "tongeo", "torculo", "torpeo", "torpesco", "traluceo", "transfluo", "transfulgeo", "transilio",
    "transluceo", "transpicio", "transtineo", "transvado", "transvenio", "tremesco", "tremisco", "trico", "trittilo", "trucilo",
    "tumeo", "tumesco", "tumido", "turgeo", "turgesco", "tussio", "udo", "umbresco", "umeo", "umesco", "unco", "urco", "urgeo",
    "urgueo", "urvo", "vacefio", "vado", "vagio", "vago", "valesco", "vanesco", "vanno", "vegeo", "vento", "verecundor", "vergo",
    "vervago", "vesanio", "vescor", "vesico", "vesperascit", "veterasco", "veteresco", "vibrisso", "vigeo", "vigesco", "vilesco",
    "vireo", "viresco", "viridesco", "vissio", "vitulor", "vivesco",
    "possum", "nolo",
}  # fmt: skip

# Taken from https://en.wiktionary.org/wiki/Category:Latin_verbs_with_missing_supine_stem_except_in_the_future_active_participle
FUTURE_ACTIVE_PARTICIPLE_VERBS: Final[set[str]] = {
    "absum", "adsum", "assum", "caleo", "coest", "desum", "discrepo", "egeo", "exsto", "exto", "ferio", "incido", "insto",
    "insum", "intersum", "obsto", "obsum", "paeniteo", "persto", "pervolo", "poeniteo", "praesum", "prosum", "subsum", "sum",
    "supersum", "volo",
}  # fmt: skip

# Taken from https://en.wiktionary.org/wiki/Category:Latin_verbs_with_missing_gerund
MISSING_GERUND_VERBS: Final[set[str]] = {
    "absum", "adsum", "aiio", "aio", "assum", "cedo", "coepi", "coest", "commemini", "desum", "inquam", "insum", "intersum",
    "libet", "lubet", "malo", "memini", "nolo", "obsum", "odi", "perlibet", "pervolo", "possum", "praesum", "prosum", "recoepi",
    "rememini", "subsum", "sum", "supersum", "volo",
}  # fmt: skip

# Taken from https://en.wiktionary.org/wiki/Category:Latin_verbs_with_missing_perfect_stem
MISSING_PERFECT_VERBS: Final[set[str]] = {
    "abaeto", "abago", "abarceo", "abbaeto", "abbito", "aberceo", "abhorresco", "abiturio", "abnato", "abnumero", "absono",
    "absto", "accessito", "accieo", "accipitro", "accubo", "acontizo", "adaugesco", "adbello", "adbito", "adcubo", "addenseo",
    "addormio", "addormisco", "adfleo", "adformido", "adfremo", "adfrio", "adgemo", "adgravesco", "adincresco", "adlubesco",
    "adludio", "admeo", "admugio", "adnicto", "adnubilo", "adnuto", "adnutrio", "adoleo", "adolesco", "adpostulo", "adprenso",
    "adservio", "adsibilo", "adsono", "adstrepo", "adtolero", "adtollo", "adtorqueo", "adurgeo", "advecto", "aegreo", "aegresco",
    "aerusco", "affleo", "afformido", "affremo", "affrio", "albeo", "albesco", "albicasco", "alesco", "alludio", "alto",
    "amaresco", "ambigo", "amoeno", "amtruo", "amylo", "annicto", "anno", "annubilo", "annuto", "annutrio", "antecello",
    "antecurro", "antepolleo", "antevio", "apage", "aperto", "apolactizo", "apotheco", "apozymo", "apparesco", "apposco",
    "appostulo", "apprenso", "arboresco", "arguto", "assenesco", "asservio", "assibilo", "assono", "astituo", "astrepo",
    "astrifico", "attolero", "attollo", "attorqueo", "attorreo", "auctifico", "augesco", "augifico", "auresco", "auroresco",
    "auroro", "aurugino", "autumnascit", "auxilio", "aveo", "baeto", "barbio", "bebo", "beto", "blandio", "blatio", "bombio",
    "bubo", "bubulcito", "bullesco", "cacaturio", "calefacto", "calesco", "calo", "calveo", "candico", "candifico", "carnifico", 
    "carro", "catulio", "caurio", "cedo", "celebresco", "cenaturio", "cineresco", "cio", "circito", "circumcurro", "circumdoleo",
    "circumgesto", "circumluo", "circumpendeo", "circumsido", "circumstupeo", "circumtergeo", "circumtorqueo", "circumverto",
    "circumvestio", "circumvorto", "clareo", "clarigo", "claudeo", "claudo", "clocito", "clueo", "cluo", "collineo", "commeto",
    "commiseresco", "commitigo", "compalpo", "compasco", "compendo", "concavo", "concupio", "condenseo", "condormio", "confarreo",
    "conresurgo", "conrideo", "consarrio", "consimilo", "consipio", "consuadeo", "contenebresco", "contigno", "contollo",
    "contumulo", "convaleo", "convecto", "convergo", "converro", "conviso", "convomo", "convorro", "cornesco", "corresurgo",
    "corrideo", "cratio", "crispio", "crocio", "crotolo", "cucurio", "cunio", "cupisco", "cursito", "deeo", "defloreo", "degravo",
    "degulo", "delambo", "delumbo", "demadesco", "demolio", "demordeo", "denarro", "denormo", "denseo", "depango", "depecto",
    "depropero", "derigeo", "deserpo", "desorbeo", "despecto", "despuo", "destico", "desuesco", "desurgo", "devigesco",
    "dicturio", "diffingo", "diiugo", "dilorico", "disconvenio", "discupio", "dishiasco", "disiugo", "dispecto", "displodo",
    "disquiro", "dissero", "disserpo", "dissulto", "distaedet", "ditesco", "diverbero", "divergo", "dormisco", "drenso",
    "drindio", "drivoro", "duplo", "edormisco", "eduro", "effervo", "effusco", "effutio", "elaqueo", "elatro", "ematuresco",
    "emeto", "emolo", "eniteo", "enotesco", "equio", "ercisco", "erudero", "eviscero", "exacerbesco", "excalfacio", "excarnifico",
    "excommunico", "exolesco", "expaveo", "expectoro", "expetesso", "expetisso", "exserto", "exsolesco", "exsplendesco", "exsto",
    "exterebro", "exto", "extollo", "exurgeo", "faeteo", "fatisco", "felio", "fervesco", "feteo", "fetesco", "fetifico",
    "fistulesco", "flacceo", "flavesco", "floresco", "foeteo", "folleo", "formico", "fraceo", "frendesco", "frigefacto",
    "frigutio", "fritinnio", "frugesco", "frutesco", "fulgesco", "furvesco", "gingrio", "glabresco", "glabro", "glattio",
    "glaucio", "glisco", "glocio", "gracillo", "graduo", "grandesco", "grandinat", "gravesco", "hebeo", "hebesco", "herbesco",
    "hercisco", "hiasco", "hilaresco", "hirrio", "hisco", "hittio", "hiulco", "horripilo", "humeo", "ignesco", "illuceo",
    "imbrico", "immordeo", "immurmuro", "impedico", "impendeo", "impeto", "impetrio", "inaestuo", "inalbeo", "inalbesco",
    "incalfacio", "incero", "inculpo", "incurvesco", "indecoro", "ineptio", "infenso", "infervesco", "infindo", "infrendo",
    "ingravesco", "inhaeresco", "inluceo", "inoboedio", "inserto", "insolesco", "instabilio", "instimulo", "intepesco",
    "interaresco", "interbito", "interequito", "intermaneo", "internecto", "intervolito", "intollo", "intribuo", "inurgeo",
    "invergo", "invesperascit", "kalo", "labasco", "lacteo", "lactesco", "lallo", "lanceo", "lancio", "langueo", "lapidesco",
    "largio", "lassesco", "latesco", "leno", "lentesco", "lipio", "liveo", "livido", "longisco", "loretho", "lucisco", "lutesco",
    "maceo", "maceresco", "macesco", "maledictito", "mammo", "marcesco", "matresco", "mellifico", "miccio", "mintrio", "minurrio",
    "miseresco", "mitesco", "mitilo", "moereo", "molio", "mollesco", "muceo", "mucesco", "murrio", "nausco", "nigreo", "nitesco",
    "nivesco", "noctesco", "nominito", "nubilo", "obaresco", "obatresco", "obducto", "obmordeo", "obnoxio", "obsido", "obsono",
    "obtenebresco", "obticeo", "obtorpeo", "offusco", "olesco", "olo", "onco", "oppedo", "paedagogo", "palpebro", "pangito",
    "passito", "patio", "patrisso", "patrizo", "pauperasco", "pavesco", "perdormisco", "perducto", "pereffluo", "perlinio",
    "perlino", "perpetuito", "perscisco", "pertingo", "pertorqueo", "petesso", "petisso", "pilo", "pilpito", "pinguesco",
    "pipilo", "pipio", "pipo", "pisito", "plecto", "plipio", "plumesco", "polleo", "populo", "porceo", "posteo", "praefluo",
    "praegestio", "praemando", "praemoveo", "praeoleo", "praependeo", "praeservio", "praeterfluo", "praetorqueo", "praevalesco",
    "procello", "procido", "propalo", "prurio", "pulpo", "purgito", "purpurasco", "puteo", "quadripartio", "quadruplo", "quatio",
    "quirrito", "rabio", "racco", "radicesco", "ranceo", "rancesco", "ranco", "ravio", "recommoneo", "redintegrasco", "redormio",
    "reducto", "refingo", "reminisco", "remollesco", "remollio", "remugio", "reneo", "reporrigo", "reposco", "retono",
    "revindico", "revivo", "ricio", "ricto", "rigeo", "rufesco", "ruo", "sacio", "sagio", "salivo", "sallo", "salveo", "sanesco",
    "sanguino", "sardo", "satago", "scopo", "scripturio", "seneo", "sentisco", "seresco", "sevio", "siccesco", "sicilio",
    "silesco", "singultio", "soccito", "sospito", "spumesco", "stabulo", "stinguo", "stritto", "subdoceo", "subinvideo",
    "subservio", "subsono", "subterfluo", "suburgeo", "subvolo", "subvolvo", "succino", "succubo", "suffringo", "sugglutio",
    "sullaturio", "superbio", "supereffluo", "superextollo", "superfulgeo", "superimmineo", "superluceo", "superobruo",
    "superoccupo", "supertraho", "supervaleo", "supervestio", "supo", "suppedo", "surio", "sustollo", "tenebresco", "tenerasco",
    "tetrinnio", "tibicino", "tinnipo", "tongeo", "torculo", "traluceo", "transluceo", "transpicio", "transtineo", "transvenio",
    "tremesco", "tremisco", "trico", "trittilo", "trucilo", "tueo", "tumeo", "tumido", "turgesco", "tussio", "umbresco", "umeo",
    "umesco", "unco", "urco", "urvo", "vanesco", "vanno", "vento", "vervago", "vesanio", "vesico", "veterasco", "veteresco",
    "vibrisso", "vieo", "vilesco", "viresco", "viridesco", "vissio",
}  # fmt: skip

# Taken from https://en.wiktionary.org/wiki/Category:Latin_verbs_with_missing_future
# deletions: cedo (two meanings), apage (not really a verb)
MISSING_FUTURE_VERBS: Final[set[str]] = {"adsoleo", "assoleo", "soleo"}

# Taken from https://en.wiktionary.org/wiki/Category:Latin_verbs_with_supine_stem_with_missing_future_active_participle
# deletions: all verbs ending in 'fio' (should be grouped with 'facio')
MISSING_FAP_VERBS: Final[set[str]] = {"libet", "lubet", "perlibet"}

# -----------------------------------------------------------------------------
# DEFECTIVE VERBS

DEFECTIVE_VERBS: Final[dict[str, Endings]] = {
    "inquam": {
        "Vpreactindsg1": "inquam",
        "Vpreactindsg2": "inquis",
        "Vpreactindsg3": "inquit",
        "Vpreactindpl1": "inquimus",
        "Vpreactindpl2": "inquitis",
        "Vpreactindpl3": "inquint",
        "Vimpactindsg3": "inquiebat",
        "Vfutactindsg2": "inquies",
        "Vfutactindsg3": "inquiet",
        "Vperactindsg1": "inquii",
        "Vperactindsg2": "inquisti",
        "Vperactindsg3": "inquit",
        "Vperactsbjsg3": "inquiat",
        "Vpreactipesg2": "inque",
    }
}

# -----------------------------------------------------------------------------
# IRREGULAR VERBS

# TODO: Expand these

type _IrregularVerb = Literal["sum", "possum", "volo", "nolo", "fero", "eo"]

IRREGULAR_VERB_CONJUGATION: Final[dict[_IrregularVerb, Conjugation]] = {
    "sum": 3,
    "possum": 3,
    "volo": 3,
    "nolo": 3,
    "fero": 3,
    "eo": 4,  # no idea if this really matters?
}

IRREGULAR_VERB_STEMS: Final[dict[_IrregularVerb, tuple[str, str]]] = {
    # (_inf_stem, _preptc_stem), unused or impossible stems are not provided
    "sum": ("", ""),
    "possum": ("", "pote"),
    "volo": ("vol", "vole"),
    "nolo": ("nol", "nole"),
    "fero": ("fer", "fere"),
    "eo": ("", "ie"),  # fourth conjugation-like?
}

IRREGULAR_VERB_CHANGES: Final[dict[_IrregularVerb, DictChanges[Ending]]] = {
    "sum": DictChanges(  # sum, esse, fui, futurus
        # perfective indicative and subjunctive, imperfect subjunctive are regular
        replacements={
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
            "Vfutactindsg1": "ero",
            "Vfutactindsg2": "eris",
            "Vfutactindsg3": "erit",
            "Vfutactindpl1": "erimus",
            "Vfutactindpl2": "eritis",
            "Vfutactindpl3": "erunt",
            "Vpreactsbjsg1": "sim",
            "Vpreactsbjsg2": "sis",
            "Vpreactsbjsg3": "sit",
            "Vpreactsbjpl1": "simus",
            "Vpreactsbjpl2": "sitis",
            "Vpreactsbjpl3": "sint",
            "Vpreactipesg2": "es",
            "Vpreactipepl2": "este",
            "Vfutactipesg2": "esto",
            "Vfutactipesg3": "esto",
            "Vfutactipepl2": "estote",
            "Vfutactipepl3": "sunto",
            "Vfutactinf   ": MultipleEndings(
                regular="futurum esse", second="fore"
            ),
        },
        additions={},
        # no passives, present participles
        deletions={re.compile(r"^.{4}pas.*$"), re.compile(r"^.preactptc.*$")},
    ),
    "possum": DictChanges(  # possum, posse, potui
        # perfective indicative and subjunctive, imperfect subjunctive are regular
        replacements={
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
            "Vfutactindsg1": "potero",
            "Vfutactindsg2": "poteris",
            "Vfutactindsg3": "poterit",
            "Vfutactindpl1": "poterimus",
            "Vfutactindpl2": "poteritis",
            "Vfutactindpl3": "poterunt",
            "Vpreactsbjsg1": "possim",
            "Vpreactsbjsg2": "possis",
            "Vpreactsbjsg3": "possit",
            "Vpreactsbjpl1": "possimus",
            "Vpreactsbjpl2": "possitis",
            "Vpreactsbjpl3": "possint",
        },
        additions={},
        # no imperatives, passives
        deletions={re.compile(r"^.{4}pas.*$"), re.compile(r"^.{7}ipe.*$")},
    ),
    "volo": DictChanges(  # volo, velle, volui, voliturus
        # only present indicative and subjunctive are irregular
        replacements={
            "Vpreactindsg2": "vis",
            "Vpreactindsg3": "vult",
            "Vpreactindpl1": "volumus",
            "Vpreactindpl2": "vultis",
            "Vpreactindpl3": "volunt",
            "Vpreactsbjsg1": "velim",
            "Vpreactsbjsg2": "velis",
            "Vpreactsbjsg3": "velit",
            "Vpreactsbjpl1": "velimus",
            "Vpreactsbjpl2": "velitis",
            "Vpreactsbjpl3": "velint",
        },
        additions={},
        # no imperatives, passives
        deletions={re.compile(r"^.{4}pas.*$"), re.compile(r"^.{7}ipe.*$")},
    ),
    "nolo": DictChanges(  # nolo, nolle, nolui
        # only present indicative and subjunctive, and imperative are irregular
        replacements={
            "Vpreactindsg1": "nolo",
            "Vpreactindsg2": "non vis",
            "Vpreactindsg3": "non vult",
            "Vpreactindpl1": "nolumus",
            "Vpreactindpl2": "non vultis",
            "Vpreactindpl3": "nolunt",
            "Vpreactsbjsg1": "nelim",
            "Vpreactsbjsg2": "nelis",
            "Vpreactsbjsg3": "nelit",
            "Vpreactsbjpl1": "nelimus",
            "Vpreactsbjpl2": "nelitis",
            "Vpreactsbjpl3": "nelint",
            "Vpreactipesg2": "noli",
            "Vpreactipepl2": "nolite",
        },
        additions={},
        # no passives
        deletions={re.compile(r"^.{4}pas.*$")},
    ),
    "fero": DictChanges(  # fero, ferre, tuli, latus
        # some forms are irregular
        replacements={
            "Vpreactindsg2": "fers",
            "Vpreactindsg3": "fert",
            "Vpreactindpl2": "fertis",
            "Vprepasindsg2": "ferris",
            "Vprepasindsg3": "fertur",
            "Vpreactipesg2": "fer",
            "Vpreactipepl2": "ferte",
            "Vprepasipesg2": "ferre",
            "Vprepasipepl2": "ferimini",
            "Vfutactipesg2": "ferto",
            "Vfutactipesg3": "ferto",
            "Vfutactipepl2": "fertote",
            "Vfutactipepl3": "ferunto",
            "Vfutpasipesg2": "fertor",
            "Vfutpasipesg3": "fertor",
            "Vfutpasipepl3": "feruntor",
            "Vprepasinf   ": "ferri",
        },
        additions={},
        deletions=set(),
    ),
    "eo": DictChanges(  # eo, ire, ii, itus
        # various forms are regular throughout
        replacements={
            "Vpreactindpl3": "eunt",
            "Vimpactindsg1": "ibam",
            "Vimpactindsg2": "ibas",
            "Vimpactindsg3": "ibat",
            "Vimpactindpl1": "ibamus",
            "Vimpactindpl2": "ibatis",
            "Vimpactindpl3": "ibant",
            "Vfutactindsg1": "ibo",
            "Vfutactindsg2": "ibis",
            "Vfutactindsg3": "ibit",
            "Vfutactindpl1": "ibimus",
            "Vfutactindpl2": "ibitis",
            "Vfutactindpl3": "ibunt",
            "Vperactindsg2": "isti",
            "Vperactindpl2": "istis",
            "Vprepasindsg1": "eor",
            "Vprepasindpl3": "euntur",
            "Vimppasindsg1": "ibar",
            "Vimppasindsg2": "ibaris",
            "Vimppasindsg3": "ibatur",
            "Vimppasindpl1": "ibamur",
            "Vimppasindpl2": "ibamini",
            "Vimppasindpl3": "ibantur",
            "Vfutpasindsg1": "ibor",
            "Vfutpasindsg2": "iberis",
            "Vfutpasindsg3": "ibitur",
            "Vfutpasindpl1": "ibimur",
            "Vfutpasindpl2": "ibimini",
            "Vfutpasindpl3": "ibuntur",
            "Vpreactsbjsg1": "eam",
            "Vpreactsbjsg2": "eas",
            "Vpreactsbjsg3": "eat",
            "Vpreactsbjpl1": "eamus",
            "Vpreactsbjpl2": "eatis",
            "Vpreactsbjpl3": "eant",
            "Vplpactsbjsg1": "issem",
            "Vplpactsbjsg2": "isses",
            "Vplpactsbjsg3": "isset",
            "Vplpactsbjpl1": "issemus",
            "Vplpactsbjpl2": "issetis",
            "Vplpactsbjpl3": "issent",
            "Vprepassbjsg1": "ear",
            "Vprepassbjsg2": "earis",
            "Vprepassbjsg3": "eatur",
            "Vprepassbjpl1": "eamur",
            "Vprepassbjpl2": "eamini",
            "Vprepassbjpl3": "eantur",
            "Vfutactipepl3": "eunto",
            "Vfutpasipepl3": "euntor",
            "Vperactinf   ": "isse",
            "Vpreactptcmaccsg": "euntem",
            "Vpreactptcmgensg": "euntis",
            "Vpreactptcmdatsg": "eunti",
            "Vpreactptcmablsg": MultipleEndings(
                regular="eunti", absolute="eunte"
            ),
            "Vpreactptcmnompl": "euntes",
            "Vpreactptcmvocpl": "euntes",
            "Vpreactptcmaccpl": "euntes",
            "Vpreactptcmgenpl": "euntium",
            "Vpreactptcmdatpl": "euntibus",
            "Vpreactptcmablpl": "euntibus",
            "Vpreactptcfaccsg": "euntem",
            "Vpreactptcfgensg": "euntis",
            "Vpreactptcfdatsg": "eunti",
            "Vpreactptcfablsg": MultipleEndings(
                regular="eunti", absolute="eunte"
            ),
            "Vpreactptcfnompl": "euntes",
            "Vpreactptcfvocpl": "euntes",
            "Vpreactptcfaccpl": "euntes",
            "Vpreactptcfgenpl": "euntium",
            "Vpreactptcfdatpl": "euntibus",
            "Vpreactptcfablpl": "euntibus",
            "Vpreactptcngensg": "euntis",
            "Vpreactptcndatsg": "eunti",
            "Vpreactptcnablsg": MultipleEndings(
                regular="eunti", absolute="eunte"
            ),
            "Vpreactptcnnompl": "euntia",
            "Vpreactptcnvocpl": "euntia",
            "Vpreactptcnaccpl": "euntia",
            "Vpreactptcngenpl": "euntium",
            "Vpreactptcndatpl": "euntibus",
            "Vpreactptcnablpl": "euntibus",
            "Vfutpasptcmnomsg": "eundus",
            "Vfutpasptcmvocsg": "eunde",
            "Vfutpasptcmaccsg": "eundum",
            "Vfutpasptcmgensg": "eundi",
            "Vfutpasptcmdatsg": "eundo",
            "Vfutpasptcmablsg": "eundo",
            "Vfutpasptcmnompl": "eundi",
            "Vfutpasptcmvocpl": "eundi",
            "Vfutpasptcmaccpl": "eundos",
            "Vfutpasptcmgenpl": "eundorum",
            "Vfutpasptcmdatpl": "eundis",
            "Vfutpasptcmablpl": "eundis",
            "Vfutpasptcfnomsg": "eunda",
            "Vfutpasptcfvocsg": "eunda",
            "Vfutpasptcfaccsg": "eundam",
            "Vfutpasptcfgensg": "eundae",
            "Vfutpasptcfdatsg": "eundae",
            "Vfutpasptcfablsg": "eunda",
            "Vfutpasptcfnompl": "eundae",
            "Vfutpasptcfvocpl": "eundae",
            "Vfutpasptcfaccpl": "eundas",
            "Vfutpasptcfgenpl": "eundarum",
            "Vfutpasptcfdatpl": "eundis",
            "Vfutpasptcfablpl": "eundis",
            "Vfutpasptcnnomsg": "eundum",
            "Vfutpasptcnvocsg": "eundum",
            "Vfutpasptcnaccsg": "eundum",
            "Vfutpasptcngensg": "eundi",
            "Vfutpasptcndatsg": "eundo",
            "Vfutpasptcnablsg": "eundo",
            "Vfutpasptcnnompl": "eunda",
            "Vfutpasptcnvocpl": "eunda",
            "Vfutpasptcnaccpl": "eunda",
            "Vfutpasptcngenpl": "eundorum",
            "Vfutpasptcndatpl": "eundis",
            "Vfutpasptcnablpl": "eundis",
            "Vgeracc": "eundum",
            "Vgergen": "eundi",
            "Vgerdat": "eundo",
            "Vgerabl": "eundo",
        },
        additions={},
        deletions=set(),
    ),
}


def is_irregular_verb(present: str) -> TypeIs[_IrregularVerb]:
    """Return whether a verb is irregular (not prefix) by its present stem.

    Parameters
    ----------
    present : str
        The present stem of the verb.

    Returns
    -------
    TypeIs[_IrregularVerbs]
        Whether the verb is irregular.
    """
    return present in IRREGULAR_VERB_CHANGES


def get_irregular_verb_conjugation(present: _IrregularVerb) -> Conjugation:
    """Return the conjugation of an irregular verb.

    Parameters
    ----------
    present : str
        The present stem of the verb.

    Returns
    -------
    Conjugation
        The conjugation of the verb.
    """
    return IRREGULAR_VERB_CONJUGATION[present]


def find_irregular_verb_stems(present: _IrregularVerb) -> tuple[str, str]:
    """Return the infinitive and present participle stem of an irregular verb.

    Parameters
    ----------
    present : _IrregularVerbs
    The irregular verb.

    Returns
    -------
    str
        The infinitive stem.
    str
        The present participle stem.
    """
    return IRREGULAR_VERB_STEMS[present]


def find_irregular_verb_changes(
    present: _IrregularVerb,
) -> DictChanges[Ending]:
    """Return the changes for an irregular verb.

    Parameters
    ----------
    present : _IrregularVerbs
        The irregular verb.

    Returns
    -------
    DictChanges[Ending]
        The endings changes.
    """
    return IRREGULAR_VERB_CHANGES[present]


# -----------------------------------------------------------------------------
# DERIVED IRREGULAR VERBS (prefix)

type _DerivedVerb = Annotated[
    str, "A verb that is derived from an irregular verb."
]
type _DerivedVerbGroups = Literal[
    "sum", "sum_preptc", "fero", "eo", "eo_impersonal_passive"
]

DERIVED_IRREGULAR_VERB_CONJUGATION: Final[
    dict[_DerivedVerbGroups, Conjugation]
] = {"sum": 3, "sum_preptc": 3, "fero": 3, "eo": 4, "eo_impersonal_passive": 4}


DERIVED_IRREGULAR_VERB_STEMS: Final[
    dict[_DerivedVerbGroups, tuple[str, str]]
] = {
    # (_inf_stem, _preptc_stem), unused or impossible stems are not provided
    "sum": ("", ""),
    "sum_preptc": ("", "se"),
    "fero": ("fer", "fere"),
    "eo": ("", "i"),
    "eo_impersonal_passive": ("", "i"),
}

DERIVED_IRREGULAR_VERBS: Final[dict[_DerivedVerbGroups, set[_DerivedVerb]]] = {
    "sum": {
        "adsum",
        "obsum",
        "desum",
        "insum",
        "intersum",
        "prosum",
        "subsum",
        "supersum",
    },
    "sum_preptc": {"absum", "praesum"},
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
    "eo": {
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
        "praetereo",
        "prodeo",
        "queo",
        "subeo",
        "transabeo",
        "transeo",
        "veneo",
    },
    "eo_impersonal_passive": {"abeo", "pereo", "redeo"},
}

DERIVED_IRREGULAR_CHANGES: Final[
    dict[_DerivedVerbGroups, Callable[[tuple[str, ...]], DictChanges[Ending]]]
] = {
    "sum": lambda x: DictChanges(  # e.g. adsum, adesse, adfui, adfuturus
        # perfective indicative and subjunctive, imperfect subjunctive are regular
        replacements={
            "Vpreactindsg2": f"{x[0]}es",
            "Vpreactindsg3": f"{x[0]}est",
            "Vpreactindpl1": f"{x[0]}sumus",
            "Vpreactindpl2": f"{x[0]}estis",
            "Vpreactindpl3": f"{x[0]}sunt",
            "Vimpactindsg1": f"{x[0]}eram",
            "Vimpactindsg2": f"{x[0]}eras",
            "Vimpactindsg3": f"{x[0]}erat",
            "Vimpactindpl1": f"{x[0]}eramus",
            "Vimpactindpl2": f"{x[0]}eratis",
            "Vimpactindpl3": f"{x[0]}erant",
            "Vfutactindsg1": f"{x[0]}ero",
            "Vfutactindsg2": f"{x[0]}eris",
            "Vfutactindsg3": f"{x[0]}erit",
            "Vfutactindpl1": f"{x[0]}erimus",
            "Vfutactindpl2": f"{x[0]}eritis",
            "Vfutactindpl3": f"{x[0]}erunt",
            "Vpreactsbjsg1": f"{x[0]}sim",
            "Vpreactsbjsg2": f"{x[0]}sis",
            "Vpreactsbjsg3": f"{x[0]}sit",
            "Vpreactsbjpl1": f"{x[0]}simus",
            "Vpreactsbjpl2": f"{x[0]}sitis",
            "Vpreactsbjpl3": f"{x[0]}sint",
            "Vpreactipesg2": f"{x[0]}es",
            "Vpreactipepl2": f"{x[0]}este",
            "Vfutactipesg2": f"{x[0]}esto",
            "Vfutactipesg3": f"{x[0]}esto",
            "Vfutactipepl2": f"{x[0]}estote",
            "Vfutactipepl3": f"{x[0]}sunto",
            "Vfutactinf   ": MultipleEndings(
                regular=f"{x[3]}futurum esse", second=f"{x[3]}fore"
            ),
        },
        additions={},
        # no passives, present participles
        deletions={re.compile(r"^.{4}pas.*$"), re.compile(r"^.preactptc.*$")},
    ),
    "sum_preptc": lambda x: DictChanges(  # e.g. absum, abesse, afui, afuturus
        # perfective indicative and subjunctive, imperfect subjunctive are regular
        replacements={
            "Vpreactindsg2": f"{x[0]}es",
            "Vpreactindsg3": f"{x[0]}est",
            "Vpreactindpl1": f"{x[0]}sumus",
            "Vpreactindpl2": f"{x[0]}estis",
            "Vpreactindpl3": f"{x[0]}sunt",
            "Vimpactindsg1": f"{x[0]}eram",
            "Vimpactindsg2": f"{x[0]}eras",
            "Vimpactindsg3": f"{x[0]}erat",
            "Vimpactindpl1": f"{x[0]}eramus",
            "Vimpactindpl2": f"{x[0]}eratis",
            "Vimpactindpl3": f"{x[0]}erant",
            "Vfutactindsg1": f"{x[0]}ero",
            "Vfutactindsg2": f"{x[0]}eris",
            "Vfutactindsg3": f"{x[0]}erit",
            "Vfutactindpl1": f"{x[0]}erimus",
            "Vfutactindpl2": f"{x[0]}eritis",
            "Vfutactindpl3": f"{x[0]}erunt",
            "Vpreactsbjsg1": f"{x[0]}sim",
            "Vpreactsbjsg2": f"{x[0]}sis",
            "Vpreactsbjsg3": f"{x[0]}sit",
            "Vpreactsbjpl1": f"{x[0]}simus",
            "Vpreactsbjpl2": f"{x[0]}sitis",
            "Vpreactsbjpl3": f"{x[0]}sint",
            "Vpreactipesg2": f"{x[0]}es",
            "Vpreactipepl2": f"{x[0]}este",
            "Vfutactipesg2": f"{x[0]}esto",
            "Vfutactipesg3": f"{x[0]}esto",
            "Vfutactipepl2": f"{x[0]}estote",
            "Vfutactipepl3": f"{x[0]}sunto",
            "Vfutactinf   ": MultipleEndings(
                regular=f"{x[3]}futurum esse", second=f"{x[3]}fore"
            ),
        },
        additions={},
        # no passives
        deletions={re.compile(r"^.{4}pas.*$")},
    ),
    "fero": lambda x: DictChanges(  # e.g. affero, afferre, attuli, allatus
        # some forms are irregular
        replacements={
            "Vpreactindsg2": f"{x[0]}fers",
            "Vpreactindsg3": f"{x[0]}fert",
            "Vpreactindpl2": f"{x[0]}fertis",
            "Vprepasindsg2": f"{x[0]}ferris",
            "Vprepasindsg3": f"{x[0]}fertur",
            "Vpreactipesg2": f"{x[0]}fer",
            "Vpreactipepl2": f"{x[0]}ferte",
            "Vprepasipesg2": f"{x[0]}ferre",
            "Vprepasipepl2": f"{x[0]}ferimini",
            "Vfutactipesg2": f"{x[0]}ferto",
            "Vfutactipesg3": f"{x[0]}ferto",
            "Vfutactipepl2": f"{x[0]}fertote",
            "Vfutactipepl3": f"{x[0]}ferunto",
            "Vfutpasipesg2": f"{x[0]}fertor",
            "Vfutpasipesg3": f"{x[0]}fertor",
            "Vfutpasipepl3": f"{x[0]}feruntor",
            "Vprepasinf   ": f"{x[0]}ferri",
        },
        additions={},
        deletions=set(),
    ),
    "eo": lambda x: DictChanges(  # e.g. adeo, adire, adii, aditus
        # various forms are regular throughout
        replacements={
            "Vpreactindpl3": f"{x[0]}eunt",
            "Vimpactindsg1": f"{x[0]}ibam",
            "Vimpactindsg2": f"{x[0]}ibas",
            "Vimpactindsg3": f"{x[0]}ibat",
            "Vimpactindpl1": f"{x[0]}ibamus",
            "Vimpactindpl2": f"{x[0]}ibatis",
            "Vimpactindpl3": f"{x[0]}ibant",
            "Vfutactindsg1": f"{x[0]}ibo",
            "Vfutactindsg2": f"{x[0]}ibis",
            "Vfutactindsg3": f"{x[0]}ibit",
            "Vfutactindpl1": f"{x[0]}ibimus",
            "Vfutactindpl2": f"{x[0]}ibitis",
            "Vfutactindpl3": f"{x[0]}ibunt",
            "Vperactindsg2": f"{x[2]}isti",
            "Vperactindpl2": f"{x[2]}istis",
            "Vprepasindsg1": f"{x[0]}eor",
            "Vprepasindpl3": f"{x[0]}euntur",
            "Vimppasindsg1": f"{x[0]}ibar",
            "Vimppasindsg2": f"{x[0]}ibaris",
            "Vimppasindsg3": f"{x[0]}ibatur",
            "Vimppasindpl1": f"{x[0]}ibamur",
            "Vimppasindpl2": f"{x[0]}ibamini",
            "Vimppasindpl3": f"{x[0]}ibantur",
            "Vfutpasindsg1": f"{x[0]}ibor",
            "Vfutpasindsg2": f"{x[0]}iberis",
            "Vfutpasindsg3": f"{x[0]}ibitur",
            "Vfutpasindpl1": f"{x[0]}ibimur",
            "Vfutpasindpl2": f"{x[0]}ibimini",
            "Vfutpasindpl3": f"{x[0]}ibuntur",
            "Vpreactsbjsg1": f"{x[0]}eam",
            "Vpreactsbjsg2": f"{x[0]}eas",
            "Vpreactsbjsg3": f"{x[0]}eat",
            "Vpreactsbjpl1": f"{x[0]}eamus",
            "Vpreactsbjpl2": f"{x[0]}eatis",
            "Vpreactsbjpl3": f"{x[0]}eant",
            "Vplpactsbjsg1": f"{x[2]}issem",
            "Vplpactsbjsg2": f"{x[2]}isses",
            "Vplpactsbjsg3": f"{x[2]}isset",
            "Vplpactsbjpl1": f"{x[2]}issemus",
            "Vplpactsbjpl2": f"{x[2]}issetis",
            "Vplpactsbjpl3": f"{x[2]}issent",
            "Vprepassbjsg1": f"{x[0]}ear",
            "Vprepassbjsg2": f"{x[0]}earis",
            "Vprepassbjsg3": f"{x[0]}eatur",
            "Vprepassbjpl1": f"{x[0]}eamur",
            "Vprepassbjpl2": f"{x[0]}eamini",
            "Vprepassbjpl3": f"{x[0]}eantur",
            "Vfutactipepl3": f"{x[0]}eunto",
            "Vfutpasipepl3": f"{x[0]}euntor",
            "Vperactinf   ": f"{x[2]}isse",
            "Vpreactptcmaccsg": f"{x[0]}euntem",
            "Vpreactptcmgensg": f"{x[0]}euntis",
            "Vpreactptcmdatsg": f"{x[0]}eunti",
            "Vpreactptcmablsg": MultipleEndings(
                regular=f"{x[0]}eunti", absolute=f"{x[0]}eunte"
            ),
            "Vpreactptcmnompl": f"{x[0]}euntes",
            "Vpreactptcmvocpl": f"{x[0]}euntes",
            "Vpreactptcmaccpl": f"{x[0]}euntes",
            "Vpreactptcmgenpl": f"{x[0]}euntium",
            "Vpreactptcmdatpl": f"{x[0]}euntibus",
            "Vpreactptcmablpl": f"{x[0]}euntibus",
            "Vpreactptcfaccsg": f"{x[0]}euntem",
            "Vpreactptcfgensg": f"{x[0]}euntis",
            "Vpreactptcfdatsg": f"{x[0]}eunti",
            "Vpreactptcfablsg": MultipleEndings(
                regular=f"{x[0]}eunti", absolute=f"{x[0]}eunte"
            ),
            "Vpreactptcfnompl": f"{x[0]}euntes",
            "Vpreactptcfvocpl": f"{x[0]}euntes",
            "Vpreactptcfaccpl": f"{x[0]}euntes",
            "Vpreactptcfgenpl": f"{x[0]}euntium",
            "Vpreactptcfdatpl": f"{x[0]}euntibus",
            "Vpreactptcfablpl": f"{x[0]}euntibus",
            "Vpreactptcngensg": f"{x[0]}euntis",
            "Vpreactptcndatsg": f"{x[0]}eunti",
            "Vpreactptcnablsg": MultipleEndings(
                regular=f"{x[0]}eunti", absolute=f"{x[0]}eunte"
            ),
            "Vpreactptcnnompl": f"{x[0]}euntia",
            "Vpreactptcnvocpl": f"{x[0]}euntia",
            "Vpreactptcnaccpl": f"{x[0]}euntia",
            "Vpreactptcngenpl": f"{x[0]}euntium",
            "Vpreactptcndatpl": f"{x[0]}euntibus",
            "Vpreactptcnablpl": f"{x[0]}euntibus",
        },
        additions={},
        deletions=set(),
    ),
    "eo_impersonal_passive": lambda x: DictChanges(  # e.g. abeo, abire, abii, abitus
        # various forms are regular throughout
        replacements={
            "Vpreactindpl3": f"{x[0]}eunt",
            "Vimpactindsg1": f"{x[0]}ibam",
            "Vimpactindsg2": f"{x[0]}ibas",
            "Vimpactindsg3": f"{x[0]}ibat",
            "Vimpactindpl1": f"{x[0]}ibamus",
            "Vimpactindpl2": f"{x[0]}ibatis",
            "Vimpactindpl3": f"{x[0]}ibant",
            "Vfutactindsg1": f"{x[0]}ibo",
            "Vfutactindsg2": f"{x[0]}ibis",
            "Vfutactindsg3": f"{x[0]}ibit",
            "Vfutactindpl1": f"{x[0]}ibimus",
            "Vfutactindpl2": f"{x[0]}ibitis",
            "Vfutactindpl3": f"{x[0]}ibunt",
            "Vimppasindsg3": f"{x[0]}ibatur",
            "Vfutpasindsg3": f"{x[0]}ibitur",
            "Vperactindsg2": f"{x[2]}isti",
            "Vperactindpl2": f"{x[2]}istis",
            "Vpreactsbjsg3": f"{x[0]}eat",
            "Vplpactsbjsg1": f"{x[2]}issem",
            "Vplpactsbjsg2": f"{x[2]}isses",
            "Vplpactsbjsg3": f"{x[2]}isset",
            "Vplpactsbjpl1": f"{x[2]}issemus",
            "Vplpactsbjpl2": f"{x[2]}issetis",
            "Vplpactsbjpl3": f"{x[2]}issent",
            "Vpreactptcmaccsg": f"{x[0]}euntem",
            "Vpreactptcmgensg": f"{x[0]}euntis",
            "Vpreactptcmdatsg": f"{x[0]}eunti",
            "Vpreactptcmablsg": MultipleEndings(
                regular=f"{x[0]}eunti", absolute=f"{x[0]}eunte"
            ),
            "Vpreactptcmnompl": f"{x[0]}euntes",
            "Vpreactptcmvocpl": f"{x[0]}euntes",
            "Vpreactptcmaccpl": f"{x[0]}euntes",
            "Vpreactptcmgenpl": f"{x[0]}euntium",
            "Vpreactptcmdatpl": f"{x[0]}euntibus",
            "Vpreactptcmablpl": f"{x[0]}euntibus",
            "Vpreactptcfaccsg": f"{x[0]}euntem",
            "Vpreactptcfgensg": f"{x[0]}euntis",
            "Vpreactptcfdatsg": f"{x[0]}eunti",
            "Vpreactptcfablsg": MultipleEndings(
                regular=f"{x[0]}eunti", absolute=f"{x[0]}eunte"
            ),
            "Vpreactptcfnompl": f"{x[0]}euntes",
            "Vpreactptcfvocpl": f"{x[0]}euntes",
            "Vpreactptcfaccpl": f"{x[0]}euntes",
            "Vpreactptcfgenpl": f"{x[0]}euntium",
            "Vpreactptcfdatpl": f"{x[0]}euntibus",
            "Vpreactptcfablpl": f"{x[0]}euntibus",
            "Vpreactptcngensg": f"{x[0]}euntis",
            "Vpreactptcndatsg": f"{x[0]}eunti",
            "Vpreactptcnablsg": MultipleEndings(
                regular=f"{x[0]}eunti", absolute=f"{x[0]}eunte"
            ),
            "Vpreactptcnnompl": f"{x[0]}euntia",
            "Vpreactptcnvocpl": f"{x[0]}euntia",
            "Vpreactptcnaccpl": f"{x[0]}euntia",
            "Vpreactptcngenpl": f"{x[0]}euntium",
            "Vpreactptcndatpl": f"{x[0]}euntibus",
            "Vpreactptcnablpl": f"{x[0]}euntibus",
        },
        additions={},
        deletions=set(),
    ),
}

_DERIVED_PRINCIPAL_STEMS: Final[
    dict[_DerivedVerbGroups, tuple[str, str, str, str]]
] = {
    "sum": ("sum", "esse", "fui", "futurus"),
    "sum_preptc": ("sum", "esse", "fui", "futurus"),
    "fero": ("fero", "ferre", "tuli", "latus"),
    "eo": ("eo", "ire", "ii", "itus"),
    "eo_impersonal_passive": ("eo", "ire", "ii", "itus"),
}


def is_derived_verb(present: str) -> TypeIs[_DerivedVerb]:
    """Return whether a verb is irregular (not prefix) by its present stem.

    Parameters
    ----------
    present : str
        The present stem of the verb.

    Returns
    -------
    TypeIs[_DerivedVerb]
        The irregular verb.
    """
    return any(present in group for group in DERIVED_IRREGULAR_VERBS.values())


def _find_derived_verb_group(present: _DerivedVerb) -> _DerivedVerbGroups:
    for group_name, group in DERIVED_IRREGULAR_VERBS.items():
        if present in group:
            return group_name

    raise AssertionError("unreachable")


def get_derived_verb_conjugation(present: _DerivedVerb) -> Conjugation:
    """Return the conjugation of an derived verb.

    Parameters
    ----------
    present : _DerivedVerb
        The present stem of the verb.

    Returns
    -------
    Conjugation
        The conjugation of the verb.
    """
    return DERIVED_IRREGULAR_VERB_CONJUGATION[
        _find_derived_verb_group(present)
    ]


def find_derived_verb_stems(present: _DerivedVerb) -> tuple[str, str]:
    """Return the infinitive and present participle stem of a derived verb.

    Parameters
    ----------
    present : _DerivedVerb
        The present stem of the verb.

    Returns
    -------
    str
        The infinitive stem.
    str
        The present participle stem.
    """
    group = _find_derived_verb_group(present)
    return cast(
        "tuple[str, str]",
        tuple(
            present.removesuffix(_DERIVED_PRINCIPAL_STEMS[group][0]) + stem
            for stem in DERIVED_IRREGULAR_VERB_STEMS[group]
        ),
    )


def find_derived_verb_changes(
    principal_parts: tuple[str, ...],
) -> DictChanges[Ending]:
    """Find the changes for a derived verb.

    Strip the main part from the principal parts (e.g. absum -> ab-), and
    generate endings changes using that.

    Parameters
    ----------
    principal_parts : tuple[str, ...]
        The principal parts of the verb.

    Returns
    -------
    DictChanges[Ending]
        The endings changes.
    """
    group = _find_derived_verb_group(principal_parts[0])
    derived_principal_stems = _DERIVED_PRINCIPAL_STEMS[group]
    return DERIVED_IRREGULAR_CHANGES[group](
        tuple(
            pp.removesuffix(derived_principal_stems[i])
            for i, pp in enumerate(principal_parts)
        )
    )


# -----------------------------------------------------------------------------
# NOUNS

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

IRREGULAR_DECLINED_NOUNS: Final[dict[str, Endings]] = {
    "deus": {
        "Nnomsg": "deus",
        "Nvocsg": MultipleEndings(regular="dee", second="deus"),
        "Naccsg": "deum",
        "Ngensg": "dei",
        "Ndatsg": "deo",
        "Nablsg": "deo",
        "Nnompl": MultipleEndings(regular="dei", second="di", third="dii"),
        "Nvocpl": MultipleEndings(regular="dei", second="di", third="dii"),
        "Naccpl": "deos",
        "Ngenpl": MultipleEndings(regular="deorum", second="deum"),
        "Ndatpl": MultipleEndings(regular="deis", second="dis", third="diis"),
        "Nablpl": MultipleEndings(regular="deis", second="dis", third="diis"),
    },
    "dea": {
        "Nnomsg": "dea",
        "Nvocsg": "dea",
        "Naccsg": "deam",
        "Ngensg": "deae",
        "Ndatsg": "deae",
        "Nablsg": "dea",
        "Nnompl": "deae",
        "Nvocpl": "deae",
        "Naccpl": "deas",
        "Ngenpl": "dearum",
        "Ndatpl": "deabus",
        "Nablpl": "deabus",
    },
    "domus": {  # domus will be considered as a fourth declension noun only
        "Nnomsg": "domus",
        "Nvocsg": "domus",
        "Naccsg": "domum",
        "Ngensg": MultipleEndings(regular="domus", locative="domi"),
        "Ndatsg": MultipleEndings(
            regular="domui", second="domo", third="domu"
        ),
        "Nablsg": MultipleEndings(  # for consistency
            regular="domu", second="domo"
        ),
        "Nnompl": "domus",
        "Nvocpl": "domus",
        "Naccpl": MultipleEndings(regular="domus", second="domos"),
        "Ngenpl": MultipleEndings(regular="domuum", second="domorum"),
        "Ndatpl": "domibus",
        "Nablpl": "domibus",
    },
    "bos": {
        "Nnomsg": "bos",
        "Nvocsg": "bos",
        "Naccsg": "bovem",
        "Ngensg": "bovis",
        "Ndatsg": "bovi",
        "Nablsg": "bove",
        "Nnompl": "boves",
        "Nvocpl": "boves",
        "Naccpl": "boves",
        "Ngenpl": MultipleEndings(
            regular="bovum", second="boum", third="boverum"
        ),
        "Ndatpl": MultipleEndings(
            regular="bovibus", second="bobus", third="bubus"
        ),
        "Nablpl": MultipleEndings(
            regular="bovibus", second="bobus", third="bubus"
        ),
    },
    "epulum": {
        "Nnomsg": "epulum",
        "Nvocsg": "epulum",
        "Naccsg": "epulum",
        "Ngensg": "epuli",
        "Ndatsg": "epulo",
        "Nablsg": "epulo",
        "Nnompl": MultipleEndings(regular="epula", second="epulae"),
        "Nvocpl": MultipleEndings(regular="epula", second="epulae"),
        "Naccpl": MultipleEndings(regular="epula", second="epulas"),
        "Ngenpl": MultipleEndings(regular="epulorum", second="epularum"),
        "Ndatpl": "epulis",
        "Nablpl": "epulis",
    },
    "sus": {
        "Nnomsg": "sus",
        "Nvocsg": "sus",
        "Naccsg": "suem",
        "Ngensg": "suis",
        "Ndatsg": "sui",
        "Nablsg": "sue",
        "Nnompl": "sues",
        "Nvocpl": "sues",
        "Naccpl": "sues",
        "Ngenpl": "suum",
        "Ndatpl": MultipleEndings(regular="suibus", second="subus"),
        "Nablpl": MultipleEndings(regular="suibus", second="subus"),
    },
}

# -----------------------------------------------------------------------------
# ADJECTIVES

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

# -----------------------------------------------------------------------------
# PRONOUNS

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
