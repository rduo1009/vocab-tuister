"""Contains edge case endings."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Annotated, Final, Literal, TypeIs, cast

from ...utils.dict_changes import DictChanges
from .misc import MultipleEndings

if TYPE_CHECKING:
    from collections.abc import Callable

    from .type_aliases import Conjugation, Ending, Endings

# TODO: Change formatting to make it clear that lines be longer here to 130 e.g. with below horizontal line
# -----------------------------------------------------------------------------
# DEFECTIVE VERBS

# FIXME: These lists are incorrect in places. If a verb has multiple etymologies,
# and one of those is defective, then the word will show up here even the other
# etymologies are not defective.

# Taken from https://en.wiktionary.org/wiki/Category:Latin_active-only_verbs
# deletions: cedo (multiple etymologies)
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
    "caverno", "celebresco", "cenaturio", "ceveo", "cineresco", "circo", "circumcurso", "circumdoleo", "circumerro",
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

# FIXME: Handling 'accido' with multiple meanings is broken
# Taken from https://en.wiktionary.org/wiki/Category:Latin_verbs_with_missing_supine_stem
# additions: possum (defective), nolo (defective), malo (defective)
# deletions: incumbo (probably mistake), ruo (multiple etymologies), cedo (multiple etymologies)
MISSING_PPP_VERBS: Final[set[str]] = {
    "abaeto", "abago", "abarceo", "abbaeto", "abbatizo", "abbito", "abequito", "aberceo", "abhorresco", "abito", "abiturio",
    "abnato", "abnumero", "abnuto", "abolesco", "aboriscor", "aborto", "abrenuntio", "absilio", "absisto", "absono", "absto",
    "abstulo", "accano", "accersio", "accessito", "accido", "accieo", "accipitro", "accubo", "aceo", "acesco", "acetasco",
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
    "caneo", "canesco", "carro", "casso", "catulio", "caumo", "caurio", "caverno", "celebresco", "cenaturio", "ceveo",
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
    "rigeo", "rigesco", "rubeo", "rubesco", "rufesco", "rugio", "sacio", "sagio", "salveo", "sanesco", "sanguino", "sapio",
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
    "possum", "nolo", "malo",
}  # fmt: skip

# Taken from https://en.wiktionary.org/wiki/Category:Latin_verbs_with_missing_supine_stem_except_in_the_future_active_participle
FUTURE_ACTIVE_PARTICIPLE_VERBS: Final[set[str]] = {
    "absum", "adsum", "assum", "caleo", "coest", "desum", "discrepo", "egeo", "exsto", "exto", "ferio", "incido", "insto",
    "insum", "intersum", "obsto", "obsum", "paeniteo", "persto", "pervolo", "poeniteo", "praesum", "prosum", "subsum", "sum",
    "supersum", "volo",
}  # fmt: skip

# Taken from https://en.wiktionary.org/wiki/Category:Latin_verbs_with_missing_gerund
# deletions: cedo (multiple etymologies)
MISSING_GERUND_VERBS: Final[set[str]] = {
    "absum", "adsum", "aiio", "aio", "assum", "coepi", "coest", "commemini", "desum", "inquam", "insum", "intersum",
    "libet", "lubet", "malo", "memini", "nolo", "obsum", "odi", "perlibet", "pervolo", "possum", "praesum", "prosum", "recoepi",
    "rememini", "subsum", "sum", "supersum", "volo",
}  # fmt: skip

# Taken from https://en.wiktionary.org/wiki/Category:Latin_verbs_with_missing_perfect_stem
# deletions: ruo (multiple etymologies), claudo (multiple etymologies), cedo (multiple etymologies)
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
    "carro", "catulio", "caurio", "celebresco", "cenaturio", "cineresco", "cio", "circito", "circumcurro", "circumdoleo",
    "circumgesto", "circumluo", "circumpendeo", "circumsido", "circumstupeo", "circumtergeo", "circumtorqueo", "circumverto",
    "circumvestio", "circumvorto", "clareo", "clarigo", "claudeo", "clocito", "clueo", "cluo", "collineo", "commeto",
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
    "revindico", "revivo", "ricio", "ricto", "rigeo", "rufesco", "sacio", "sagio", "salivo", "sallo", "salveo", "sanesco",
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
# deletions: cedo (multiple etymologies), apage (not really a verb)
MISSING_FUTURE_VERBS: Final[set[str]] = {"adsoleo", "assoleo", "soleo"}

# Taken from https://en.wiktionary.org/wiki/Category:Latin_verbs_with_supine_stem_with_missing_future_active_participle
# deletions: all verbs ending in 'fio' (should be grouped with 'facio')
MISSING_FAP_VERBS: Final[set[str]] = {"libet", "lubet", "perlibet"}

# Taken from https://en.wiktionary.org/wiki/Category:Latin_impersonal_verbs
# many deletions as there are some regular verbs with impersonal meanings placed here
IMPERSONAL_VERBS: Final[set[str]] = {
    "advesperascit", "autumnascit", "autumnescit", "coest", "compluit", "depudet", "diluculat", "dispudet", "distaedet",
    "grandinat", "impluit", "infit", "invesperascit", "libet", "lubet", "miseret", "ningit", "ninguit", "oportet", "perlibet",
    "pertaedet", "piget", "pluit", "refert", "taedet", "vesperascit",
}  # fmt: skip

# Taken from https://en.wiktionary.org/wiki/Category:Latin_verbs_with_impersonal_passive
# NOTE: Some verbs in here might be 'impersonal in the passive in Old Latin', not sure if that counts?
IMPERSONAL_PASSIVE_VERBS: Final[set[str]] = {
    "abaestuo", "abambulo", "abeo", "abequito", "abludo", "abnato", "abnocto", "aborto", "absilio", "absisto", "absono", "absto",
    "accano", "accapito", "accessito", "accubo", "adcubo", "adfluo", "adservio", "adsto", "adsurgo", "advenio", "advivo",
    "affluo", "antevenio", "asservio", "assurgo", "asto", "aufugio", "buccino", "bucino", "cado", "concubo", "concumbo",
    "conferveo", "confugio", "consisto", "convivo", "curso", "decumbo", "defluo", "depoclo", "diffugio", "dissideo", "dormio",
    "evenio", "faveo", "ferveo", "fervo", "hymnio", "inoboedio", "insanio", "insisto", "intersto", "lapso", "ningo", "obsisto",
    "obsto", "paeniteo", "pareo", "perdoleo", "pereo", "perfluo", "perfugio", "persto", "pervenio", "poeniteo", "possum",
    "profugio", "psallo", "redeo", "referveo", "refugio", "resilio", "resisto", "resto", "revenio", "saevio", "sedeo", "servio",
    "sterto", "sto", "subservio", "subvenio", "supervivo", "usito", "vapulo", "venio", "victito", "vivo", "volo", "vomito",
}  # fmt: skip

# -----------------------------------------------------------------------------
# FULLY DEFECTIVE VERBS
# (verbs where it is more convenient to simply define the endings manually)

DEFECTIVE_VERBS: Final[dict[str, Endings]] = {
    "inquam": {
        "Vpreactindsg1": "inquam",    "Vpreactindsg2": "inquis",   "Vpreactindsg3": "inquit",
        "Vpreactindpl1": "inquimus",  "Vpreactindpl2": "inquitis", "Vpreactindpl3": "inquint",
        "Vimpactindsg3": "inquiebat", "Vfutactindsg2": "inquies",  "Vfutactindsg3": "inquiet",
        "Vperactindsg1": "inquii",    "Vperactindsg2": "inquisti", "Vperactindsg3": "inquit",
        "Vperactsbjsg3": "inquiat",
        "Vpreactipesg2": "inque",
    },
    "coepi": {
        "Vperactindsg1"   : "coepi",           "Vperactindsg2"   : "coepisti",        "Vperactindsg3"   : "coepit",
        "Vperactindpl1"   : "coepimus",        "Vperactindpl2"   : "coepistis",       "Vperactindpl3"   : "coeperunt",
        "Vplpactindsg1"   : "coeperam",        "Vplpactindsg2"   : "coeperas",        "Vplpactindsg3"   : "coeperat",
        "Vplpactindpl1"   : "coeperamus",      "Vplpactindpl2"   : "coeperatis",      "Vplpactindpl3"   : "coeperant",
        "Vfpractindsg1"   : "coepero",         "Vfpractindsg2"   : "coeperis",        "Vfpractindsg3"   : "coeperit",
        "Vfpractindpl1"   : "coeperimus",      "Vfpractindpl2"   : "coeperitis",      "Vfpractindpl3"   : "coeperint",
        "Vperpasindsg1"   : "coeptus sum",     "Vperpasindsg2"   : "coeptus es",      "Vperpasindsg3"   : "coeptus est",
        "Vperpasindpl1"   : "coeptus sumus",   "Vperpasindpl2"   : "coeptus estis",   "Vperpasindpl3"   : "coeptus sunt",
        "Vplppasindsg1"   : "coeptus eram",    "Vplppasindsg2"   : "coeptus eras",    "Vplppasindsg3"   : "coeptus erat",
        "Vplppasindpl1"   : "coeptus eramus",  "Vplppasindpl2"   : "coeptus eratis",  "Vplppasindpl3"   : "coeptus erant",
        "Vfprpasindsg1"   : "coeptus ero",     "Vfprpasindsg2"   : "coeptus eris",    "Vfprpasindsg3"   : "coeptus erit",
        "Vfprpasindpl1"   : "coeptus erimus",  "Vfprpasindpl2"   : "coeptus eritis",  "Vfprpasindpl3"   : "coeptus erunt",
        "Vperactsbjsg1"   : "coeperim",        "Vperactsbjsg2"   : "coeperis",        "Vperactsbjsg3"   : "coeperit",
        "Vperactsbjpl1"   : "coeperimus",      "Vperactsbjpl2"   : "coeperitis",      "Vperactsbjpl3"   : "coeperint",
        "Vplpactsbjsg1"   : "coepissem",       "Vplpactsbjsg2"   : "coepisses",       "Vplpactsbjsg3"   : "coepisset",
        "Vplpactsbjpl1"   : "coepissemus",     "Vplpactsbjpl2"   : "coepissetis",     "Vplpactsbjpl3"   : "coepissent",
        "Vperpassbjsg1"   : "coeptus sim",     "Vperpassbjsg2"   : "coeptus sis",     "Vperpassbjsg3"   : "coeptus sit",
        "Vperpassbjpl1"   : "coeptus simus",   "Vperpassbjpl2"   : "coeptus sitis",   "Vperpassbjpl3"   : "coeptus sint",
        "Vplppassbjsg1"   : "coeptus essem",   "Vplppassbjsg2"   : "coeptus esses",   "Vplppassbjsg3"   : "coeptus esset",
        "Vplppassbjpl1"   : "coeptus essemus", "Vplppassbjpl2"   : "coeptus essetis", "Vplppassbjpl3"   : "coeptus essent",
        "Vfutactinf   "   : "coepturus esse",  "Vperactinf   "   : "coepisse",
        "Vfutpasinf   "   : "coeptum iri",     "Vperpasinf   "   : "coeptus esse",
        "Vfutactptcmnomsg": "coepturus",       "Vfutactptcmvocsg": "coepture",        "Vfutactptcmaccsg": "coepturum",
        "Vfutactptcmgensg": "coepturi",        "Vfutactptcmdatsg": "coepturo",        "Vfutactptcmablsg": "coepturo",
        "Vfutactptcmnompl": "coepturi",        "Vfutactptcmvocpl": "coepturi",        "Vfutactptcmaccpl": "coepturos",
        "Vfutactptcmgenpl": "coepturorum",     "Vfutactptcmdatpl": "coepturis",       "Vfutactptcmablpl": "coepturis",
        "Vfutactptcfnomsg": "coeptura",        "Vfutactptcfvocsg": "coeptura",        "Vfutactptcfaccsg": "coepturam",
        "Vfutactptcfgensg": "coepturae",       "Vfutactptcfdatsg": "coepturae",       "Vfutactptcfablsg": "coeptura",
        "Vfutactptcfnompl": "coepturae",       "Vfutactptcfvocpl": "coepturae",       "Vfutactptcfaccpl": "coepturas",
        "Vfutactptcfgenpl": "coepturarum",     "Vfutactptcfdatpl": "coepturis",       "Vfutactptcfablpl": "coepturis",
        "Vfutactptcnnomsg": "coepturum",       "Vfutactptcnvocsg": "coepturum",       "Vfutactptcnaccsg": "coepturum",
        "Vfutactptcngensg": "coepturi",        "Vfutactptcndatsg": "coepturo",        "Vfutactptcnablsg": "coepturo",
        "Vfutactptcnnompl": "coeptura",        "Vfutactptcnvocpl": "coeptura",        "Vfutactptcnaccpl": "coeptura",
        "Vfutactptcngenpl": "coepturorum",     "Vfutactptcndatpl": "coepturis",       "Vfutactptcnablpl": "coepturis",
        "Vperpasptcmnomsg": "coeptus",         "Vperpasptcmvocsg": "coepte",          "Vperpasptcmaccsg": "coeptum",
        "Vperpasptcmgensg": "coepti",          "Vperpasptcmdatsg": "coepto",          "Vperpasptcmablsg": "coepto",
        "Vperpasptcmnompl": "coepti",          "Vperpasptcmvocpl": "coepti",          "Vperpasptcmaccpl": "coeptos",
        "Vperpasptcmgenpl": "coeptorum",       "Vperpasptcmdatpl": "coeptis",         "Vperpasptcmablpl": "coeptis",
        "Vperpasptcfnomsg": "coepta",          "Vperpasptcfvocsg": "coepta",          "Vperpasptcfaccsg": "coeptam",
        "Vperpasptcfgensg": "coeptae",         "Vperpasptcfdatsg": "coeptae",         "Vperpasptcfablsg": "coepta",
        "Vperpasptcfnompl": "coeptae",         "Vperpasptcfvocpl": "coeptae",         "Vperpasptcfaccpl": "coeptas",
        "Vperpasptcfgenpl": "coeptarum",       "Vperpasptcfdatpl": "coeptis",         "Vperpasptcfablpl": "coeptis",
        "Vperpasptcnnomsg": "coeptum",         "Vperpasptcnvocsg": "coeptum",         "Vperpasptcnaccsg": "coeptum",
        "Vperpasptcngensg": "coepti",          "Vperpasptcndatsg": "coepto",          "Vperpasptcnablsg": "coepto",
        "Vperpasptcnnompl": "coepta",          "Vperpasptcnvocpl": "coepta",          "Vperpasptcnaccpl": "coepta",
        "Vperpasptcngenpl": "coeptorum",       "Vperpasptcndatpl": "coeptis",         "Vperpasptcnablpl": "coeptis",
        "Vsupacc"         : "coeptum",         "Vsupabl"         : "coeptu",
    },
    "recoepi": {
        "Vperactindsg1"   : "recoepi",           "Vperactindsg2"   : "recoepisti",        "Vperactindsg3"   : "recoepit",
        "Vperactindpl1"   : "recoepimus",        "Vperactindpl2"   : "recoepistis",       "Vperactindpl3"   : "recoeperunt",
        "Vplpactindsg1"   : "recoeperam",        "Vplpactindsg2"   : "recoeperas",        "Vplpactindsg3"   : "recoeperat",
        "Vplpactindpl1"   : "recoeperamus",      "Vplpactindpl2"   : "recoeperatis",      "Vplpactindpl3"   : "recoeperant",
        "Vfpractindsg1"   : "recoepero",         "Vfpractindsg2"   : "recoeperis",        "Vfpractindsg3"   : "recoeperit",
        "Vfpractindpl1"   : "recoeperimus",      "Vfpractindpl2"   : "recoeperitis",      "Vfpractindpl3"   : "recoeperint",
        "Vperpasindsg1"   : "recoeptus sum",     "Vperpasindsg2"   : "recoeptus es",      "Vperpasindsg3"   : "recoeptus est",
        "Vperpasindpl1"   : "recoeptus sumus",   "Vperpasindpl2"   : "recoeptus estis",   "Vperpasindpl3"   : "recoeptus sunt",
        "Vplppasindsg1"   : "recoeptus eram",    "Vplppasindsg2"   : "recoeptus eras",    "Vplppasindsg3"   : "recoeptus erat",
        "Vplppasindpl1"   : "recoeptus eramus",  "Vplppasindpl2"   : "recoeptus eratis",  "Vplppasindpl3"   : "recoeptus erant",
        "Vfprpasindsg1"   : "recoeptus ero",     "Vfprpasindsg2"   : "recoeptus eris",    "Vfprpasindsg3"   : "recoeptus erit",
        "Vfprpasindpl1"   : "recoeptus erimus",  "Vfprpasindpl2"   : "recoeptus eritis",  "Vfprpasindpl3"   : "recoeptus erunt",
        "Vperactsbjsg1"   : "recoeperim",        "Vperactsbjsg2"   : "recoeperis",        "Vperactsbjsg3"   : "recoeperit",
        "Vperactsbjpl1"   : "recoeperimus",      "Vperactsbjpl2"   : "recoeperitis",      "Vperactsbjpl3"   : "recoeperint",
        "Vplpactsbjsg1"   : "recoepissem",       "Vplpactsbjsg2"   : "recoepisses",       "Vplpactsbjsg3"   : "recoepisset",
        "Vplpactsbjpl1"   : "recoepissemus",     "Vplpactsbjpl2"   : "recoepissetis",     "Vplpactsbjpl3"   : "recoepissent",
        "Vperpassbjsg1"   : "recoeptus sim",     "Vperpassbjsg2"   : "recoeptus sis",     "Vperpassbjsg3"   : "recoeptus sit",
        "Vperpassbjpl1"   : "recoeptus simus",   "Vperpassbjpl2"   : "recoeptus sitis",   "Vperpassbjpl3"   : "recoeptus sint",
        "Vplppassbjsg1"   : "recoeptus essem",   "Vplppassbjsg2"   : "recoeptus esses",   "Vplppassbjsg3"   : "recoeptus esset",
        "Vplppassbjpl1"   : "recoeptus essemus", "Vplppassbjpl2"   : "recoeptus essetis", "Vplppassbjpl3"   : "recoeptus essent",
        "Vfutactinf   "   : "recoepturus esse",  "Vperactinf   "   : "recoepisse",
        "Vfutpasinf   "   : "recoeptum iri",     "Vperpasinf   "   : "recoeptus esse",
        "Vfutactptcmnomsg": "recoepturus",       "Vfutactptcmvocsg": "recoepture",        "Vfutactptcmaccsg": "recoepturum",
        "Vfutactptcmgensg": "recoepturi",        "Vfutactptcmdatsg": "recoepturo",        "Vfutactptcmablsg": "recoepturo",
        "Vfutactptcmnompl": "recoepturi",        "Vfutactptcmvocpl": "recoepturi",        "Vfutactptcmaccpl": "recoepturos",
        "Vfutactptcmgenpl": "recoepturorum",     "Vfutactptcmdatpl": "recoepturis",       "Vfutactptcmablpl": "recoepturis",
        "Vfutactptcfnomsg": "recoeptura",        "Vfutactptcfvocsg": "recoeptura",        "Vfutactptcfaccsg": "recoepturam",
        "Vfutactptcfgensg": "recoepturae",       "Vfutactptcfdatsg": "recoepturae",       "Vfutactptcfablsg": "recoeptura",
        "Vfutactptcfnompl": "recoepturae",       "Vfutactptcfvocpl": "recoepturae",       "Vfutactptcfaccpl": "recoepturas",
        "Vfutactptcfgenpl": "recoepturarum",     "Vfutactptcfdatpl": "recoepturis",       "Vfutactptcfablpl": "recoepturis",
        "Vfutactptcnnomsg": "recoepturum",       "Vfutactptcnvocsg": "recoepturum",       "Vfutactptcnaccsg": "recoepturum",
        "Vfutactptcngensg": "recoepturi",        "Vfutactptcndatsg": "recoepturo",        "Vfutactptcnablsg": "recoepturo",
        "Vfutactptcnnompl": "recoeptura",        "Vfutactptcnvocpl": "recoeptura",        "Vfutactptcnaccpl": "recoeptura",
        "Vfutactptcngenpl": "recoepturorum",     "Vfutactptcndatpl": "recoepturis",       "Vfutactptcnablpl": "recoepturis",
        "Vperpasptcmnomsg": "recoeptus",         "Vperpasptcmvocsg": "recoepte",          "Vperpasptcmaccsg": "recoeptum",
        "Vperpasptcmgensg": "recoepti",          "Vperpasptcmdatsg": "recoepto",          "Vperpasptcmablsg": "recoepto",
        "Vperpasptcmnompl": "recoepti",          "Vperpasptcmvocpl": "recoepti",          "Vperpasptcmaccpl": "recoeptos",
        "Vperpasptcmgenpl": "recoeptorum",       "Vperpasptcmdatpl": "recoeptis",         "Vperpasptcmablpl": "recoeptis",
        "Vperpasptcfnomsg": "recoepta",          "Vperpasptcfvocsg": "recoepta",          "Vperpasptcfaccsg": "recoeptam",
        "Vperpasptcfgensg": "recoeptae",         "Vperpasptcfdatsg": "recoeptae",         "Vperpasptcfablsg": "recoepta",
        "Vperpasptcfnompl": "recoeptae",         "Vperpasptcfvocpl": "recoeptae",         "Vperpasptcfaccpl": "recoeptas",
        "Vperpasptcfgenpl": "recoeptarum",       "Vperpasptcfdatpl": "recoeptis",         "Vperpasptcfablpl": "recoeptis",
        "Vperpasptcnnomsg": "recoeptum",         "Vperpasptcnvocsg": "recoeptum",         "Vperpasptcnaccsg": "recoeptum",
        "Vperpasptcngensg": "recoepti",          "Vperpasptcndatsg": "recoepto",          "Vperpasptcnablsg": "recoepto",
        "Vperpasptcnnompl": "recoepta",          "Vperpasptcnvocpl": "recoepta",          "Vperpasptcnaccpl": "recoepta",
        "Vperpasptcngenpl": "recoeptorum",       "Vperpasptcndatpl": "recoeptis",         "Vperpasptcnablpl": "recoeptis",
        "Vsupacc"         : "recoeptum",         "Vsupabl"         : "recoeptu",
    },
    "commemini": {
        "Vpreactindsg1"   : "commemini",       "Vpreactindsg2"   : "commeministi",    "Vpreactindsg3"   : "commeminit",
        "Vpreactindpl1"   : "commeminimus",    "Vpreactindpl2"   : "commeministis",   "Vpreactindpl3"   : "commeminerunt",
        "Vimpactindsg1"   : "commemineram",    "Vimpactindsg2"   : "commemineras",    "Vimpactindsg3"   : "commeminerat",
        "Vimpactindpl1"   : "commemineramus",  "Vimpactindpl2"   : "commemineratis",  "Vimpactindpl3"   : "commeminerant",
        "Vfutactindsg1"   : "commeminero",     "Vfutactindsg2"   : "commemineris",    "Vfutactindsg3"   : "commeminerit",
        "Vfutactindpl1"   : "commeminerimus",  "Vfutactindpl2"   : "commemineritis",  "Vfutactindpl3"   : "commeminerint",
        "Vpreactsbjsg1"   : "commeminerim",    "Vpreactsbjsg2"   : "commemineris",    "Vpreactsbjsg3"   : "commeminerit",
        "Vpreactsbjpl1"   : "commeminerimus",  "Vpreactsbjpl2"   : "commemineritis",  "Vpreactsbjpl3"   : "commeminerint",
        "Vimpactsbjsg1"   : "commeminissem",   "Vimpactsbjsg2"   : "commeminisses",   "Vimpactsbjsg3"   : "commeminisset",
        "Vimpactsbjpl1"   : "commeminissemus", "Vimpactsbjpl2"   : "commeminissetis", "Vimpactsbjpl3"   : "commeminissent",
        "Vfutactipesg2"   : "commemento",      "Vfutactipesg3"   : "commemento",      "Vfutactipepl2"   : "commementote",
        "Vpreactinf   "   : "commeminisse",
        "Vpreactptcmnomsg": "commeminens",     "Vpreactptcmvocsg": "commeminens",     "Vpreactptcmaccsg": "commeminentem",
        "Vpreactptcmgensg": "commeminentis",   "Vpreactptcmdatsg": "commeminenti",
        "Vpreactptcmablsg": MultipleEndings(regular="commeminenti", absolute="commeminente"),
        "Vpreactptcmnompl": "commeminentes",   "Vpreactptcmvocpl": "commeminentes",   "Vpreactptcmaccpl": "commeminentes",
        "Vpreactptcmgenpl": "commeminentium",  "Vpreactptcmdatpl": "commeminentibus", "Vpreactptcmablpl": "commeminentibus",
        "Vpreactptcfnomsg": "commeminens",     "Vpreactptcfvocsg": "commeminens",     "Vpreactptcfaccsg": "commeminentem",
        "Vpreactptcfgensg": "commeminentis",   "Vpreactptcfdatsg": "commeminenti",
        "Vpreactptcfablsg": MultipleEndings(regular="commeminenti", absolute="commeminente"),
        "Vpreactptcfnompl": "commeminentes",   "Vpreactptcfvocpl": "commeminentes",   "Vpreactptcfaccpl": "commeminentes",
        "Vpreactptcfgenpl": "commeminentium",  "Vpreactptcfdatpl": "commeminentibus", "Vpreactptcfablpl": "commeminentibus",
        "Vpreactptcnnomsg": "commeminens",     "Vpreactptcnvocsg": "commeminens",     "Vpreactptcnaccsg": "commeminens",
        "Vpreactptcngensg": "commeminentis",   "Vpreactptcndatsg": "commeminenti",
        "Vpreactptcnablsg": MultipleEndings(regular="commeminenti", absolute="commeminente"),
        "Vpreactptcnnompl": "commeminentia",   "Vpreactptcnvocpl": "commeminentia",   "Vpreactptcnaccpl": "commeminentia",
        "Vpreactptcngenpl": "commeminentium",  "Vpreactptcndatpl": "commeminentibus", "Vpreactptcnablpl": "commeminentibus",
    },
    "memini": {
        "Vpreactindsg1"   : "memini",       "Vpreactindsg2"   : "meministi",    "Vpreactindsg3"   : "meminit",
        "Vpreactindpl1"   : "meminimus",    "Vpreactindpl2"   : "meministis",   "Vpreactindpl3"   : "meminerunt",
        "Vimpactindsg1"   : "memineram",    "Vimpactindsg2"   : "memineras",    "Vimpactindsg3"   : "meminerat",
        "Vimpactindpl1"   : "memineramus",  "Vimpactindpl2"   : "memineratis",  "Vimpactindpl3"   : "meminerant",
        "Vfutactindsg1"   : "meminero",     "Vfutactindsg2"   : "memineris",    "Vfutactindsg3"   : "meminerit",
        "Vfutactindpl1"   : "meminerimus",  "Vfutactindpl2"   : "memineritis",  "Vfutactindpl3"   : "meminerint",
        "Vpreactsbjsg1"   : "meminerim",    "Vpreactsbjsg2"   : "memineris",    "Vpreactsbjsg3"   : "meminerit",
        "Vpreactsbjpl1"   : "meminerimus",  "Vpreactsbjpl2"   : "memineritis",  "Vpreactsbjpl3"   : "meminerint",
        "Vimpactsbjsg1"   : "meminissem",   "Vimpactsbjsg2"   : "meminisses",   "Vimpactsbjsg3"   : "meminisset",
        "Vimpactsbjpl1"   : "meminissemus", "Vimpactsbjpl2"   : "meminissetis", "Vimpactsbjpl3"   : "meminissent",
        "Vfutactipesg2"   : "memento",      "Vfutactipesg3"   : "memento",      "Vfutactipepl2"   : "mementote",
        "Vpreactinf   "   : "meminisse",
        "Vpreactptcmnomsg": "meminens",     "Vpreactptcmvocsg": "meminens",     "Vpreactptcmaccsg": "meminentem",
        "Vpreactptcmgensg": "meminentis",   "Vpreactptcmdatsg": "meminenti",
        "Vpreactptcmablsg": MultipleEndings(regular="meminenti", absolute="meminente"),
        "Vpreactptcmnompl": "meminentes",   "Vpreactptcmvocpl": "meminentes",   "Vpreactptcmaccpl": "meminentes",
        "Vpreactptcmgenpl": "meminentium",  "Vpreactptcmdatpl": "meminentibus", "Vpreactptcmablpl": "meminentibus",
        "Vpreactptcfnomsg": "meminens",     "Vpreactptcfvocsg": "meminens",     "Vpreactptcfaccsg": "meminentem",
        "Vpreactptcfgensg": "meminentis",   "Vpreactptcfdatsg": "meminenti",
        "Vpreactptcfablsg": MultipleEndings(regular="meminenti", absolute="meminente"),
        "Vpreactptcfnompl": "meminentes",   "Vpreactptcfvocpl": "meminentes",   "Vpreactptcfaccpl": "meminentes",
        "Vpreactptcfgenpl": "meminentium",  "Vpreactptcfdatpl": "meminentibus", "Vpreactptcfablpl": "meminentibus",
        "Vpreactptcnnomsg": "meminens",     "Vpreactptcnvocsg": "meminens",     "Vpreactptcnaccsg": "meminens",
        "Vpreactptcngensg": "meminentis",   "Vpreactptcndatsg": "meminenti",
        "Vpreactptcnablsg": MultipleEndings(regular="meminenti", absolute="meminente"),
        "Vpreactptcnnompl": "meminentia",   "Vpreactptcnvocpl": "meminentia",   "Vpreactptcnaccpl": "meminentia",
        "Vpreactptcngenpl": "meminentium",  "Vpreactptcndatpl": "meminentibus", "Vpreactptcnablpl": "meminentibus",
    },
    "rememini": {
        "Vpreactindsg1"   : "rememini",       "Vpreactindsg2"   : "remeministi",    "Vpreactindsg3"   : "rememinit",
        "Vpreactindpl1"   : "rememinimus",    "Vpreactindpl2"   : "remeministis",   "Vpreactindpl3"   : "rememinerunt",
        "Vimpactindsg1"   : "rememineram",    "Vimpactindsg2"   : "rememineras",    "Vimpactindsg3"   : "rememinerat",
        "Vimpactindpl1"   : "rememineramus",  "Vimpactindpl2"   : "rememineratis",  "Vimpactindpl3"   : "rememinerant",
        "Vfutactindsg1"   : "rememinero",     "Vfutactindsg2"   : "rememineris",    "Vfutactindsg3"   : "rememinerit",
        "Vfutactindpl1"   : "rememinerimus",  "Vfutactindpl2"   : "rememineritis",  "Vfutactindpl3"   : "rememinerint",
        "Vpreactsbjsg1"   : "rememinerim",    "Vpreactsbjsg2"   : "rememineris",    "Vpreactsbjsg3"   : "rememinerit",
        "Vpreactsbjpl1"   : "rememinerimus",  "Vpreactsbjpl2"   : "rememineritis",  "Vpreactsbjpl3"   : "rememinerint",
        "Vimpactsbjsg1"   : "rememinissem",   "Vimpactsbjsg2"   : "rememinisses",   "Vimpactsbjsg3"   : "rememinisset",
        "Vimpactsbjpl1"   : "rememinissemus", "Vimpactsbjpl2"   : "rememinissetis", "Vimpactsbjpl3"   : "rememinissent",
        "Vfutactipesg2"   : "rememento",      "Vfutactipesg3"   : "rememento",      "Vfutactipepl2"   : "remementote",
        "Vpreactinf   "   : "rememinisse",
        "Vpreactptcmnomsg": "rememinens",     "Vpreactptcmvocsg": "rememinens",     "Vpreactptcmaccsg": "rememinentem",
        "Vpreactptcmgensg": "rememinentis",   "Vpreactptcmdatsg": "rememinenti",
        "Vpreactptcmablsg": MultipleEndings(regular="rememinenti", absolute="rememinente"),
        "Vpreactptcmnompl": "rememinentes",   "Vpreactptcmvocpl": "rememinentes",   "Vpreactptcmaccpl": "rememinentes",
        "Vpreactptcmgenpl": "rememinentium",  "Vpreactptcmdatpl": "rememinentibus", "Vpreactptcmablpl": "rememinentibus",
        "Vpreactptcfnomsg": "rememinens",     "Vpreactptcfvocsg": "rememinens",     "Vpreactptcfaccsg": "rememinentem",
        "Vpreactptcfgensg": "rememinentis",   "Vpreactptcfdatsg": "rememinenti",
        "Vpreactptcfablsg": MultipleEndings(regular="rememinenti", absolute="rememinente"),
        "Vpreactptcfnompl": "rememinentes",   "Vpreactptcfvocpl": "rememinentes",   "Vpreactptcfaccpl": "rememinentes",
        "Vpreactptcfgenpl": "rememinentium",  "Vpreactptcfdatpl": "rememinentibus", "Vpreactptcfablpl": "rememinentibus",
        "Vpreactptcnnomsg": "rememinens",     "Vpreactptcnvocsg": "rememinens",     "Vpreactptcnaccsg": "rememinens",
        "Vpreactptcngensg": "rememinentis",   "Vpreactptcndatsg": "rememinenti",
        "Vpreactptcnablsg": MultipleEndings(regular="rememinenti", absolute="rememinente"),
        "Vpreactptcnnompl": "rememinentia",   "Vpreactptcnvocpl": "rememinentia",   "Vpreactptcnaccpl": "rememinentia",
        "Vpreactptcngenpl": "rememinentium",  "Vpreactptcndatpl": "rememinentibus", "Vpreactptcnablpl": "rememinentibus",
    },
    "odi": {
        "Vpreactindsg1"   : "odi",          "Vpreactindsg2"   : "odisti",       "Vpreactindsg3"   : "odit",
        "Vpreactindpl1"   : "odimus",       "Vpreactindpl2"   : "odistis",      "Vpreactindpl3"   : "oderunt",
        "Vimpactindsg1"   : "oderam",       "Vimpactindsg2"   : "oderas",       "Vimpactindsg3"   : "oderat",
        "Vimpactindpl1"   : "oderamus",     "Vimpactindpl2"   : "oderatis",     "Vimpactindpl3"   : "oderant",
        "Vfutactindsg1"   : "odero",        "Vfutactindsg2"   : "oderis",       "Vfutactindsg3"   : "oderit",
        "Vfutactindpl1"   : "oderimus",     "Vfutactindpl2"   : "oderitis",     "Vfutactindpl3"   : "oderint",
        "Vperactindsg1"   : "osus sum",     "Vperactindsg2"   : "osus es",      "Vperactindsg3"   : "osus est",
        "Vperactindpl1"   : "osus sumus",   "Vperactindpl2"   : "osus estis",   "Vperactindpl3"   : "osus sunt",
        "Vplpactindsg1"   : "osus eram",    "Vplpactindsg2"   : "osus eras",    "Vplpactindsg3"   : "osus erat",
        "Vplpactindpl1"   : "osus eramus",  "Vplpactindpl2"   : "osus eratis",  "Vplpactindpl3"   : "osus erant",
        "Vfpractindsg1"   : "osus ero",     "Vfpractindsg2"   : "osus eris",    "Vfpractindsg3"   : "osus erit",
        "Vfpractindpl1"   : "osus erimus",  "Vfpractindpl2"   : "osus eritis",  "Vfpractindpl3"   : "osus erunt",
        "Vprepasindsg1"   : "oderim",       "Vprepasindsg2"   : "oderis",       "Vprepasindsg3"   : "oderit",
        "Vprepasindpl1"   : "oderimus",     "Vprepasindpl2"   : "oderitis",     "Vprepasindpl3"   : "oderint",
        "Vimppasindsg1"   : "odissem",      "Vimppasindsg2"   : "odisses",      "Vimppasindsg3"   : "odisset",
        "Vimppasindpl1"   : "odissemus",    "Vimppasindpl2"   : "odissetis",    "Vimppasindpl3"   : "odissent",
        "Vperpasindsg1"   : "osus sim",     "Vperpasindsg2"   : "osus sis",     "Vperpasindsg3"   : "osus sit",
        "Vperpasindpl1"   : "osus simus",   "Vperpasindpl2"   : "osus sitis",   "Vperpasindpl3"   : "osus sint",
        "Vplppasindsg1"   : "osus essem",   "Vplppasindsg2"   : "osus esses",   "Vplppasindsg3"   : "osus esset",
        "Vplppasindpl1"   : "osus essemus", "Vplppasindpl2"   : "osus essetis", "Vplppasindpl3"   : "osus essent",
        "Vpreactinf   "   : "odisse",       "Vfutactinf   "   : "osurus esse",  "Vperactinf   "   : "osus esse",
        "Vfutactptcmnomsg": "osurus",       "Vfutactptcmvocsg": "osure",        "Vfutactptcmaccsg": "osurum",
        "Vfutactptcmgensg": "osuri",        "Vfutactptcmdatsg": "osuro",        "Vfutactptcmablsg": "osuro",
        "Vfutactptcmnompl": "osuri",        "Vfutactptcmvocpl": "osuri",        "Vfutactptcmaccpl": "osuros",
        "Vfutactptcmgenpl": "osurorum",     "Vfutactptcmdatpl": "osuris",       "Vfutactptcmablpl": "osuris",
        "Vfutactptcfnomsg": "osura",        "Vfutactptcfvocsg": "osura",        "Vfutactptcfaccsg": "osuram",
        "Vfutactptcfgensg": "osurae",       "Vfutactptcfdatsg": "osurae",       "Vfutactptcfablsg": "osura",
        "Vfutactptcfnompl": "osurae",       "Vfutactptcfvocpl": "osurae",       "Vfutactptcfaccpl": "osuras",
        "Vfutactptcfgenpl": "osurarum",     "Vfutactptcfdatpl": "osuris",       "Vfutactptcfablpl": "osuris",
        "Vfutactptcnnomsg": "osurum",       "Vfutactptcnvocsg": "osurum",       "Vfutactptcnaccsg": "osurum",
        "Vfutactptcngensg": "osuri",        "Vfutactptcndatsg": "osuro",        "Vfutactptcnablsg": "osuro",
        "Vfutactptcnnompl": "osura",        "Vfutactptcnvocpl": "osura",        "Vfutactptcnaccpl": "osura",
        "Vfutactptcngenpl": "osurorum",     "Vfutactptcndatpl": "osuris",       "Vfutactptcnablpl": "osuris",
        "Vperpasptcmnomsg": "osus",         "Vperpasptcmvocsg": "ose",          "Vperpasptcmaccsg": "osum",
        "Vperpasptcmgensg": "osi",          "Vperpasptcmdatsg": "oso",          "Vperpasptcmablsg": "oso",
        "Vperpasptcmnompl": "osi",          "Vperpasptcmvocpl": "osi",          "Vperpasptcmaccpl": "osos",
        "Vperpasptcmgenpl": "osorum",       "Vperpasptcmdatpl": "osis",         "Vperpasptcmablpl": "osis",
        "Vperpasptcfnomsg": "osa",          "Vperpasptcfvocsg": "osa",          "Vperpasptcfaccsg": "osam",
        "Vperpasptcfgensg": "osae",         "Vperpasptcfdatsg": "osae",         "Vperpasptcfablsg": "osa",
        "Vperpasptcfnompl": "osae",         "Vperpasptcfvocpl": "osae",         "Vperpasptcfaccpl": "osas",
        "Vperpasptcfgenpl": "osarum",       "Vperpasptcfdatpl": "osis",         "Vperpasptcfablpl": "osis",
        "Vperpasptcnnomsg": "osum",         "Vperpasptcnvocsg": "osum",         "Vperpasptcnaccsg": "osum",
        "Vperpasptcngensg": "osi",          "Vperpasptcndatsg": "oso",          "Vperpasptcnablsg": "oso",
        "Vperpasptcnnompl": "osa",          "Vperpasptcnvocpl": "osa",          "Vperpasptcnaccpl": "osa",
        "Vperpasptcngenpl": "osorum",       "Vperpasptcndatpl": "osis",         "Vperpasptcnablpl": "osis",
        "Vsupacc"         : "osum",         "Vsupabl"         : "osu",
    },
}  # fmt: skip


# -----------------------------------------------------------------------------
# IRREGULAR VERBS

type _IrregularVerb = Literal[
    "sum", "possum", "volo", "nolo", "malo", "fero", "eo", "facio"
]

IRREGULAR_VERB_CONJUGATION: Final[dict[_IrregularVerb, Conjugation]] = {
    "sum": 3,
    "possum": 3,
    "volo": 3,
    "nolo": 3,
    "malo": 3,
    "fero": 3,
    "eo": 4,  # no idea if this really matters?
    "facio": 5,
}

IRREGULAR_VERB_STEMS: Final[dict[_IrregularVerb, tuple[str, str]]] = {
    # (_inf_stem, _preptc_stem), unused or impossible stems are not provided
    "sum": ("", ""),
    "possum": ("", "pote"),
    "volo": ("vol", "vole"),
    "nolo": ("nol", "nole"),
    "malo": ("mal", "male"),
    "fero": ("fer", "fere"),
    "eo": ("", "ie"),  # fourth conjugation-like?
    "facio": ("fac", "facie"),
}

IRREGULAR_VERB_CHANGES: Final[dict[_IrregularVerb, DictChanges[Ending]]] = {
    "sum": DictChanges(  # sum, esse, fui, futurus
        # perfective indicative and subjunctive, imperfect subjunctive are regular
        replacements={
            "Vpreactindsg2": "es",     "Vpreactindsg3": "est",
            "Vpreactindpl1": "sumus",  "Vpreactindpl2": "estis",  "Vpreactindpl3": "sunt",
            "Vimpactindsg1": "eram",   "Vimpactindsg2": "eras",   "Vimpactindsg3": "erat",
            "Vimpactindpl1": "eramus", "Vimpactindpl2": "eratis", "Vimpactindpl3": "erant",
            "Vfutactindsg1": "ero",    "Vfutactindsg2": "eris",   "Vfutactindsg3": "erit",
            "Vfutactindpl1": "erimus", "Vfutactindpl2": "eritis", "Vfutactindpl3": "erunt",
            "Vpreactsbjsg1": "sim",    "Vpreactsbjsg2": "sis",    "Vpreactsbjsg3": "sit",
            "Vpreactsbjpl1": "simus",  "Vpreactsbjpl2": "sitis",  "Vpreactsbjpl3": "sint",
            "Vpreactipesg2": "es",     "Vpreactipepl2": "este",
            "Vfutactipesg2": "esto",   "Vfutactipesg3": "esto",
            "Vfutactipepl2": "estote", "Vfutactipepl3": "sunto",
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
            "Vpreactindsg2": "potes",     "Vpreactindsg3": "potest",
            "Vpreactindpl1": "possumus",  "Vpreactindpl2": "potestis",  "Vpreactindpl3": "possunt",
            "Vimpactindsg1": "poteram",   "Vimpactindsg2": "poteras",   "Vimpactindsg3": "poterat",
            "Vimpactindpl1": "poteramus", "Vimpactindpl2": "poteratis", "Vimpactindpl3": "poterant",
            "Vfutactindsg1": "potero",    "Vfutactindsg2": "poteris",   "Vfutactindsg3": "poterit",
            "Vfutactindpl1": "poterimus", "Vfutactindpl2": "poteritis", "Vfutactindpl3": "poterunt",
            "Vpreactsbjsg1": "possim",    "Vpreactsbjsg2": "possis",    "Vpreactsbjsg3": "possit",
            "Vpreactsbjpl1": "possimus",  "Vpreactsbjpl2": "possitis",  "Vpreactsbjpl3": "possint",
        },
        additions={},
        # no imperatives, passives
        deletions={re.compile(r"^.{4}pas.*$"), re.compile(r"^.{7}ipe.*$")},
    ),
    "volo": DictChanges(  # volo, velle, volui, voliturus
        # only present indicative and subjunctive are irregular
        replacements={
            "Vpreactindsg2": "vis",     "Vpreactindsg3": "vult",
            "Vpreactindpl1": "volumus", "Vpreactindpl2": "vultis",  "Vpreactindpl3": "volunt",
            "Vpreactsbjsg1": "velim",   "Vpreactsbjsg2": "velis",   "Vpreactsbjsg3": "velit",
            "Vpreactsbjpl1": "velimus", "Vpreactsbjpl2": "velitis", "Vpreactsbjpl3": "velint",
        },
        additions={},
        # no imperatives, passives
        deletions={re.compile(r"^.{4}pas.*$"), re.compile(r"^.{7}ipe.*$")},
    ),
    "nolo": DictChanges(  # nolo, nolle, nolui
        # only present indicative and subjunctive, and imperative are irregular
        replacements={
            "Vpreactindsg2": "non vis", "Vpreactindsg3": "non vult",
            "Vpreactindpl1": "nolumus", "Vpreactindpl2": "non vultis", "Vpreactindpl3": "nolunt",
            "Vpreactsbjsg1": "nelim",   "Vpreactsbjsg2": "nelis",      "Vpreactsbjsg3": "nelit",
            "Vpreactsbjpl1": "nelimus", "Vpreactsbjpl2": "nelitis",    "Vpreactsbjpl3": "nelint",
            "Vpreactipesg2": "noli",    "Vpreactipepl2": "nolite",
        },
        additions={},
        # no passives
        deletions={re.compile(r"^.{4}pas.*$")},
    ),
    "malo": DictChanges(  # malo, malle, malui
        # only present indicative and subjunctive are irregular
        replacements={
            "Vpreactindsg2": "mavis",   "Vpreactindsg3": "mavult",
            "Vpreactindpl1": "malumus", "Vpreactindpl2": "mavultis", "Vpreactindpl3": "malunt",
            "Vpreactsbjsg1": "malim",   "Vpreactsbjsg2": "malis",    "Vpreactsbjsg3": "malit",
            "Vpreactsbjpl1": "malimus", "Vpreactsbjpl2": "malitis",  "Vpreactsbjpl3": "malint",
        },
        additions={},
        # no passives, imperatives
        deletions={re.compile(r"^.{4}pas.*$"), re.compile(r"^.{7}ipe.*$")},
    ),
    "fero": DictChanges(  # fero, ferre, tuli, latus
        # some forms are irregular
        replacements={
            "Vpreactindsg2": "fers",     "Vpreactindsg3": "fert",
            "Vpreactindpl2": "fertis",
            "Vprepasindsg2": "ferris",   "Vprepasindsg3": "fertur",
            "Vpreactipesg2": "fer",      "Vpreactipepl2": "ferte",
            "Vprepasipesg2": "ferre",    "Vprepasipepl2": "ferimini",
            "Vfutactipesg2": "ferto",    "Vfutactipesg3": "ferto",
            "Vfutactipepl2": "fertote",  "Vfutactipepl3": "ferunto",
            "Vfutpasipesg2": "fertor",   "Vfutpasipesg3": "fertor",
            "Vfutpasipepl3": "feruntor",
            "Vprepasinf   ": "ferri",
        },
        additions={},
        deletions=set(),
    ),
    "eo": DictChanges(  # eo, ire, ii, itus
        # various forms are regular throughout
        replacements={
            "Vpreactindpl3"   : "eunt",
            "Vimpactindsg1"   : "ibam",     "Vimpactindsg2"   : "ibas",     "Vimpactindsg3"   : "ibat",
            "Vimpactindpl1"   : "ibamus",   "Vimpactindpl2"   : "ibatis",   "Vimpactindpl3"   : "ibant",
            "Vfutactindsg1"   : "ibo",      "Vfutactindsg2"   : "ibis",     "Vfutactindsg3"   : "ibit",
            "Vfutactindpl1"   : "ibimus",   "Vfutactindpl2"   : "ibitis",   "Vfutactindpl3"   : "ibunt",
            "Vperactindsg2"   : "isti",
            "Vperactindpl2"   : "istis",
            "Vprepasindsg1"   : "eor",
            "Vprepasindpl3"   : "euntur",
            "Vimppasindsg1"   : "ibar",     "Vimppasindsg2"   : "ibaris",   "Vimppasindsg3"   : "ibatur",
            "Vimppasindpl1"   : "ibamur",   "Vimppasindpl2"   : "ibamini",  "Vimppasindpl3"   : "ibantur",
            "Vfutpasindsg1"   : "ibor",     "Vfutpasindsg2"   : "iberis",   "Vfutpasindsg3"   : "ibitur",
            "Vfutpasindpl1"   : "ibimur",   "Vfutpasindpl2"   : "ibimini",  "Vfutpasindpl3"   : "ibuntur",
            "Vpreactsbjsg1"   : "eam",      "Vpreactsbjsg2"   : "eas",      "Vpreactsbjsg3"   : "eat",
            "Vpreactsbjpl1"   : "eamus",    "Vpreactsbjpl2"   : "eatis",    "Vpreactsbjpl3"   : "eant",
            "Vplpactsbjsg1"   : "issem",    "Vplpactsbjsg2"   : "isses",    "Vplpactsbjsg3"   : "isset",
            "Vplpactsbjpl1"   : "issemus",  "Vplpactsbjpl2"   : "issetis",  "Vplpactsbjpl3"   : "issent",
            "Vprepassbjsg1"   : "ear",      "Vprepassbjsg2"   : "earis",    "Vprepassbjsg3"   : "eatur",
            "Vprepassbjpl1"   : "eamur",    "Vprepassbjpl2"   : "eamini",   "Vprepassbjpl3"   : "eantur",
            "Vfutactipepl3"   : "eunto",
            "Vfutpasipepl3"   : "euntor",
            "Vperactinf   "   : "isse",
            "Vpreactptcmaccsg": "euntem",   "Vpreactptcmgensg": "euntis",   "Vpreactptcmdatsg": "eunti",
            "Vpreactptcmablsg": MultipleEndings(regular="eunti", absolute="eunte"),
            "Vpreactptcmnompl": "euntes",   "Vpreactptcmvocpl": "euntes",   "Vpreactptcmaccpl": "euntes",
            "Vpreactptcmgenpl": "euntium",  "Vpreactptcmdatpl": "euntibus", "Vpreactptcmablpl": "euntibus",
            "Vpreactptcfaccsg": "euntem",   "Vpreactptcfgensg": "euntis",   "Vpreactptcfdatsg": "eunti",
            "Vpreactptcfablsg": MultipleEndings(regular="eunti", absolute="eunte"),
            "Vpreactptcfnompl": "euntes",   "Vpreactptcfvocpl": "euntes",   "Vpreactptcfaccpl": "euntes",
            "Vpreactptcfgenpl": "euntium",  "Vpreactptcfdatpl": "euntibus", "Vpreactptcfablpl": "euntibus",
            "Vpreactptcngensg": "euntis",   "Vpreactptcndatsg": "eunti",
            "Vpreactptcnablsg": MultipleEndings(regular="eunti", absolute="eunte"),
            "Vpreactptcnnompl": "euntia",   "Vpreactptcnvocpl": "euntia",   "Vpreactptcnaccpl": "euntia",
            "Vpreactptcngenpl": "euntium",  "Vpreactptcndatpl": "euntibus", "Vpreactptcnablpl": "euntibus",
            "Vfutpasptcmnomsg": "eundus",   "Vfutpasptcmvocsg": "eunde",    "Vfutpasptcmaccsg": "eundum",
            "Vfutpasptcmgensg": "eundi",    "Vfutpasptcmdatsg": "eundo",    "Vfutpasptcmablsg": "eundo",
            "Vfutpasptcmnompl": "eundi",    "Vfutpasptcmvocpl": "eundi",    "Vfutpasptcmaccpl": "eundos",
            "Vfutpasptcmgenpl": "eundorum", "Vfutpasptcmdatpl": "eundis",   "Vfutpasptcmablpl": "eundis",
            "Vfutpasptcfnomsg": "eunda",    "Vfutpasptcfvocsg": "eunda",    "Vfutpasptcfaccsg": "eundam",
            "Vfutpasptcfgensg": "eundae",   "Vfutpasptcfdatsg": "eundae",   "Vfutpasptcfablsg": "eunda",
            "Vfutpasptcfnompl": "eundae",   "Vfutpasptcfvocpl": "eundae",   "Vfutpasptcfaccpl": "eundas",
            "Vfutpasptcfgenpl": "eundarum", "Vfutpasptcfdatpl": "eundis",   "Vfutpasptcfablpl": "eundis",
            "Vfutpasptcnnomsg": "eundum",   "Vfutpasptcnvocsg": "eundum",   "Vfutpasptcnaccsg": "eundum",
            "Vfutpasptcngensg": "eundi",    "Vfutpasptcndatsg": "eundo",    "Vfutpasptcnablsg": "eundo",
            "Vfutpasptcnnompl": "eunda",    "Vfutpasptcnvocpl": "eunda",    "Vfutpasptcnaccpl": "eunda",
            "Vfutpasptcngenpl": "eundorum", "Vfutpasptcndatpl": "eundis",   "Vfutpasptcnablpl": "eundis",
            "Vgeracc"         : "eundum",   "Vgergen"         : "eundi",    "Vgerdat"         : "eundo",    "Vgerabl": "eundo",
        },
        additions={},
        deletions=set(),
    ),
    "facio": DictChanges( # facio, facere, feci, factus
        # suppletive with 'fieri'
        replacements={
            "Vprepasindsg1": "fio",      "Vprepasindsg2": "fis",      "Vprepasindsg3": "fit",
            "Vprepasindpl1": "fimus",    "Vprepasindpl2": "fitis",    "Vprepasindpl3": "fiunt",
            "Vimppasindsg1": "fiebam",   "Vimppasindsg2": "fiebas",   "Vimppasindsg3": "fiebat",
            "Vimppasindpl1": "fiebamus", "Vimppasindpl2": "fiebatis", "Vimppasindpl3": "fiebant",
            "Vfutpasindsg1": "fiam",     "Vfutpasindsg2": "fies",     "Vfutpasindsg3": "fiet",
            "Vfutpasindpl1": "fiemus",   "Vfutpasindpl2": "fietis",   "Vfutpasindpl3": "fient",
            "Vprepassbjsg1": "fiam",     "Vprepassbjsg2": "fias",     "Vprepassbjsg3": "fiat",
            "Vprepassbjpl1": "fiamus",   "Vprepassbjpl2": "fiatis",   "Vprepassbjpl3": "fiant",
            "Vimppassbjsg1": "fierem",   "Vimppassbjsg2": "fieres",   "Vimppassbjsg3": "fieret",
            "Vimppassbjpl1": "fieremus", "Vimppassbjpl2": "fieretis", "Vimppassbjpl3": "fierent",
            "Vpreactipesg2": MultipleEndings(regular="fac", second="face"),
            "Vprepasipesg2": "fi",       "Vprepasipepl2": "fite",
            "Vfutpasipesg2": "fito",     "Vfutpasipesg3": "fito",
            "Vfutpasipepl2": "fitote",   "Vfutpasipepl3": "fiunto",
            "Vprepasinf   ": "fieri",
        },
        additions={},
        deletions=set(),
    ),
}  # fmt: skip


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
    "sum", "sum_preptc", "fero", "eo", "eo_impersonal_passive", "facio"
]

DERIVED_IRREGULAR_VERB_CONJUGATION: Final[
    dict[_DerivedVerbGroups, Conjugation]
] = {
    "sum": 3,
    "sum_preptc": 3,
    "fero": 3,
    "eo": 4,
    "eo_impersonal_passive": 4,
    "facio": 5,
}


DERIVED_IRREGULAR_VERB_STEMS: Final[
    dict[_DerivedVerbGroups, tuple[str, str]]
] = {
    # (_inf_stem, _preptc_stem), unused or impossible stems are not provided
    "sum": ("", ""),
    "sum_preptc": ("", "se"),
    "fero": ("fer", "fere"),
    "eo": ("", "i"),
    "eo_impersonal_passive": ("", "i"),
    "facio": ("fac", "face"),
}

DERIVED_IRREGULAR_VERBS: Final[dict[_DerivedVerbGroups, set[_DerivedVerb]]] = {
    "sum": {
        "adsum", "obsum", "desum", "insum", "intersum", "prosum", "subsum", "supersum",
    },
    "sum_preptc": {"absum", "praesum"},
    "fero": {
        "affero", "aufero", "circumfero", "confero", "defero", "differo", "effero", "infero", "interfero", "introfero", "offero",
        "perfero", "postfero", "praefero", "profero", "refero", "suffero", "transfero",
    },
    "eo": {
        "adeo", "ambeo", "circumeo", "coeo", "deeo", "dispereo", "exeo", "ineo", "intereo", "introeo", "nequeo", "obeo",
        "praetereo", "prodeo", "queo", "subeo", "transabeo", "transeo", "veneo",
    },
    "eo_impersonal_passive": {"abeo", "pereo", "redeo"},
    "facio": {
        "arefacio", "benefacio", "calefacio", "commonefacio", "disfacio", "liquefacio", "malefacio", "mollifacio", "olfacio",
        "patefacio", "satisfacio", "stupefacio", "tepefacio",
    },
}  # fmt: skip

DERIVED_IRREGULAR_CHANGES: Final[
    dict[_DerivedVerbGroups, Callable[[tuple[str, ...]], DictChanges[Ending]]]
] = {
    "sum": lambda x: DictChanges(  # e.g. adsum, adesse, adfui, adfuturus
        # perfective indicative and subjunctive, imperfect subjunctive are regular
        replacements={
            "Vpreactindsg2": f"{x[0]}es",     "Vpreactindsg3": f"{x[0]}est",
            "Vpreactindpl1": f"{x[0]}sumus",  "Vpreactindpl2": f"{x[0]}estis",  "Vpreactindpl3": f"{x[0]}sunt",
            "Vimpactindsg1": f"{x[0]}eram",   "Vimpactindsg2": f"{x[0]}eras",   "Vimpactindsg3": f"{x[0]}erat",
            "Vimpactindpl1": f"{x[0]}eramus", "Vimpactindpl2": f"{x[0]}eratis", "Vimpactindpl3": f"{x[0]}erant",
            "Vfutactindsg1": f"{x[0]}ero",    "Vfutactindsg2": f"{x[0]}eris",   "Vfutactindsg3": f"{x[0]}erit",
            "Vfutactindpl1": f"{x[0]}erimus", "Vfutactindpl2": f"{x[0]}eritis", "Vfutactindpl3": f"{x[0]}erunt",
            "Vpreactsbjsg1": f"{x[0]}sim",    "Vpreactsbjsg2": f"{x[0]}sis",    "Vpreactsbjsg3": f"{x[0]}sit",
            "Vpreactsbjpl1": f"{x[0]}simus",  "Vpreactsbjpl2": f"{x[0]}sitis",  "Vpreactsbjpl3": f"{x[0]}sint",
            "Vpreactipesg2": f"{x[0]}es",     "Vpreactipepl2": f"{x[0]}este",
            "Vfutactipesg2": f"{x[0]}esto",   "Vfutactipesg3": f"{x[0]}esto",
            "Vfutactipepl2": f"{x[0]}estote", "Vfutactipepl3": f"{x[0]}sunto",
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
            "Vpreactindsg2": f"{x[0]}es",     "Vpreactindsg3": f"{x[0]}est",
            "Vpreactindpl1": f"{x[0]}sumus",  "Vpreactindpl2": f"{x[0]}estis",  "Vpreactindpl3": f"{x[0]}sunt",
            "Vimpactindsg1": f"{x[0]}eram",   "Vimpactindsg2": f"{x[0]}eras",   "Vimpactindsg3": f"{x[0]}erat",
            "Vimpactindpl1": f"{x[0]}eramus", "Vimpactindpl2": f"{x[0]}eratis", "Vimpactindpl3": f"{x[0]}erant",
            "Vfutactindsg1": f"{x[0]}ero",    "Vfutactindsg2": f"{x[0]}eris",   "Vfutactindsg3": f"{x[0]}erit",
            "Vfutactindpl1": f"{x[0]}erimus", "Vfutactindpl2": f"{x[0]}eritis", "Vfutactindpl3": f"{x[0]}erunt",
            "Vpreactsbjsg1": f"{x[0]}sim",    "Vpreactsbjsg2": f"{x[0]}sis",    "Vpreactsbjsg3": f"{x[0]}sit",
            "Vpreactsbjpl1": f"{x[0]}simus",  "Vpreactsbjpl2": f"{x[0]}sitis",  "Vpreactsbjpl3": f"{x[0]}sint",
            "Vpreactipesg2": f"{x[0]}es",     "Vpreactipepl2": f"{x[0]}este",
            "Vfutactipesg2": f"{x[0]}esto",   "Vfutactipesg3": f"{x[0]}esto",
            "Vfutactipepl2": f"{x[0]}estote", "Vfutactipepl3": f"{x[0]}sunto",
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
            "Vpreactindsg2": f"{x[0]}fers",     "Vpreactindsg3": f"{x[0]}fert",
            "Vpreactindpl2": f"{x[0]}fertis",
            "Vprepasindsg2": f"{x[0]}ferris",   "Vprepasindsg3": f"{x[0]}fertur",
            "Vpreactipesg2": f"{x[0]}fer",      "Vpreactipepl2": f"{x[0]}ferte",
            "Vprepasipesg2": f"{x[0]}ferre",    "Vprepasipepl2": f"{x[0]}ferimini",
            "Vfutactipesg2": f"{x[0]}ferto",    "Vfutactipesg3": f"{x[0]}ferto",
            "Vfutactipepl2": f"{x[0]}fertote",  "Vfutactipepl3": f"{x[0]}ferunto",
            "Vfutpasipesg2": f"{x[0]}fertor",   "Vfutpasipesg3": f"{x[0]}fertor",
            "Vfutpasipepl3": f"{x[0]}feruntor",
            "Vprepasinf   ": f"{x[0]}ferri",
        },
        additions={},
        deletions=set(),
    ),
    "eo": lambda x: DictChanges(  # e.g. adeo, adire, adii, aditus
        # various forms are regular throughout
        replacements={
            "Vpreactindpl3"   : f"{x[0]}eunt",
            "Vimpactindsg1"   : f"{x[0]}ibam",    "Vimpactindsg2"   : f"{x[0]}ibas",     "Vimpactindsg3"   : f"{x[0]}ibat",
            "Vimpactindpl1"   : f"{x[0]}ibamus",  "Vimpactindpl2"   : f"{x[0]}ibatis",   "Vimpactindpl3"   : f"{x[0]}ibant",
            "Vfutactindsg1"   : f"{x[0]}ibo",     "Vfutactindsg2"   : f"{x[0]}ibis",     "Vfutactindsg3"   : f"{x[0]}ibit",
            "Vfutactindpl1"   : f"{x[0]}ibimus",  "Vfutactindpl2"   : f"{x[0]}ibitis",   "Vfutactindpl3"   : f"{x[0]}ibunt",
            "Vperactindsg2"   : f"{x[2]}isti",    "Vperactindpl2"   : f"{x[2]}istis",
            "Vprepasindsg1"   : f"{x[0]}eor",     "Vprepasindpl3"   : f"{x[0]}euntur",
            "Vimppasindsg1"   : f"{x[0]}ibar",    "Vimppasindsg2"   : f"{x[0]}ibaris",   "Vimppasindsg3"   : f"{x[0]}ibatur",
            "Vimppasindpl1"   : f"{x[0]}ibamur",  "Vimppasindpl2"   : f"{x[0]}ibamini",  "Vimppasindpl3"   : f"{x[0]}ibantur",
            "Vfutpasindsg1"   : f"{x[0]}ibor",    "Vfutpasindsg2"   : f"{x[0]}iberis",   "Vfutpasindsg3"   : f"{x[0]}ibitur",
            "Vfutpasindpl1"   : f"{x[0]}ibimur",  "Vfutpasindpl2"   : f"{x[0]}ibimini",  "Vfutpasindpl3"   : f"{x[0]}ibuntur",
            "Vpreactsbjsg1"   : f"{x[0]}eam",     "Vpreactsbjsg2"   : f"{x[0]}eas",      "Vpreactsbjsg3"   : f"{x[0]}eat",
            "Vpreactsbjpl1"   : f"{x[0]}eamus",   "Vpreactsbjpl2"   : f"{x[0]}eatis",    "Vpreactsbjpl3"   : f"{x[0]}eant",
            "Vplpactsbjsg1"   : f"{x[2]}issem",   "Vplpactsbjsg2"   : f"{x[2]}isses",    "Vplpactsbjsg3"   : f"{x[2]}isset",
            "Vplpactsbjpl1"   : f"{x[2]}issemus", "Vplpactsbjpl2"   : f"{x[2]}issetis",  "Vplpactsbjpl3"   : f"{x[2]}issent",
            "Vprepassbjsg1"   : f"{x[0]}ear",     "Vprepassbjsg2"   : f"{x[0]}earis",    "Vprepassbjsg3"   : f"{x[0]}eatur",
            "Vprepassbjpl1"   : f"{x[0]}eamur",   "Vprepassbjpl2"   : f"{x[0]}eamini",   "Vprepassbjpl3"   : f"{x[0]}eantur",
            "Vfutactipepl3"   : f"{x[0]}eunto",   "Vfutpasipepl3"   : f"{x[0]}euntor",
            "Vperactinf   "   : f"{x[2]}isse",
            "Vpreactptcmaccsg": f"{x[0]}euntem",  "Vpreactptcmgensg": f"{x[0]}euntis",   "Vpreactptcmdatsg": f"{x[0]}eunti",
            "Vpreactptcmablsg": MultipleEndings(regular=f"{x[0]}eunti", absolute=f"{x[0]}eunte"),
            "Vpreactptcmnompl": f"{x[0]}euntes",  "Vpreactptcmvocpl": f"{x[0]}euntes",   "Vpreactptcmaccpl": f"{x[0]}euntes",
            "Vpreactptcmgenpl": f"{x[0]}euntium", "Vpreactptcmdatpl": f"{x[0]}euntibus", "Vpreactptcmablpl": f"{x[0]}euntibus",
            "Vpreactptcfaccsg": f"{x[0]}euntem",  "Vpreactptcfgensg": f"{x[0]}euntis",   "Vpreactptcfdatsg": f"{x[0]}eunti",
            "Vpreactptcfablsg": MultipleEndings(regular=f"{x[0]}eunti", absolute=f"{x[0]}eunte"),
            "Vpreactptcfnompl": f"{x[0]}euntes",  "Vpreactptcfvocpl": f"{x[0]}euntes",   "Vpreactptcfaccpl": f"{x[0]}euntes",
            "Vpreactptcfgenpl": f"{x[0]}euntium", "Vpreactptcfdatpl": f"{x[0]}euntibus", "Vpreactptcfablpl": f"{x[0]}euntibus",
            "Vpreactptcngensg": f"{x[0]}euntis",  "Vpreactptcndatsg": f"{x[0]}eunti",
            "Vpreactptcnablsg": MultipleEndings(regular=f"{x[0]}eunti", absolute=f"{x[0]}eunte"),
            "Vpreactptcnnompl": f"{x[0]}euntia",  "Vpreactptcnvocpl": f"{x[0]}euntia",   "Vpreactptcnaccpl": f"{x[0]}euntia",
            "Vpreactptcngenpl": f"{x[0]}euntium", "Vpreactptcndatpl": f"{x[0]}euntibus", "Vpreactptcnablpl": f"{x[0]}euntibus",
        },
        additions={},
        deletions=set(),
    ),
    "eo_impersonal_passive": lambda x: DictChanges(  # e.g. abeo, abire, abii, abitus
        # various forms are regular throughout
        replacements={
            "Vpreactindpl3"   : f"{x[0]}eunt",
            "Vimpactindsg1"   : f"{x[0]}ibam",    "Vimpactindsg2"   : f"{x[0]}ibas",     "Vimpactindsg3"   : f"{x[0]}ibat",
            "Vimpactindpl1"   : f"{x[0]}ibamus",  "Vimpactindpl2"   : f"{x[0]}ibatis",   "Vimpactindpl3"   : f"{x[0]}ibant",
            "Vfutactindsg1"   : f"{x[0]}ibo",     "Vfutactindsg2"   : f"{x[0]}ibis",     "Vfutactindsg3"   : f"{x[0]}ibit",
            "Vfutactindpl1"   : f"{x[0]}ibimus",  "Vfutactindpl2"   : f"{x[0]}ibitis",   "Vfutactindpl3"   : f"{x[0]}ibunt",
            "Vimppasindsg3"   : f"{x[0]}ibatur",
            "Vfutpasindsg3"   : f"{x[0]}ibitur",
            "Vperactindsg2"   : f"{x[2]}isti",    "Vperactindpl2"   : f"{x[2]}istis",
            "Vpreactsbjsg3"   : f"{x[0]}eat",
            "Vplpactsbjsg1"   : f"{x[2]}issem",   "Vplpactsbjsg2"   : f"{x[2]}isses",    "Vplpactsbjsg3"   : f"{x[2]}isset",
            "Vplpactsbjpl1"   : f"{x[2]}issemus", "Vplpactsbjpl2"   : f"{x[2]}issetis",  "Vplpactsbjpl3"   : f"{x[2]}issent",
            "Vpreactptcmaccsg": f"{x[0]}euntem",  "Vpreactptcmgensg": f"{x[0]}euntis",   "Vpreactptcmdatsg": f"{x[0]}eunti",
            "Vpreactptcmablsg": MultipleEndings(regular=f"{x[0]}eunti", absolute=f"{x[0]}eunte"),
            "Vpreactptcmnompl": f"{x[0]}euntes",  "Vpreactptcmvocpl": f"{x[0]}euntes",   "Vpreactptcmaccpl": f"{x[0]}euntes",
            "Vpreactptcmgenpl": f"{x[0]}euntium", "Vpreactptcmdatpl": f"{x[0]}euntibus", "Vpreactptcmablpl": f"{x[0]}euntibus",
            "Vpreactptcfaccsg": f"{x[0]}euntem",  "Vpreactptcfgensg": f"{x[0]}euntis",   "Vpreactptcfdatsg": f"{x[0]}eunti",
            "Vpreactptcfablsg": MultipleEndings(regular=f"{x[0]}eunti", absolute=f"{x[0]}eunte"),
            "Vpreactptcfnompl": f"{x[0]}euntes",  "Vpreactptcfvocpl": f"{x[0]}euntes",   "Vpreactptcfaccpl": f"{x[0]}euntes",
            "Vpreactptcfgenpl": f"{x[0]}euntium", "Vpreactptcfdatpl": f"{x[0]}euntibus", "Vpreactptcfablpl": f"{x[0]}euntibus",
            "Vpreactptcngensg": f"{x[0]}euntis",  "Vpreactptcndatsg": f"{x[0]}eunti",
            "Vpreactptcnablsg": MultipleEndings(regular=f"{x[0]}eunti", absolute=f"{x[0]}eunte"),
            "Vpreactptcnnompl": f"{x[0]}euntia",  "Vpreactptcnvocpl": f"{x[0]}euntia",   "Vpreactptcnaccpl": f"{x[0]}euntia",
            "Vpreactptcngenpl": f"{x[0]}euntium", "Vpreactptcndatpl": f"{x[0]}euntibus", "Vpreactptcnablpl": f"{x[0]}euntibus",
        },
        additions={},
        deletions=set(),
    ),
    "facio": lambda x: DictChanges( # patefacio, patefacere, patefeci, patefactus
        # suppletive with 'fieri'
        replacements={
            "Vprepasindsg1": f"{x[0]}fio",      "Vprepasindsg2": f"{x[0]}fis",      "Vprepasindsg3": f"{x[0]}fit",
            "Vprepasindpl1": f"{x[0]}fimus",    "Vprepasindpl2": f"{x[0]}fitis",    "Vprepasindpl3": f"{x[0]}fiunt",
            "Vimppasindsg1": f"{x[0]}fiebam",   "Vimppasindsg2": f"{x[0]}fiebas",   "Vimppasindsg3": f"{x[0]}fiebat",
            "Vimppasindpl1": f"{x[0]}fiebamus", "Vimppasindpl2": f"{x[0]}fiebatis", "Vimppasindpl3": f"{x[0]}fiebant",
            "Vfutpasindsg1": f"{x[0]}fiam",     "Vfutpasindsg2": f"{x[0]}fies",     "Vfutpasindsg3": f"{x[0]}fiet",
            "Vfutpasindpl1": f"{x[0]}fiemus",   "Vfutpasindpl2": f"{x[0]}fietis",   "Vfutpasindpl3": f"{x[0]}fient",
            "Vprepassbjsg1": f"{x[0]}fiam",     "Vprepassbjsg2": f"{x[0]}fias",     "Vprepassbjsg3": f"{x[0]}fiat",
            "Vprepassbjpl1": f"{x[0]}fiamus",   "Vprepassbjpl2": f"{x[0]}fiatis",   "Vprepassbjpl3": f"{x[0]}fiant",
            "Vimppassbjsg1": f"{x[0]}fierem",   "Vimppassbjsg2": f"{x[0]}fieres",   "Vimppassbjsg3": f"{x[0]}fieret",
            "Vimppassbjpl1": f"{x[0]}fieremus", "Vimppassbjpl2": f"{x[0]}fieretis", "Vimppassbjpl3": f"{x[0]}fierent",
            "Vprepasipesg2": f"{x[0]}fi",       "Vprepasipepl2": f"{x[0]}fite",
            "Vfutpasipesg2": f"{x[0]}fito",     "Vfutpasipesg3": f"{x[0]}fito",
            "Vfutpasipepl2": f"{x[0]}fitote",   "Vfutpasipepl3": f"{x[0]}fiunto",
            "Vprepasinf   ": f"{x[0]}fieri",
        },
        additions={},
        deletions=set(),
    ),
}  # fmt: skip

_DERIVED_PRINCIPAL_STEMS: Final[
    dict[_DerivedVerbGroups, tuple[str, str, str, str]]
] = {
    "sum": ("sum", "esse", "fui", "futurus"),
    "sum_preptc": ("sum", "esse", "fui", "futurus"),
    "fero": ("fero", "ferre", "tuli", "latus"),
    "eo": ("eo", "ire", "ii", "itus"),
    "eo_impersonal_passive": ("eo", "ire", "ii", "itus"),
    "facio": ("facio", "facere", "feci", "factus"),
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
        "Nnomsg": "ego", "Nvocsg": "ego",   "Naccsg": "me",
        "Ngensg": "mei", "Ndatsg": "mihi",  "Nablsg": "me",
        "Nnompl": "nos", "Nvocpl": "nos",   "Naccpl": "nos",
        "Ngenpl": MultipleEndings(regular="nostri", partitive="nostrum"),
        "Ndatpl": "nobis", "Nablpl": "nobis",
    },
    "nos": { # Plurals as sometimes they are included in vocab lists alone
        "Nnompl": "nos", "Nvocpl": "nos",   "Naccpl": "nos",
        "Ngenpl": MultipleEndings(regular="nostri", partitive="nostrum"),
        "Ndatpl": "nobis", "Nablpl": "nobis",
    },
    "tu": {
        "Nnomsg": "tu", "Nvocsg": "tu",    "Naccsg": "te",
        "Ngensg": "tui", "Ndatsg": "tibi",  "Nablsg": "te",
        "Nnompl": "vos", "Nvocpl": "vos",   "Naccpl": "vos",
        "Ngenpl": MultipleEndings(regular="vestri", partitive="vestrum"),
        "Ndatpl": "vobis", "Nablpl": "vobis",
    },
    "vos": {
        "Nnompl": "vos", "Nvocpl": "vos",   "Naccpl": "vos",
        "Ngenpl": MultipleEndings(regular="vestri", partitive="vestrum"),
        "Ndatpl": "vobis", "Nablpl": "vobis",
    },
    "se": {
        "Naccsg": "se",
        "Ngensg": "sui", "Ndatsg": "sibi", "Nablsg": "se",
        "Naccpl": "se",
        "Ngenpl": "sui", "Ndatpl": "sibi", "Nablpl": "se",
    },
}  # fmt: skip

IRREGULAR_DECLINED_NOUNS: Final[dict[str, Endings]] = {
    "deus": {
        "Nnomsg": "deus",
        "Nvocsg": MultipleEndings(regular="dee", second="deus"),
        "Naccsg": "deum",
        "Ngensg": "dei",  "Ndatsg": "deo", "Nablsg": "deo",
        "Nnompl": MultipleEndings(regular="dei", second="di", third="dii"),
        "Nvocpl": MultipleEndings(regular="dei", second="di", third="dii"),
        "Naccpl": "deos",
        "Ngenpl": MultipleEndings(regular="deorum", second="deum"),
        "Ndatpl": MultipleEndings(regular="deis", second="dis", third="diis"),
        "Nablpl": MultipleEndings(regular="deis", second="dis", third="diis"),
    },
    "dea": {
        "Nnomsg": "dea",    "Nvocsg": "dea",    "Naccsg": "deam",
        "Ngensg": "deae",   "Ndatsg": "deae",   "Nablsg": "dea",
        "Nnompl": "deae",   "Nvocpl": "deae",   "Naccpl": "deas",
        "Ngenpl": "dearum", "Ndatpl": "deabus", "Nablpl": "deabus",
    },
    "domus": {  # domus will be considered as a fourth declension noun only
        "Nnomsg": "domus",   "Nvocsg": "domus",   "Naccsg": "domum",
        "Ngensg": MultipleEndings(regular="domus", locative="domi"),
        "Ndatsg": MultipleEndings(regular="domui", second="domo", third="domu"),
        "Nablsg": MultipleEndings(regular="domu", second="domo"),  # for consistency
        "Nnompl": "domus",   "Nvocpl": "domus",
        "Naccpl": MultipleEndings(regular="domus", second="domos"),
        "Ngenpl": MultipleEndings(regular="domuum", second="domorum"),
        "Ndatpl": "domibus", "Nablpl": "domibus",
    },
    "bos": {
        "Nnomsg": "bos",   "Nvocsg": "bos",   "Naccsg": "bovem",
        "Ngensg": "bovis", "Ndatsg": "bovi",  "Nablsg": "bove",
        "Nnompl": "boves", "Nvocpl": "boves", "Naccpl": "boves",
        "Ngenpl": MultipleEndings(regular="bovum", second="boum", third="boverum"),
        "Ndatpl": MultipleEndings(regular="bovibus", second="bobus", third="bubus"),
        "Nablpl": MultipleEndings(regular="bovibus", second="bobus", third="bubus"),
    },
    "epulum": {
        "Nnomsg": "epulum", "Nvocsg": "epulum", "Naccsg": "epulum",
        "Ngensg": "epuli",  "Ndatsg": "epulo",  "Nablsg": "epulo",
        "Nnompl": MultipleEndings(regular="epula", second="epulae"),
        "Nvocpl": MultipleEndings(regular="epula", second="epulae"),
        "Naccpl": MultipleEndings(regular="epula", second="epulas"),
        "Ngenpl": MultipleEndings(regular="epulorum", second="epularum"),
        "Ndatpl": "epulis", "Nablpl": "epulis",
    },
    "sus": {
        "Nnomsg": "sus",  "Nvocsg": "sus",  "Naccsg": "suem",
        "Ngensg": "suis", "Ndatsg": "sui",  "Nablsg": "sue",
        "Nnompl": "sues", "Nvocpl": "sues", "Naccpl": "sues",
        "Ngenpl": "suum",
        "Ndatpl": MultipleEndings(regular="suibus", second="subus"),
        "Nablpl": MultipleEndings(regular="suibus", second="subus"),
    },
}  # fmt: skip

# -----------------------------------------------------------------------------
# ADJECTIVES

LIS_ADJECTIVES: Final[set[str]] = {
    "facilis", "difficilis", "similis", "dissimilis", "gracilis", "humilis",
}  # fmt: skip

# Contains adjectives that have irregular forms in the comparative,
# superlative and adverb forms.
# Note that some of these adjectives do not have adverb forms, so the adverb
# forms are given a None value instead.
IRREGULAR_STEM_ADJECTIVES: Final[
    dict[str, tuple[str, str, str | None, str | None, str | None]]
] = {
    "bonus": ("melior", "optim", "bene", "melius", "optime"),
    "malus": ("peior", "pessim", "male", "peius", "pessime"),
    "magnus": ("maior", "maxim", None, None, None),
    "parvus": ("minor", "minim", None, None, None),
    # multo (adverb) exists but that would very much stuff up things
    # TODO: Maybe it can not stuff up things?
    "multus": ("plus", "plurim", None, None, None),
    # nequam should probably just be put in as a regular
    "nequam": ("nequior", "nequissim", None, None, None),
    "frugi": ("frugalior", "frugalissim", "frugaliter", "frugalius", "frugalissime"),
    "dexter": ("dexterior", "dextim", None, None, None),
    # ultro (adverb) exists but that would very much stuff up things
    "ulter": ("ulterior", "ultim", None, None, None),
    # FIXME: but 'extimus' exists for superlative
    # Would need to define way to get MultipleEndings into f-strings perhaps?
    "exter": ("exterior", "extrem", None, None, None),
    # Same here with 'postumus'
    "posterus": ("posterior", "postrem", None, None, None),
    # supra (adverb) exists but that would very much stuff up things
    # Superlatives 'superrimus' 'superrumus' 'summus'
    "superus": ("superior", "suprem", None, None, None),
}  # fmt: skip

IRREGULAR_ADJECTIVES: Final[dict[str, Endings]] = {
    "duo": {
        "Aposmnompl": "duo",
        "Aposmvocpl": "duo",
        "Aposmaccpl": MultipleEndings(regular="duos", second="duo"),
        "Aposmgenpl": MultipleEndings(regular="duorum", second="duum"),
        "Aposmdatpl": "duobus",
        "Aposmablpl": "duobus",
        "Aposfnompl": "duae",
        "Aposfvocpl": "duae",
        "Aposfaccpl": "duas",
        "Aposfgenpl": "duarum",
        "Aposfdatpl": "duabus",
        "Aposfablpl": "duabus",
        "Aposnnompl": "duo",
        "Aposnvocpl": "duo",
        "Aposnaccpl": "duo",
        "Aposngenpl": MultipleEndings(regular="duorum", second="duum"),
        "Aposndatpl": "duobus",
        "Aposnablpl": "duobus",
    }
}

# adjectives with principal parts that don't match validation code (so bypass them)
IRREGULAR_PP_ADJECTIVES: Final[set[str]] = {"tres"}

# Taken from https://en.wiktionary.org/wiki/Category:Latin_uncomparable_adverbs
UNCOMPARABLE_ADVERBS: Final[set[str]] = {
    "gratis", "abdicative", "abusive", "fere", "eo", "here", "imperative", "qua", "rite", "sic", "sat", "vero", "et", "gratuito", 
    "ni", "universe", "ne", "ea", "nec", "forte", "mane", "ubique", "numquam", "quotidie", "quotannis", "dein", "hodie", 
    "scilicet", "jam", "ter", "luce", "umquam", "alias", "alibi", "amen", "ante", "numero", "passive", "finite", "hic", "super", 
    "semper", "relative", "frustra", "ut", "nunc", "ergo", "crebra", "canatim", "acervatim", "quadrupedatim", "vermiculate", 
    "olim", "una", "haut", "quaque", "undique", "cavernatim", "undatim", "Celtice", "Anglice", "triste", "nuncupative", "tam", 
    "solum", "ita", "circa", "verbatim", "quid", "cur", "mere", "mire", "diverse", "clam", "cetera", "mox", "repente", "furtim", 
    "subito", "hoc", "denique", "quidem", "qui", "temere", "mage", "item", "furto", "interim", "paene", "post", "ubi", "nunquam", 
    "versus", "futile", "pone", "dulce", "ferme", "heri", "forsan", "quoque", "cordate", "suave", "alio", "reflexive", "ultra", 
    "sexto", "primo", "tandem", "satis", "falso", "sacrilege", "pene", "quondam", "sincere", "bis", "como", "ideo", "inde", 
    "continuo", "contra", "retro", "num", "hoi", "juxta", "hau", "circum", "recto", "iam", "puta", "cras", "tum", "rursus", 
    "deinde", "festive", "tamen", "explicate", "adhuc", "semel", "tantum", "praesto", "propter", "unde", "idcirco", "ibidem", 
    "neque", "usque", "etiam", "nimium", "prius", "protinus", "uti", "nimis", "itaque", "iterum", "asseverate", "potius", "AUC", 
    "satin", "romanice", "sensate", "recens", "mutuum", "passim", "secundo", "sis", "inductive", "quo", "topper", "hac", "magis", 
    "videlicet", "foris", "sursum", "aliunde", "perenne", "simul", "vulgo", "sesqui", "patrie", "porro", "obiter", "statim", 
    "interea", "quocum", "sacrate", "quomodo", "abunde", "vix", "dilucide", "medie", "vicies", "tunc", "intra", "adeo", "casu", 
    "illo", "paulisper", "altum", "fors", "anniversarie", "procul", "enucleate", "gradatim", "minime", "quanti", "perdite", 
    "nonne", "neutro", "abhinc", "horno", "intemperate", "tanti", "verum", "mutuo", "aliquid", "incontra", "dorsum", 
    "inaugurato", "cubi", "romane", "superfluo", "caute", "contrarie", "mutua", "iuxta", "perpetuo", "perpetue", "duplicato", 
    "perfacile", "fortuito", "brevi", "recta", "divise", "impraesentiarum", "liberaliter", "porod", "nimirum", "sortito", 
    "maledice", "benedice", "nondum", "quin", "auspicato", "matutino", "primum", "sollerter", "sodes", "augurato", "perbene", 
    "confestim", "huc", "ilico", "nudius", "quadrate", "eminus", "ceu", "fortasse", "bifariam", "bipartito", "divinitus", 
    "divorse", "eadem", "exinde", "haud", "occulto", "quoquomodo", "quidni", "aliter", "alterne", "amabo", "humanitus", "humi", 
    "hinc", "repens", "loquaciter", "antea", "isti", "accusatorie", "hactenus", "hauddum", "gregatim", "gratiis", "forsit", 
    "forsitan", "fortassis", "amatorie", "omnino", "mecum", "tecum", "secum", "nobiscum", "vobiscum", "quicum", "quibuscum", 
    "satisne", "satine", "pondo", "consolatorie", "ubinam", "ubicumque", "foras", "multo", "primitus", "nuncupatim", "promiscue", 
    "imperiose", "conserte", "consuetudinarie", "eapropter", "improvide", "propterea", "litteratim", "millies", "quare", "quoad", 
    "huiusmodi", "quemadmodum", "comminus", "volup", "vulgare", "interdum", "tanquam", "nempe", "illico", "coniecturaliter", 
    "imprimis", "denuo", "quantumvis", "illi", "rivatim", "longule", "caelitus", "coelitus", "abinde", "posthac", "pagatim", 
    "dehinc", "nequiquam", "quadripartito", "sicut", "circiter", "commodum", "deorsum", "illic", "istuc", "pacifice", "prae", 
    "condicionaliter", "praeceps", "futtile", "palaestrice", "palaestricos", "palam", "propalam", "alternis", "palliolatim", 
    "membratim", "participialiter", "matronaliter", "patrice", "superne", "pancratice", "aviditer", "avariter", "aventer", 
    "imperiabiliter", "imperabiliter", "imperatorie", "quacum", "cotidie", "citra", "tempori", "equidem", "aeterno", "aeternum", 
    "aliquando", "perpetuum", "illac", "consulariter", "ultro", "subtus", "consentanee", "meridie", "bovatim", "velut", 
    "hospitaliter", "rursum", "inurbane", "gentilitus", "decenter", "somnialiter", "sedulo", "tantopere", "vicibus", 
    "adseverate", "praesertim", "iure", "graece", "tertium", "tertio", "quartum", "quintum", "maeste", "ceterum", "voluptuose", 
    "obviam", "dubie", "inferne", "producte", "spurce", "oppido", "commodo", "nihilo", "decimum", "eodem", "nocte", "alicubi", 
    "aliquanto", "aliquotiens", "vesperi", "paullo", "praes", "demum", "illoc", "interdiu", "municipatim", "nonnumquam", 
    "postea", "postremo", "privatim", "quater", "quotiens", "sponte", "viritim", "nonnihil", "aliqua", "aliquo", "saltem", 
    "admodum", "cumque", "duntaxat", "dumtaxat", "ejusmodi", "eiusmodi", "invicem", "nihilominus", "partim", "paulatim", 
    "paullatim", "proinde", "quamdiu", "quamvis", "quatenus", "revera", "tantundem", "unquam", "utrimque", "adaeque", "canonice", 
    "deinceps", "formaliter", "huiuscemodi", "iampridem", "pariter", "permaxime", "philosophice", "similiter", "specialiter", 
    "tamquam", "unice", "universaliter", "tantummodo", "nequando", "inscie", "praeterea", "quocumque", "sicuti", "aliquamdiu", 
    "aliquantum", "aliquam", "antiquitus", "bipertito", "retrorsum", "coram", "cuneatim", "desuper", "pridem", "identidem", 
    "iniussu", "insuper", "introrsus", "introrsum", "intus", "necubi", "nequaquam", "nusquam", "penitus", "posteaquam", 
    "postremum", "postridie", "potissimum", "praeterquam", "pridie", "profecto", "setius", "singillatim", "sinistrorsus", 
    "siquidem", "sudum", "tripertito", "turmatim", "utinam", "vicem", "vicissim", "alioquin", "alioqui", "amodo", "illuc", 
    "intrinsecus", "numquid", "peregre", "quacumque", "quaecumque", "quamcumque", "quoadusque", "quousque", "seorsum", "septies", 
    "usquequo", "utique", "utraque", "alterutrum", "alteruter", "deterius", "extrinsecus", "qualiter", "ingratis", "desursum", 
    "immo", "superabundanter", "corporaliter", "quapropter", "naturaliter", "milies", "quotienscumque", "easdem", "indesinenter", 
    "multifariam", "ostentui", "adversum", "solummodo", "taliter", "inpraesentiarum", "ambitiose", "exin", "libentissime", 
    "perperam", "proculdubio", "funditus", "simitu", "simitur", "sensim", "saltim", "tamdiu", "certatim", "illinc", "divisim", 
    "nexabunde", "explicanter", "familiariter", "parumper", "attamen", "extemplo", "forinsecus", "iuge", "qualibet", "commixtim", 
    "commistim", "consequenter", "septimum", "octavum", "consideranter", "consimiliter", "assentatorie", "adsentatorie", 
    "appetenter", "apprime", "adprime", "articulatim", "amplifice", "alicunde", "aliquantisper", "adfatim", "affatim", "adfabre", 
    "affabre", "actuose", "actutum", "aliorsum", "aliovorsum", "antehac", "antidea", "cottidie", "alternatim", "caesim", 
    "carptim", "castellatim", "cautim", "catervatim", "cursim", "circumscripte", "confertim", "centuriatim", "dudum", "eatenus", 
    "exsultim", "exultim", "generatim", "horsum", "correpte", "celeriuscule", "centiens", "centies", "curiatim", "deciens", 
    "decies", "deorsus", "derepente", "desperanter", "dextrorsum", "dextrorsus", "dextrovorsum", "dupliciter", "efficienter", 
    "fataliter", "feraciter", "furialiter", "generaliter", "genialiter", "adubi", "sinceriter", "sextum", "quinquies", 
    "septuagies", "quamobrem", "unianimiter", "istiusmodi", "memoriter", "quamlibet", "suppliciter", "prorsus", "totiens", 
    "procaciter", "quolibet", "tripliciter", "altrinsecus", "cognoscibiliter", "cuiusmodi", "gallice", "infirmiter", 
    "insipienter", "lycaonice", "minutatim", "multipliciter", "nequiter", "noctu", "particulatim", "perendie", "quantocius", 
    "quinimmo", "quoquam", "raptim", "segregatim", "sexies", "sicine", "sicubi", "silenter", "utpote", "utro", "mendaciter", 
    "sufficienter", "achariter", "ignoranter", "infideliter", "inprimis", "inpudenter", "impudenter", "propere", "quadrifariam", 
    "radicitus", "septempliciter", "terribiliter", "veluti", "etiamnum", "habitualiter", "idipsum", "incunctanter", 
    "inseparabiliter", "litteraliter", "originaliter", "peculiariter", "peramanter", "perinde", "personaliter", "pluries", 
    "praecellenter", "quodammodo", "reapse", "sollemniter", "summatim", "summopere", "symbolice", "aliquantulum", "aliquatenus", 
    "circulariter", "conformiter", "hujusmodi", "illibenter", "imo", "impotenter", "indifferenter", "ineleganter", 
    "infallibiliter", "insigniter", "insimul", "irregulariter", "regulariter", "itidem", "jampridem", "litterate", "localiter", 
    "magistraliter", "neutiquam", "nonnunquam", "noviter", "nullatenus", "nullibi", "ordinatim", "perniciter", 
    "perpendiculariter", "quantopere", "saepenumero", "secius", "sexagecuplum", "sigillatim", "sophistice", "sparsim", 
    "speciatim", "strictim", "subinde", "trifariam", "tropice", "uniformiter", "usquam", "cujusmodi", "quaelibet", "quamprimum", 
    "quovis", "sensibiliter", "impigre", "licenter", "muliebriter", "impariter", "luculenter", "perquam", "proin", "propemodum", 
    "quonam", "quorsum", "quoties", "rationaliter", "realiter", "simulac", "toties", "protenus", "uspiam", "circulatim", 
    "dispersim", "ecquid", "ioculariter", "istic", "mordicus", "notabiliter", "oppidatim", "persaepe", "plurifariam", 
    "provinciatim", "quaterdecies", "quingenties", "quinquiens", "regionatim", "sexagies", "sexagiens", "tricies", "vicatim", 
    "vivatim", "vixdum", "adhoc", "cuicuimodi", "ecquando", "etiamnunc", "iamdudum", "jamdudum", "ingratiis", "miliens", 
    "milliens", "ostiatim", "perliberaliter", "permixtim", "perraro", "populariter", "quadringentiens", "quadringenties", 
    "quindeciens", "quindecies", "quorsom", "tantisper", "triciens", "incomposite", "viciens", "propatulo", "ducenties", 
    "ducentiens", "inibi", "tributim", "quadragies", "quadragiens", "illim", "perbreviter", "aliquandiu", "petulanter", 
    "titubanter", "orthogonaliter", "utrinque", "octogies", "octogiens", "septiens", "voluptarie", "persapienter", 
    "incredibiliter", "propediem", "postmodo", "puriter", "trecenties", "trecentiens", "Volsce", "indidem", "ubertim", 
    "domesticatim", "duodecies", "subsultim", "cominus", "decussatim", "disiunctim", "independenter", "multoties", "postmodum", 
    "praeterpropter", "quantumlibet", "quomodolibet", "seiunctim", "fasciatim", "albescente", "hoze", "Iberice", "anglice", 
    "exadversum", "danice", "recessim", "adusque", "aliuta", "assulatim", "bacchatim", "blanditim", "capreolatim", "citatim", 
    "collusorie", "datatim", "improperanter", "pedatim", "perlubenter", "fabriliter", "indiscriminatim", "perpetim", "jactanter", 
    "iamiam", "jamjam", "iamiamque", "jamjamque", "iuxtim", "juxtim", "perdiu", "duis", "minume", "hucusque", "surridicule", 
    "subridicule", "peraeque", "meliuscule", "munditer", "nitenter", "nonies", "pompaliter", "proquam", "quadantenus", 
    "quadratim", "quadrifariter", "reflexim", "septifariam", "signanter", "somniculose", "tabulatim", "testatim", "ubilibet", 
    "ubiquaque", "ubivis", "ullatenus", "universatim", "vacive", "vafre", "veraciter", "volgariter", "cujuscemodi", "iccirco", 
    "nequicquam", "quojus", "quorsus", "eoad", "disjunctim", "hujuscemodi", "indisiunctim", "indisjunctim", "sejunctim", 
    "accedenter", "undecies", "quandocumque", "facul", "prosus", "utcumque", "tumultuario", "aegyptiace", "etiamdum", 
    "circumcirca", "ilicet", "sophos", "clanculum", "verticaliter", "usurpative", "guttatim", "quirquir", "Hiberice", 
    "trinaliter", "plerumque", "plerunque", "pleraque", "undecumque", "insolabiliter", "simulatque", "dedicative", "exim", 
    "minutim", "tantumdem", "quoquo", "quaqua", "vesperascente", "trucissime", "tuatim", "meatim", "utque", "dunc", 
    "nichilominus", "desusum", "novies", "unciatim", "haudquaquam", "hmoi", "longitrorsus", "longitrosus", "istinc", "nequo", 
    "octies", "iusum", "diatim", "dietim", "Cimbrice", "compluriens", "dierecte", "utut", "usualiter", "fartim", "medullitus", 
    "aliquovorsum", "istorsum", "poenaliter", "certative", "pugnitus", "punctim", "pugilice", "sensualiter", "sententialiter", 
    "visibiliter", "aemulanter", "adpetenter", "expetenter", "perpetualiter", "contemplabiliter", "contemplatim", "templatim", 
    "extempulo", "patronymice", "tractabiliter", "tractim", "conducibiliter", "deductim", "signatim", "praedicative", "oretenus", 
    "aliquoties", "permale", "pessum", "quantisper", "incassum", "siremps", "viꝫ", "usqꝫ", "scissim", "fluctuatim", "quomo", 
    "temporatim", "quandoque", "noscum", "voscum", "urbanatim", "noctanter", "inpigre", "rusticatim", "maestiter", "laetanter", 
    "dextere", "totaliter", "umbraliter", "amariter", "cunque", "capitulatim", "desubito", "efflictim", "enimvero", "exiliter", 
    "furenter", "immisericorditer", "immortaliter", "incisim", "infabre", "innumerabiliter", "insatiabiliter", "abaliud", 
    "utrubi", "incurabiliter", "irremediabiliter", "irremisse", "irremissibiliter", "taxim", "velud", "urceatim", "sicunde", 
    "laudabiliter", "undequadragiens", "duodetriciens", "nonagiens", "quinquagiens", "quinquagies", "manipulatim", "multimodis", 
    "tolutim", "rationabiliter", "ideoque", "ritualiter", "abante", "extunc", "usquequaque", "alacriter", "numne", "numnam", 
    "nuncubi", "pectinatim", "cordicitus", "rarenter", "stirpitus", "illatenus", "praequam", "animitus", "quotlibet", "opipare", 
    "perbelle", "perbenigne", "corditus", "undelibet", "universim", "quotiescumque", "glorianter", "aliqualiter", "oculitus", 
    "dubitatim", "syndesmotice", "viliter", "ceteroqui", "illorsum", "observanter", "aliquisquam", "quotcumque", "quomodocumque", 
    "nudiustertius", "ampliter", "pertinenter", "nominaliter", "sciꝫ", "gradualiter", "qn̄ꝫ", "utrubique", "iosum", "deorsom", 
    "deosum", "zosum", "iosu", "diosum", "deorsu", "iosso", "iossu", "iusu", "nunciam", "inquantum", "offatim", "terdeciens", 
    "tergiversanter", "noviens", "praeterhac", "quandolibet", "undeunde", "disertim", "sedecies", "sexdecies", "aliquit", 
    "stillatim", "lasciviter", "stillanter", "actualiter", "virtualiter", "ambifariam", "ambifarius", "summissim", "submissim", 
    "simulter", "solerter", "faculter", "nominetenus", "omnifariam", "nonnil", "nonnichil", "scalatim", "nichilo", "pluraliter", 
    "ubiubi",
}  # fmt: skip

# Created from pipx run src/scripts/create_adjective_with_adverb.py, then copying and word wrapping result
REAL_ADVERB_ADJECTIVES: Final[set[str]] = {
    "irremediabilis", "decorus", "muscosus", "sextuplex", "suavis", "activus", "palaestricus", "perfidelis", "sanus", "praecipuus", 
    "collaudabilis", "celer", "vivax", "syndesmoticus", "iocularis", "apprimus", "frequens", "superus", "purus", 
    "plenus", "respectivus", "nasutus", "inaequalis", "Celticus", "culpabilis", "atrox", "impar", "nuncupativus", "hilaris", 
    "unanimus", "condicionalis", "communis", "infidelis", "evidens", "acer", "fabrilis", "iudicialis", "lepidus", "ocularis", 
    "idoneus", "gratus", "iactans", "orthogonalis", "gentilis", "pugnax", "quincuplex", "imperitus", "germanus", "opiparus", 
    "fatalis", "sollers", "sortitus", "irregularis", "verus", "impatiens", "atticus", "poenalis", "invisibilis", "continens", 
    "dulcis", "superfluus", "patronymicus", "cognoscibilis", "tyrannicus", "extemporalis", "frugalis", "densus", "inenodabilis", 
    "egregius", "invidiosus", "realis", "brevis", "blandus", "amatorius", "impiger", "exilis", "foelix", "quinquiplex", 
    "infirmus", "clarus", "eximius", "bellus", "verax", "procax", "unanimis", "fanaticus", "largus", "studiosus", "creber", 
    "putidus", "accommodatus", "contemptus", "lenis", "Latinus", "formosus", "fortis", "contemplabilis", "pertinax", "improsper", 
    "rabiosus", "muliebris", "tumidus", "verticalis", "absconditus", "dissimilis", "fallax", "pompalis", "imperativus", "uber", 
    "placidus", "magistralis", "avidus", "inhospitalis", "divinus", "immortalis", "centralis", "tardus", "indefessus", "civilis", 
    "Numidus", "passivus", "benevolus", "mendax", "luculentus", "maestus", "iocundus", "imprudens", "peritus", "inanis", 
    "infelix", "conubialis", "magnificus", "ducalis", "acerbus", "servilis", "peramans", "cordialis", "superbus", "malus", 
    "acharis", "aequus", "declamatorius", "inutilis", "significatorius", "inclemens", "insipiens", "serus", "multus", 
    "patheticus", "consuetudinarius", "promiscuus", "sedulus", "Ibericus", "vermiculatus", "regularis", "inreprehensibilis", 
    "admirabilis", "officialis", "solidus", "haereticus", "venustus", "petulans", "contentus", "improbus", "inurbanus", 
    "aliquantus", "castus", "actuosus", "generalis", "concinnus", "argutus", "aeternus", "hiulcus", "adverbialis", "indisertus", 
    "semicircularis", "insignis", "innumerabilis", "vafer", "pudens", "iracundus", "perfacilis", "senilis", "adulatorius", 
    "linearis", "subitus", "grandis", "medicabilis", "sublimis", "dolosus", "abundus", "Cimbricus", "independens", "similis", 
    "tranquillus", "perpendicularis", "adsiduus", "socors", "militarius", "primus", "philosophicus", "amarus", "impunis", 
    "citus", "laudabilis", "cautus", "iucundus", "peculiaris", "cruentus", "lacrimosus", "simplex", "formalis", "benignus", 
    "causarius", "cordatus", "lugubris", "irremissibilis", "identicus", "universalis", "praecellens", "patricus", "pronus", 
    "politicus", "jactans", "contumax", "tripertitus", "attentus", "imperiosus", "vulgaris", "sophisticus", "inpunis", 
    "immodestus", "litteratus", "fraudulentus", "virilis", "litteralis", "bipartitus", "coniecturalis", "astutus", 
    "consentaneus", "duplex", "quadruplex", "consimilis", "idealis", "persapiens", "foedus", "lubens", "palliolatus", "copiosus", 
    "flagitiosus", "irreprehensibilis", "fartus", "impudens", "romanicus", "personalis", "pacificus", "gravis", "sententialis", 
    "incurabilis", "Numidicus", "stultus", "femininus", "sensibilis", "naturalis", "puerilis", "effrenatus", "licens", "quies", 
    "accusatorius", "eminens", "amoenus", "constans", "salsus", "aegyptiacus", "hostilis", "futtilis", "inseparabilis", 
    "honorificus", "militaris", "indebitus", "somniculosus", "longinquus", "indefensus", "ingeniosus", "memor", "rapidus", 
    "crudelis", "frugi", "libens", "insalubris", "perspicax", "lacrimabilis", "symbolicus", "obscurus", "querulus", "Megaricus", 
    "excellens", "tentativus", "vacivus", "periculosus", "tolerabilis", "inhumanus", "infirmis", "virulentus", "fidelis", 
    "saluber", "originalis", "saepis", "trux", "uniformis", "mollis", "tenuis", "infrequens", "aequabilis", "sollemnis", 
    "aliqualis", "incredibilis", "laboriosus", "elegans", "longulus", "romanus", "fortuitus", "properus", "anilis", "humilis", 
    "modestus", "affabilis", "favorabilis", "precativus", "gulosus", "sagax", "pellax", "obnoxius", "manifestus", "callidus", 
    "Hibericus", "insatiabilis", "indissolubilis", "popularis", "contrarius", "hospitalis", "unianimis", "firmus", "durabilis", 
    "velox", "perpetualis", "sacrilegus", "internus", "relativus", "ferinus", "prudens", "ridiculus", "gelidus", "sensualis", 
    "inculpatus", "laetus", "septemplex", "incruentus", "latinus", "rationalis", "inelegans", "necessus", "oscitans", 
    "perbrevis", "insuperabilis", "generosus", "immisericors", "loquax", "subtilis", "mobilis", "avarus", "violentus", "invisus", 
    "liberalis", "talis", "pravus", "visibilis", "perfectus", "legitimus", "sincerus", "improprius", "regalis", "gracilis", 
    "rarus", "durus", "indubius", "criticus", "megaricus", "perrarus", "facilis", "credibilis", "quintuplex", "magnus", 
    "ambiguus", "firmis", "minutus", "anniversarius", "turpis", "aequalis", "latus", "ulter", "tractabilis", "necessarius", 
    "commodus", "dierectus", "habitualis", "conformis", "amicus", "ferox", "patrius", "certus", "paulus", "beatus", "papillaris", 
    "perennis", "minax", "praeproperus", "arctus", "supernus", "utilis", "serenus", "sententiosus", "longiusculus", "frigidus", 
    "difficilis", "perridiculus", "probus", "fugax", "altus", "miser", "hilarus", "adclivis", "ignorabilis", "consularis", 
    "incontinens", "novemplex", "torvus", "indispositus", "inferus", "longanimis", "impius", "vigilans", "mundus", 
    "incompositus", "spiritalis", "auspicatus", "inpudens", "indiscretus", "iugis", "meliusculus", "asper", "interrogativus", 
    "liber", "consolatorius", "inconstans", "bonus", "danicus", "mirabilis", "gloriosus", "clemens", "numerosus", "septuplex", 
    "pretiosus", "providus", "notabilis", "Libycus", "securus", "scholasticus", "singularis", "vitiosus", "inoffensus", "pius", 
    "participialis", "tutus", "humanus", "potissimus", "barbarus", "vocalis", "imperatorius", "stomachosus", "usualis", "unicus", 
    "mutuus", "agilis", "diversus", "felix", "fortunatus", "longus", "insolens", "pernix", "impurus", "impotens", "decemplex", 
    "Atticus", "enervis", "romanticus", "trinalis", "verisimilis", "mediocris", "lentus", "irrisibilis", "praeclarus", "moralis", 
    "probabilis", "Occitanus", "indifferens", "pudicus", "reflexivus", "par", "tristis", "assiduus", "festivus", "gratuitus", 
    "conducibilis", "intemperatus", "saevus", "candidulus", "cothurnatus", "intemperans", "specialis", "familiaris", "continuus", 
    "supplex", "localis", "jocundus", "aeger", "fraternus", "instrenuus", "circularis", "indigestus", "multiplex", "essentialis", 
    "triplex", "complusculi", "prolixus", "sonorus", "efficax", "excusabilis", "jucundus", "opportunus", "genialis", "laxus", 
    "corporalis", "discordiosus", "horribilis", "pulcher", "consideratus", "strenuus", "terribilis", "absurdus", "repens", 
    "ferax", "normalis", "planus", "matronalis", "philosophus", "perpetuus", "gallicus", "novus", "pollucibilis", "illecebrosus", 
    "amplus", "audax", "navus", "tener", "pulcer", "animosus", "vicinus", "acutulus", "furialis", "futilis", "indiligens", 
    "comis", "segnis", "universus", "centumplex", "levis", "violens", "sensatus", "lividus", "amabilis", "vehemens"
}  # fmt: skip


# -----------------------------------------------------------------------------
# PRONOUNS

PRONOUNS: Final[dict[str, Endings]] = {
    "hic": {
        "Pmnomsg": "hic",  "Pmaccsg": "hunc", "Pmgensg": "huius", "Pmdatsg": "huic", "Pmablsg": "hoc",
        "Pmnompl": "hi",   "Pmaccpl": "hos",  "Pmgenpl": "horum", "Pmdatpl": "his",  "Pmablpl": "his",
        "Pfnomsg": "haec", "Pfaccsg": "hanc", "Pfgensg": "huius", "Pfdatsg": "huic", "Pfablsg": "hac",
        "Pfnompl": "hae",  "Pfaccpl": "has",  "Pfgenpl": "harum", "Pfdatpl": "his",  "Pfablpl": "his",
        "Pnnomsg": "hoc",  "Pnaccsg": "hoc",  "Pngensg": "huius", "Pndatsg": "huic", "Pnablsg": "hoc",
        "Pnnompl": "haec", "Pnaccpl": "haec", "Pngenpl": "horum", "Pndatpl": "his",  "Pnablpl": "his",
    },
    "ille": {
        "Pmnomsg": "ille",  "Pmaccsg": "illum", "Pmgensg": "illius",  "Pmdatsg": "illi",  "Pmablsg": "illo",
        "Pmnompl": "illi",  "Pmaccpl": "illos", "Pmgenpl": "illorum", "Pmdatpl": "illis", "Pmablpl": "illis",
        "Pfnomsg": "illa",  "Pfaccsg": "illam", "Pfgensg": "illius",  "Pfdatsg": "illi",  "Pfablsg": "illa",
        "Pfnompl": "illae", "Pfaccpl": "illas", "Pfgenpl": "illarum", "Pfdatpl": "illis", "Pfablpl": "illis",
        "Pnnomsg": "illud", "Pnaccsg": "illud", "Pngensg": "illius",  "Pndatsg": "illi",  "Pnablsg": "illo",
        "Pnnompl": "illa",  "Pnaccpl": "illa",  "Pngenpl": "illorum", "Pndatpl": "illis", "Pnablpl": "illis",
    },
    "is": {
        "Pmnomsg": "is",  "Pmaccsg": "eum", "Pmgensg": "eius",  "Pmdatsg": "ei",  "Pmablsg": "eo",
        "Pmnompl": "ei",  "Pmaccpl": "eos", "Pmgenpl": "eorum", "Pmdatpl": "eis", "Pmablpl": "eis",
        "Pfnomsg": "ea",  "Pfaccsg": "eam", "Pfgensg": "eius",  "Pfdatsg": "ei",  "Pfablsg": "ea",
        "Pfnompl": "eae", "Pfaccpl": "eas", "Pfgenpl": "earum", "Pfdatpl": "eis", "Pfablpl": "eis",
        "Pnnomsg": "id",  "Pnaccsg": "id",  "Pngensg": "eius",  "Pndatsg": "ei",  "Pnablsg": "eo",
        "Pnnompl": "ea",  "Pnaccpl": "ea",  "Pngenpl": "eorum", "Pndatpl": "eis", "Pnablpl": "eis",
    },
    "ipse": {
        "Pmnomsg": "ipse",  "Pmaccsg": "ipsum", "Pmgensg": "ipsius",  "Pmdatsg": "ipsi",  "Pmablsg": "ipso",
        "Pmnompl": "ipsi",  "Pmaccpl": "ipsos", "Pmgenpl": "ipsorum", "Pmdatpl": "ipsis", "Pmablpl": "ipsis",
        "Pfnomsg": "ipsa",  "Pfaccsg": "ipsam", "Pfgensg": "ipsius",  "Pfdatsg": "ipsi",  "Pfablsg": "ipsa",
        "Pfnompl": "ipsae", "Pfaccpl": "ipsas", "Pfgenpl": "ipsarum", "Pfdatpl": "ipsis", "Pfablpl": "ipsis",
        "Pnnomsg": "ipsum", "Pnaccsg": "ipsum", "Pngensg": "ipsius",  "Pndatsg": "ipsi",  "Pnablsg": "ipso",
        "Pnnompl": "ipsa",  "Pnaccpl": "ipsa",  "Pngenpl": "ipsorum", "Pndatpl": "ipsis", "Pnablpl": "ipsis",
    },
    "idem": {
        "Pmnomsg": "idem",   "Pmaccsg": "eundem", "Pmgensg": "eiusdem",  "Pmdatsg": "eidem",  "Pmablsg": "eodem",
        "Pmnompl": "eidem",  "Pmaccpl": "eosdem", "Pmgenpl": "eorundem", "Pmdatpl": "eisdem", "Pmablpl": "eisdem",
        "Pfnomsg": "eadem",  "Pfaccsg": "eandem", "Pfgensg": "eiusdem",  "Pfdatsg": "eidem",  "Pfablsg": "eadem",
        "Pfnompl": "eaedem", "Pfaccpl": "easdem", "Pfgenpl": "earundem", "Pfdatpl": "eisdem", "Pfablpl": "eisdem",
        "Pnnomsg": "idem",   "Pnaccsg": "idem",   "Pngensg": "eiusdem",  "Pndatsg": "eidem",  "Pnablsg": "eodem",
        "Pnnompl": "eadem",  "Pnaccpl": "eadem",  "Pngenpl": "eorundem", "Pndatpl": "eisdem", "Pnablpl": "eisdem",
    },
    "qui": {
        "Pmnomsg": "qui",  "Pmaccsg": "quem", "Pmgensg": "cuius",  "Pmdatsg": "cui",    "Pmablsg": "quo",
        "Pmnompl": "qui",  "Pmaccpl": "quos", "Pmgenpl": "quorum", "Pmdatpl": "quibus", "Pmablpl": "quibus",
        "Pfnomsg": "quae", "Pfaccsg": "quam", "Pfgensg": "cuius",  "Pfdatsg": "cui",    "Pfablsg": "qua",
        "Pfnompl": "quae", "Pfaccpl": "quas", "Pfgenpl": "quarum", "Pfdatpl": "quibus", "Pfablpl": "quibus",
        "Pnnomsg": "quod", "Pnaccsg": "quod", "Pngensg": "cuius",  "Pndatsg": "cui",    "Pnablsg": "quo",
        "Pnnompl": "quae", "Pnaccpl": "quae", "Pngenpl": "quorum", "Pndatpl": "quibus", "Pnablpl": "quibus",
    },
    "quidam": {
        "Pmnomsg": "quidam",  "Pmaccsg": "quendam", "Pmgensg": "cuiusdam",  "Pmdatsg": "cuidam",    "Pmablsg": "quodam",
        "Pmnompl": "quidam",  "Pmaccpl": "quosdam", "Pmgenpl": "quorundam", "Pmdatpl": "quibusdam", "Pmablpl": "quibusdam",
        "Pfnomsg": "quaedam", "Pfaccsg": "quandam", "Pfgensg": "cuiusdam",  "Pfdatsg": "cuidam",    "Pfablsg": "quadam",
        "Pfnompl": "quaedam", "Pfaccpl": "quasdam", "Pfgenpl": "quarundam", "Pfdatpl": "quibusdam", "Pfablpl": "quibusdam",
        "Pnnomsg": "quoddam", "Pnaccsg": "quoddam", "Pngensg": "cuiusdam",  "Pndatsg": "cuidam",    "Pnablsg": "quodam",
        "Pnnompl": "quaedam", "Pnaccpl": "quaedam", "Pngenpl": "quorundam", "Pndatpl": "quibusdam", "Pnablpl": "quibusdam",
    },
    "aliquis": {
        "Pmnomsg": "aliquis",  "Pmaccsg": "aliquem", "Pmgensg": "alicuius",  "Pmdatsg": "alicui",    "Pmablsg": "aliquo",
        "Pmnompl": "aliqui",   "Pmaccpl": "aliquos", "Pmgenpl": "aliquorum", "Pmdatpl": "aliquibus", "Pmablpl": "aliquibus",
        "Pfnomsg": "aliqua",   "Pfaccsg": "aliquam", "Pfgensg": "alicuius",  "Pfdatsg": "alicui",    "Pfablsg": "aliqua",
        "Pfnompl": "aliquae",  "Pfaccpl": "aliquas", "Pfgenpl": "aliquarum", "Pfdatpl": "aliquibus", "Pfablpl": "aliquibus",
        "Pnnomsg": "aliquid",  "Pnaccsg": "aliquid", "Pngensg": "alicuius",  "Pndatsg": "alicui",    "Pnablsg": "aliquo",
        "Pnnompl": "aliqua",   "Pnaccpl": "aliqua",  "Pngenpl": "aliquorum", "Pndatpl": "aliquibus", "Pnablpl": "aliquibus",
    },
    "iste": {
        "Pmnomsg": "iste",  "Pmaccsg": "istum", "Pmgensg": "istius",  "Pmdatsg": "isti",  "Pmablsg": "isto",
        "Pmnompl": "isti",  "Pmaccpl": "istos", "Pmgenpl": "istorum", "Pmdatpl": "istis", "Pmablpl": "istis",
        "Pfnomsg": "ista",  "Pfaccsg": "istam", "Pfgensg": "istius",  "Pfdatsg": "isti",  "Pfablsg": "ista",
        "Pfnompl": "istae", "Pfaccpl": "istas", "Pfgenpl": "istarum", "Pfdatpl": "istis", "Pfablpl": "istis",
        "Pnnomsg": "istud", "Pnaccsg": "istud", "Pngensg": "istius",  "Pndatsg": "isti",  "Pnablsg": "isto",
        "Pnnompl": "ista",  "Pnaccpl": "ista",  "Pngenpl": "istorum", "Pndatpl": "istis", "Pnablpl": "istis",
    },
    "quisquam": {
        "Pmnomsg": "quisquam",
        "Pmaccsg": "quemquam",
        "Pmgensg": "cuiusquam",
        "Pmdatsg": "cuiquam",
        "Pmablsg": MultipleEndings(regular="quoquam", second="quiquam"),
        "Pfnomsg": "quisquam",
        "Pfaccsg": "quemquam",
        "Pfgensg": "cuiusquam",
        "Pfdatsg": "cuiquam",
        "Pfablsg": MultipleEndings(regular="quoquam", second="quiquam"),
        "Pnnomsg": MultipleEndings(regular="quidquam", second="quicquam"),
        "Pnaccsg": MultipleEndings(regular="quidquam", second="quicquam"),
        "Pngensg": "cuiusquam",
        "Pndatsg": "cuiquam",
        "Pnablsg": MultipleEndings(regular="quoquam", second="quiquam"),
    },
}  # fmt: skip
