import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from src.core.accido.endings import Verb
from src.core.accido.misc import Case, Gender, Mood, MultipleEndings, Number, Tense, Voice

# taken from src/core/accido/edge_cases.py before irregular verb reimplementation
IRREGULAR_VERBS = {
    "sum": {  # no passives
        "Vpreactindsg1": "sum", "Vpreactindsg2": "es", "Vpreactindsg3": "est", "Vpreactindpl1": "sumus", "Vpreactindpl2": "estis", "Vpreactindpl3": "sunt", "Vimpactindsg1": "eram", "Vimpactindsg2": "eras", "Vimpactindsg3": "erat", "Vimpactindpl1": "eramus", "Vimpactindpl2": "eratis", "Vimpactindpl3": "erant", "Vfutactindsg1": "ero", "Vfutactindsg2": "eris", "Vfutactindsg3": "erit", "Vfutactindpl1": "erimus", "Vfutactindpl2": "eritis", "Vfutactindpl3": "erunt", "Vperactindsg1": "fui", "Vperactindsg2": "fuisti", "Vperactindsg3": "fuit", "Vperactindpl1": "fuimus", "Vperactindpl2": "fuistis", "Vperactindpl3": "fuerunt", "Vplpactindsg1": "fueram", "Vplpactindsg2": "fueras", "Vplpactindsg3": "fuerat", "Vplpactindpl1": "fueramus", "Vplpactindpl2": "fueratis", "Vplpactindpl3": "fuerant", "Vfpractindsg1": "fuero", "Vfpractindsg2": "fueris", "Vfpractindsg3": "fuerit", "Vfpractindpl1": "fuerimus", "Vfpractindpl2": "fueritis", "Vfpractindpl3": "fuerint",
        "Vpreactsbjsg1": "sim", "Vpreactsbjsg2": "sis", "Vpreactsbjsg3": "sit", "Vpreactsbjpl1": "simus", "Vpreactsbjpl2": "sitis", "Vpreactsbjpl3": "sint", "Vimpactsbjsg1": "essem", "Vimpactsbjsg2": "esses", "Vimpactsbjsg3": "esset", "Vimpactsbjpl1": "essemus", "Vimpactsbjpl2": "essetis", "Vimpactsbjpl3": "essent", "Vperactsbjsg1": "fuerim", "Vperactsbjsg2": "fueris", "Vperactsbjsg3": "fuerit", "Vperactsbjpl1": "fuerimus", "Vperactsbjpl2": "fueritis", "Vperactsbjpl3": "fuerint", "Vplpactsbjsg1": "fuissem", "Vplpactsbjsg2": "fuisses", "Vplpactsbjsg3": "fuisset", "Vplpactsbjpl1": "fuissemus", "Vplpactsbjpl2": "fuissetis", "Vplpactsbjpl3": "fuissent",
        "Vpreactipesg2": "es", "Vpreactipepl2": "este",
        "Vpreactinf   ": "esse",
        "Vfutactptcfablpl": "futuris", "Vfutactptcfablsg": "futura", "Vfutactptcfaccpl": "futuras", "Vfutactptcfaccsg": "futuram", "Vfutactptcfdatpl": "futuris", "Vfutactptcfdatsg": "futurae", "Vfutactptcfgenpl": "futurarum", "Vfutactptcfgensg": "futurae", "Vfutactptcfnompl": "futurae", "Vfutactptcfnomsg": "futura", "Vfutactptcfvocpl": "futurae", "Vfutactptcfvocsg": "futura", "Vfutactptcmablpl": "futuris", "Vfutactptcmablsg": "futuro", "Vfutactptcmaccpl": "futuros", "Vfutactptcmaccsg": "futurum", "Vfutactptcmdatpl": "futuris", "Vfutactptcmdatsg": "futuro", "Vfutactptcmgenpl": "futurorum", "Vfutactptcmgensg": "futuri", "Vfutactptcmnompl": "futuri", "Vfutactptcmnomsg": "futurus", "Vfutactptcmvocpl": "futuri", "Vfutactptcmvocsg": "future", "Vfutactptcnablpl": "futuris", "Vfutactptcnablsg": "futuro", "Vfutactptcnaccpl": "futura", "Vfutactptcnaccsg": "futurum", "Vfutactptcndatpl": "futuris", "Vfutactptcndatsg": "futuro", "Vfutactptcngenpl": "futurorum", "Vfutactptcngensg": "futuri", "Vfutactptcnnompl": "futura", "Vfutactptcnnomsg": "futurum", "Vfutactptcnvocpl": "futura", "Vfutactptcnvocsg": "futurum",
    },
    "possum": {  # no imperatives, passives
        "Vpreactindsg1": "possum", "Vpreactindsg2": "potes", "Vpreactindsg3": "potest", "Vpreactindpl1": "possumus", "Vpreactindpl2": "potestis", "Vpreactindpl3": "possunt", "Vimpactindsg1": "poteram", "Vimpactindsg2": "poteras", "Vimpactindsg3": "poterat", "Vimpactindpl1": "poteramus", "Vimpactindpl2": "poteratis", "Vimpactindpl3": "poterant", "Vfutactindsg1": "potero", "Vfutactindsg2": "poteris", "Vfutactindsg3": "poterit", "Vfutactindpl1": "poterimus", "Vfutactindpl2": "poteritis", "Vfutactindpl3": "poterunt", "Vperactindsg1": "potui", "Vperactindsg2": "potuisti", "Vperactindsg3": "potuit", "Vperactindpl1": "potuimus", "Vperactindpl2": "potuistis", "Vperactindpl3": "potuerunt", "Vplpactindsg1": "potueram", "Vplpactindsg2": "potueras", "Vplpactindsg3": "potuerat", "Vplpactindpl1": "potueramus", "Vplpactindpl2": "potueratis", "Vplpactindpl3": "potuerant", "Vfpractindsg1": "potuero", "Vfpractindsg2": "potueris", "Vfpractindsg3": "potuerit", "Vfpractindpl1": "potuerimus", "Vfpractindpl2": "potueritis", "Vfpractindpl3": "potuerint",
        "Vpreactsbjsg1": "possim", "Vpreactsbjsg2": "possis", "Vpreactsbjsg3": "possit", "Vpreactsbjpl1": "possimus", "Vpreactsbjpl2": "possitis", "Vpreactsbjpl3": "possint", "Vimpactsbjsg1": "possem", "Vimpactsbjsg2": "posses", "Vimpactsbjsg3": "posset", "Vimpactsbjpl1": "possemus", "Vimpactsbjpl2": "possetis", "Vimpactsbjpl3": "possent", "Vperactsbjsg1": "potuerim", "Vperactsbjsg2": "potueris", "Vperactsbjsg3": "potuerit", "Vperactsbjpl1": "potuerimus", "Vperactsbjpl2": "potueritis", "Vperactsbjpl3": "potuerint", "Vplpactsbjsg1": "potuissem", "Vplpactsbjsg2": "potuisses", "Vplpactsbjsg3": "potuisset", "Vplpactsbjpl1": "potuissemus", "Vplpactsbjpl2": "potuissetis", "Vplpactsbjpl3": "potuissent",
        "Vpreactinf   ": "posse", "Vpreactptcfablpl": "potentibus", "Vpreactptcfablsg": MultipleEndings(regular="potenti",absolute="potente" ), "Vpreactptcfaccpl": "potentes", "Vpreactptcfaccsg": "potentem", "Vpreactptcfdatpl": "potentibus", "Vpreactptcfdatsg": "potenti", "Vpreactptcfgenpl": "potentium", "Vpreactptcfgensg": "potentis", "Vpreactptcfnompl": "potentes", "Vpreactptcfnomsg": "potens", "Vpreactptcfvocpl": "potentes", "Vpreactptcfvocsg": "potens", "Vpreactptcmablpl": "potentibus", "Vpreactptcmablsg": MultipleEndings(regular="potenti",absolute="potente" ), "Vpreactptcmaccpl": "potentes", "Vpreactptcmaccsg": "potentem", "Vpreactptcmdatpl": "potentibus", "Vpreactptcmdatsg": "potenti", "Vpreactptcmgenpl": "potentium", "Vpreactptcmgensg": "potentis", "Vpreactptcmnompl": "potentes", "Vpreactptcmnomsg": "potens", "Vpreactptcmvocpl": "potentes", "Vpreactptcmvocsg": "potens", "Vpreactptcnablpl": "potentibus", "Vpreactptcnablsg": MultipleEndings(regular="potenti",absolute="potente" ), "Vpreactptcnaccpl": "potentia", "Vpreactptcnaccsg": "potens", "Vpreactptcndatpl": "potentibus", "Vpreactptcndatsg": "potenti", "Vpreactptcngenpl": "potentium", "Vpreactptcngensg": "potentis", "Vpreactptcnnompl": "potentia", "Vpreactptcnnomsg": "potens", "Vpreactptcnvocpl": "potentia", "Vpreactptcnvocsg": "potens",
    },
    "volo": {  # no imperatives, passives
        "Vpreactindsg1": "volo", "Vpreactindsg2": "vis", "Vpreactindsg3": "vult", "Vpreactindpl1": "volumus", "Vpreactindpl2": "vultis", "Vpreactindpl3": "volunt", "Vimpactindsg1": "volebam", "Vimpactindsg2": "volebas", "Vimpactindsg3": "volebat", "Vimpactindpl1": "volebamus", "Vimpactindpl2": "volebatis", "Vimpactindpl3": "volebant", "Vfutactindsg1": "volam", "Vfutactindsg2": "voles", "Vfutactindsg3": "volet", "Vfutactindpl1": "volemus", "Vfutactindpl2": "voletis", "Vfutactindpl3": "volent", "Vperactindsg1": "volui", "Vperactindsg2": "voluisti", "Vperactindsg3": "voluit", "Vperactindpl1": "voluimus", "Vperactindpl2": "voluistis", "Vperactindpl3": "voluerunt", "Vplpactindsg1": "volueram", "Vplpactindsg2": "volueras", "Vplpactindsg3": "voluerat", "Vplpactindpl1": "volueramus", "Vplpactindpl2": "volueratis", "Vplpactindpl3": "voluerant", "Vfpractindsg1": "voluero", "Vfpractindsg2": "volueris", "Vfpractindsg3": "voluerit", "Vfpractindpl1": "voluerimus", "Vfpractindpl2": "volueritis", "Vfpractindpl3": "voluerint",
        "Vpreactsbjsg1": "velim", "Vpreactsbjsg2": "velis", "Vpreactsbjsg3": "velit", "Vpreactsbjpl1": "velimus", "Vpreactsbjpl2": "velitis", "Vpreactsbjpl3": "velint", "Vimpactsbjsg1": "vellem", "Vimpactsbjsg2": "velles", "Vimpactsbjsg3": "vellet", "Vimpactsbjpl1": "vellemus", "Vimpactsbjpl2": "velletis", "Vimpactsbjpl3": "vellent", "Vperactsbjsg1": "voluerim", "Vperactsbjsg2": "volueris", "Vperactsbjsg3": "voluerit", "Vperactsbjpl1": "voluerimus", "Vperactsbjpl2": "volueritis", "Vperactsbjpl3": "voluerint", "Vplpactsbjsg1": "voluissem", "Vplpactsbjsg2": "voluisses", "Vplpactsbjsg3": "voluisset", "Vplpactsbjpl1": "voluissemus", "Vplpactsbjpl2": "voluissetis", "Vplpactsbjpl3": "voluissent",
        "Vpreactinf   ": "velle",
    },
    "nolo": {  # no passives
        "Vpreactindsg1": "nolo", "Vpreactindsg2": "non vis", "Vpreactindsg3": "non vult", "Vpreactindpl1": "nolumus", "Vpreactindpl2": "non vultis", "Vpreactindpl3": "nolunt", "Vimpactindsg1": "nolebam", "Vimpactindsg2": "nolebas", "Vimpactindsg3": "nolebat", "Vimpactindpl1": "nolebamus", "Vimpactindpl2": "nolebatis", "Vimpactindpl3": "nolebant", "Vfutactindsg1": "nolam", "Vfutactindsg2": "noles", "Vfutactindsg3": "nolet", "Vfutactindpl1": "nolemus", "Vfutactindpl2": "noletis", "Vfutactindpl3": "nolent", "Vperactindsg1": "nolui", "Vperactindsg2": "noluisti", "Vperactindsg3": "noluit", "Vperactindpl1": "noluimus", "Vperactindpl2": "noluistis", "Vperactindpl3": "noluerunt", "Vplpactindsg1": "nolueram", "Vplpactindsg2": "nolueras", "Vplpactindsg3": "noluerat", "Vplpactindpl1": "nolueramus", "Vplpactindpl2": "nolueratis", "Vplpactindpl3": "noluerant", "Vfpractindsg1": "noluero", "Vfpractindsg2": "nolueris", "Vfpractindsg3": "noluerit", "Vfpractindpl1": "noluerimus", "Vfpractindpl2": "nolueritis", "Vfpractindpl3": "noluerint",
        "Vpreactsbjsg1": "nelim", "Vpreactsbjsg2": "nelis", "Vpreactsbjsg3": "nelit", "Vpreactsbjpl1": "nelimus", "Vpreactsbjpl2": "nelitis", "Vpreactsbjpl3": "nelint", "Vimpactsbjsg1": "nollem", "Vimpactsbjsg2": "nolles", "Vimpactsbjsg3": "nollet", "Vimpactsbjpl1": "nollemus", "Vimpactsbjpl2": "nolletis", "Vimpactsbjpl3": "nollent", "Vperactsbjsg1": "noluerim", "Vperactsbjsg2": "nolueris", "Vperactsbjsg3": "noluerit", "Vperactsbjpl1": "noluerimus", "Vperactsbjpl2": "nolueritis", "Vperactsbjpl3": "noluerint", "Vplpactsbjsg1": "noluissem", "Vplpactsbjsg2": "noluisses", "Vplpactsbjsg3": "noluisset", "Vplpactsbjpl1": "noluissemus", "Vplpactsbjpl2": "noluissetis", "Vplpactsbjpl3": "noluissent",
        "Vpreactipesg2": "noli", "Vpreactipepl2": "nolite",
        "Vpreactinf   ": "nolle",
    },
    "fero": {
        "Vpreactindsg1": "fero", "Vpreactindsg2": "fers", "Vpreactindsg3": "fert", "Vpreactindpl1": "ferimus", "Vpreactindpl2": "fertis", "Vpreactindpl3": "ferunt", "Vimpactindsg1": "ferebam", "Vimpactindsg2": "ferebas", "Vimpactindsg3": "ferebat", "Vimpactindpl1": "ferebamus", "Vimpactindpl2": "ferebatis", "Vimpactindpl3": "ferebant", "Vfutactindsg1": "feram", "Vfutactindsg2": "feres", "Vfutactindsg3": "feret", "Vfutactindpl1": "feremus", "Vfutactindpl2": "feretis", "Vfutactindpl3": "ferent", "Vperactindsg1": "tuli", "Vperactindsg2": "tulisti", "Vperactindsg3": "tulit", "Vperactindpl1": "tulimus", "Vperactindpl2": "tulistis", "Vperactindpl3": "tulerunt", "Vplpactindsg1": "tuleram", "Vplpactindsg2": "tuleras", "Vplpactindsg3": "tulerat", "Vplpactindpl1": "tuleramus", "Vplpactindpl2": "tuleratis", "Vplpactindpl3": "tulerant", "Vfpractindsg1": "tulero", "Vfpractindsg2": "tuleris", "Vfpractindsg3": "tulerit", "Vfpractindpl1": "tulerimus", "Vfpractindpl2": "tuleritis", "Vfpractindpl3": "tulerint",
        "Vprepasindsg1": "feror", "Vprepasindsg2": "ferris", "Vprepasindsg3": "fertur", "Vprepasindpl1": "ferimur", "Vprepasindpl2": "ferimini", "Vprepasindpl3": "feruntur", "Vimppasindsg1": "ferebar", "Vimppasindsg2": "ferebaris", "Vimppasindsg3": "ferebatur", "Vimppasindpl1": "ferebamur", "Vimppasindpl2": "ferebamini", "Vimppasindpl3": "ferebantur", "Vfutpasindsg1": "ferar", "Vfutpasindsg2": "fereris", "Vfutpasindsg3": "feretur", "Vfutpasindpl1": "feremur", "Vfutpasindpl2": "feremini", "Vfutpasindpl3": "ferentur", "Vperpasindsg1": "latus sum", "Vperpasindsg2": "latus es", "Vperpasindsg3": "latus est", "Vperpasindpl1": "lati sumus", "Vperpasindpl2": "lati estis", "Vperpasindpl3": "lati sunt", "Vplppasindsg1": "latus eram", "Vplppasindsg2": "latus eras", "Vplppasindsg3": "latus erat", "Vplppasindpl1": "lati eramus", "Vplppasindpl2": "lati eratis", "Vplppasindpl3": "lati erant", "Vfprpasindsg1": "latus ero", "Vfprpasindsg2": "latus eris", "Vfprpasindsg3": "latus erit", "Vfprpasindpl1": "lati erimus", "Vfprpasindpl2": "lati eritis", "Vfprpasindpl3": "lati erunt",
        "Vpreactsbjsg1": "feram", "Vpreactsbjsg2": "feras", "Vpreactsbjsg3": "ferat", "Vpreactsbjpl1": "feramus", "Vpreactsbjpl2": "feratis", "Vpreactsbjpl3": "ferant", "Vimpactsbjsg1": "ferrem", "Vimpactsbjsg2": "ferres", "Vimpactsbjsg3": "ferret", "Vimpactsbjpl1": "ferremus", "Vimpactsbjpl2": "ferretis", "Vimpactsbjpl3": "ferrent", "Vperactsbjsg1": "tulerim", "Vperactsbjsg2": "tuleris", "Vperactsbjsg3": "tulerit", "Vperactsbjpl1": "tulerimus", "Vperactsbjpl2": "tuleritis", "Vperactsbjpl3": "tulerint", "Vplpactsbjsg1": "tulissem", "Vplpactsbjsg2": "tulisses", "Vplpactsbjsg3": "tulisset", "Vplpactsbjpl1": "tulissemus", "Vplpactsbjpl2": "tulissetis", "Vplpactsbjpl3": "tulissent",
        "Vpreactipesg2": "fer", "Vpreactipepl2": "ferte",
        "Vpreactinf   ": "ferre", "Vprepasinf   ": "ferri",
    },
    "eo": {
        "Vpreactindsg1": "eo", "Vpreactindsg2": "is", "Vpreactindsg3": "it", "Vpreactindpl1": "imus", "Vpreactindpl2": "itis", "Vpreactindpl3": "eunt", "Vimpactindsg1": "ibam", "Vimpactindsg2": "ibas", "Vimpactindsg3": "ibat", "Vimpactindpl1": "ibamus", "Vimpactindpl2": "ibatis", "Vimpactindpl3": "ibant", "Vfutactindsg1": "ibo", "Vfutactindsg2": "ibis", "Vfutactindsg3": "ibit", "Vfutactindpl1": "ibimus", "Vfutactindpl2": "ibitis", "Vfutactindpl3": "ibunt", "Vperactindsg1": "ii", "Vperactindsg2": "isti", "Vperactindsg3": "iit", "Vperactindpl1": "iimus", "Vperactindpl2": "istis", "Vperactindpl3": "ierunt", "Vplpactindsg1": "ieram", "Vplpactindsg2": "ieras", "Vplpactindsg3": "ierat", "Vplpactindpl1": "ieramus", "Vplpactindpl2": "ieratis", "Vplpactindpl3": "ierant", "Vfpractindsg1": "iero", "Vfpractindsg2": "ieris", "Vfpractindsg3": "ierit", "Vfpractindpl1": "ierimus", "Vfpractindpl2": "ieritis", "Vfpractindpl3": "ierint",
        "Vprepasindsg1": "eor", "Vprepasindsg2": "iris", "Vprepasindsg3": "itur", "Vprepasindpl1": "imur", "Vprepasindpl2": "imini", "Vprepasindpl3": "euntur", "Vimppasindsg1": "ibar", "Vimppasindsg2": "ibaris", "Vimppasindsg3": "ibatur", "Vimppasindpl1": "ibamur", "Vimppasindpl2": "ibamini", "Vimppasindpl3": "ibantur", "Vfutpasindsg1": "ibor", "Vfutpasindsg2": "iberis", "Vfutpasindsg3": "ibitur", "Vfutpasindpl1": "ibimur", "Vfutpasindpl2": "ibimini", "Vfutpasindpl3": "ibuntur", "Vperpasindsg1": "itus sum", "Vperpasindsg2": "itus es", "Vperpasindsg3": "itus est", "Vperpasindpl1": "iti sumus", "Vperpasindpl2": "iti estis", "Vperpasindpl3": "iti sunt", "Vplppasindsg1": "itus eram", "Vplppasindsg2": "itus eras", "Vplppasindsg3": "itus erat", "Vplppasindpl1": "iti eramus", "Vplppasindpl2": "iti eratis", "Vplppasindpl3": "iti erant", "Vfprpasindsg1": "itus ero", "Vfprpasindsg2": "itus eris", "Vfprpasindsg3": "itus erit", "Vfprpasindpl1": "iti erimus", "Vfprpasindpl2": "iti eritis", "Vfprpasindpl3": "iti erunt",
        "Vpreactsbjsg1": "eam", "Vpreactsbjsg2": "eas", "Vpreactsbjsg3": "eat", "Vpreactsbjpl1": "eamus", "Vpreactsbjpl2": "eatis", "Vpreactsbjpl3": "eant", "Vimpactsbjsg1": "irem", "Vimpactsbjsg2": "ires", "Vimpactsbjsg3": "iret", "Vimpactsbjpl1": "iremus", "Vimpactsbjpl2": "iretis", "Vimpactsbjpl3": "irent", "Vperactsbjsg1": "ierim", "Vperactsbjsg2": "ieris", "Vperactsbjsg3": "ierit", "Vperactsbjpl1": "ierimus", "Vperactsbjpl2": "ieritis", "Vperactsbjpl3": "ierint", "Vplpactsbjsg1": "issem", "Vplpactsbjsg2": "isses", "Vplpactsbjsg3": "isset", "Vplpactsbjpl1": "issemus", "Vplpactsbjpl2": "issetis", "Vplpactsbjpl3": "issent",
        "Vpreactipesg2": "i", "Vpreactipepl2": "ite",
        "Vpreactinf   ": "ire", "Vprepasinf   ": "iri",
    },
    "absum": {  # no imperatives, passives
        "Vpreactindsg1": "absum", "Vpreactindsg2": "abes", "Vpreactindsg3": "abest", "Vpreactindpl1": "absumus", "Vpreactindpl2": "abestis", "Vpreactindpl3": "absunt", "Vimpactindsg1": "aberam", "Vimpactindsg2": "aberas", "Vimpactindsg3": "aberat", "Vimpactindpl1": "aberamus", "Vimpactindpl2": "aberatis", "Vimpactindpl3": "aberant", "Vfutactindsg1": "abero", "Vfutactindsg2": "aberis", "Vfutactindsg3": "aberit", "Vfutactindpl1": "aberimus", "Vfutactindpl2": "aberitis", "Vfutactindpl3": "aberunt", "Vperactindsg1": "afui", "Vperactindsg2": "afuisti", "Vperactindsg3": "afuit", "Vperactindpl1": "afuimus", "Vperactindpl2": "afuistis", "Vperactindpl3": "afuerunt", "Vplpactindsg1": "afueram", "Vplpactindsg2": "afueras", "Vplpactindsg3": "afuerat", "Vplpactindpl1": "afueramus", "Vplpactindpl2": "afueratis", "Vplpactindpl3": "afuerant", "Vfpractindsg1": "afuero", "Vfpractindsg2": "afueris", "Vfpractindsg3": "afuerit", "Vfpractindpl1": "afuerimus", "Vfpractindpl2": "afueritis", "Vfpractindpl3": "afuerint",
        "Vpreactsbjsg1": "absim", "Vpreactsbjsg2": "absis", "Vpreactsbjsg3": "absit", "Vpreactsbjpl1": "absimus", "Vpreactsbjpl2": "absitis", "Vpreactsbjpl3": "absint", "Vimpactsbjsg1": "abessem", "Vimpactsbjsg2": "abesses", "Vimpactsbjsg3": "abesset", "Vimpactsbjpl1": "abessemus", "Vimpactsbjpl2": "abessetis", "Vimpactsbjpl3": "abessent", "Vperactsbjsg1": "afuerim", "Vperactsbjsg2": "afueris", "Vperactsbjsg3": "afuerit", "Vperactsbjpl1": "afuerimus", "Vperactsbjpl2": "afueritis", "Vperactsbjpl3": "afuerint", "Vplpactsbjsg1": "afuissem", "Vplpactsbjsg2": "afuisses", "Vplpactsbjsg3": "afuisset", "Vplpactsbjpl1": "afuissemus", "Vplpactsbjpl2": "afuissetis", "Vplpactsbjpl3": "afuissent",
        "Vpreactinf   ": "abesse",
    },
    "adsum": {  # no imperatives, passives
        "Vpreactindsg1": "adsum", "Vpreactindsg2": "ades", "Vpreactindsg3": "adest", "Vpreactindpl1": "adsumus", "Vpreactindpl2": "adestis", "Vpreactindpl3": "adsunt", "Vimpactindsg1": "aderam", "Vimpactindsg2": "aderas", "Vimpactindsg3": "aderat", "Vimpactindpl1": "aderamus", "Vimpactindpl2": "aderatis", "Vimpactindpl3": "aderant", "Vfutactindsg1": "adero", "Vfutactindsg2": "aderis", "Vfutactindsg3": "aderit", "Vfutactindpl1": "aderimus", "Vfutactindpl2": "aderitis", "Vfutactindpl3": "aderunt", "Vperactindsg1": "adfui", "Vperactindsg2": "adfuisti", "Vperactindsg3": "adfuit", "Vperactindpl1": "adfuimus", "Vperactindpl2": "adfuistis", "Vperactindpl3": "adfuerunt", "Vplpactindsg1": "adfueram", "Vplpactindsg2": "adfueras", "Vplpactindsg3": "adfuerat", "Vplpactindpl1": "adfueramus", "Vplpactindpl2": "adfueratis", "Vplpactindpl3": "adfuerant",
        "Vfpractindsg1": "adfuero", "Vfpractindsg2": "adfueris", "Vfpractindsg3": "adfuerit", "Vfpractindpl1": "adfuerimus", "Vfpractindpl2": "adfueritis", "Vfpractindpl3": "adfuerint", "Vpreactsbjsg1": "adsim", "Vpreactsbjsg2": "adsis", "Vpreactsbjsg3": "adsit", "Vpreactsbjpl1": "adsimus", "Vpreactsbjpl2": "adsitis", "Vpreactsbjpl3": "adsint", "Vimpactsbjsg1": "adessem", "Vimpactsbjsg2": "adesses", "Vimpactsbjsg3": "adesset", "Vimpactsbjpl1": "adessemus", "Vimpactsbjpl2": "adessetis", "Vimpactsbjpl3": "adessent", "Vperactsbjsg1": "adfuerim", "Vperactsbjsg2": "adfueris", "Vperactsbjsg3": "adfuerit", "Vperactsbjpl1": "adfuerimus", "Vperactsbjpl2": "adfueritis", "Vperactsbjpl3": "adfuerint", "Vplpactsbjsg1": "adfuissem", "Vplpactsbjsg2": "adfuisses", "Vplpactsbjsg3": "adfuisset", "Vplpactsbjpl1": "adfuissemus", "Vplpactsbjpl2": "adfuissetis", "Vplpactsbjpl3": "adfuissent",
        "Vpreactinf   ": "adesse",
    },
    "inquam": {  # defective conjugation
        "Vpreactindsg1": "inquam", "Vpreactindsg2": "inquis", "Vpreactindsg3": "inquit", "Vpreactindpl1": "inquimus", "Vpreactindpl2": "inquitis", "Vpreactindpl3": "inquint", "Vimpactindsg3": "inquiebat", "Vfutactindsg2": "inquies", "Vfutactindsg3": "inquiet", "Vperactindsg1": "inquii", "Vperactindsg2": "inquisti", "Vperactindsg3": "inquit",
        "Vperactsbjsg3": "inquiat",
        "Vpreactipesg2": "inque",
    },
}  # fmt: skip

VERB_COMBINATIONS = (
    (Tense.PRESENT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.ACTIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PRESENT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PRESENT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PRESENT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PRESENT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PRESENT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PRESENT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.IMPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.IMPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.IMPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.FUTURE, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.FUTURE, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.FUTURE, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.FUTURE, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.FUTURE, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.FUTURE, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.PASSIVE, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 1, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 2, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 3, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 1, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 2, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 3, Number.PLURAL),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 1, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 2, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 3, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 1, Number.PLURAL),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 2, Number.PLURAL),
    (Tense.IMPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 3, Number.PLURAL),
    (Tense.PERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 1, Number.SINGULAR),
    (Tense.PERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 2, Number.SINGULAR),
    (Tense.PERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 3, Number.SINGULAR),
    (Tense.PERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 1, Number.PLURAL),
    (Tense.PERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 2, Number.PLURAL),
    (Tense.PERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 3, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 1, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 2, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 3, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 1, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 2, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE, 3, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.IMPERATIVE, 2, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.IMPERATIVE, 2, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.INFINITIVE, None, None),
    (Tense.PRESENT, Voice.PASSIVE, Mood.INFINITIVE, None, None),
)


class TestVerbConjugation:
    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "celo", "celas", "celat", "celamus", "celatis", "celant",
        "celabam", "celabas", "celabat", "celabamus", "celabatis", "celabant",
        "celabo", "celabis", "celabit", "celabimus", "celabitis", "celabunt",
        "celavi", "celavisti", "celavit", "celavimus", "celavistis", "celaverunt",
        "celaveram", "celaveras", "celaverat", "celaveramus", "celaveratis", "celaverant",
        "celavero", "celaveris", "celaverit", "celaverimus", "celaveritis", "celaverint",

        "celor", "celaris", "celatur", "celamur", "celamini", "celantur",
        "celabar", "celabaris", "celabatur", "celabamur", "celabamini", "celabantur",
        "celabor", "celaberis", "celabitur", "celabimur", "celabimini", "celabuntur",
        "celatus sum", "celatus es", "celatus est", "celati sumus", "celati estis", "celati sunt",
        "celatus eram", "celatus eras", "celatus erat", "celati eramus", "celati eratis", "celati erant",
        "celatus ero", "celatus eris", "celatus erit", "celati erimus", "celati eritis", "celati erunt",

        "celem", "celes", "celet", "celemus", "celetis", "celent",
        "celarem", "celares", "celaret", "celaremus", "celaretis", "celarent",
        "celaverim", "celaveris", "celaverit", "celaverimus", "celaveritis", "celaverint",
        "celavissem", "celavisses", "celavisset", "celavissemus", "celavissetis", "celavissent",

        "cela", "celate",

        "celare", "celari",
    ])])  # fmt: skip
    def test_firstconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "maneo", "manes", "manet", "manemus", "manetis", "manent",
        "manebam", "manebas", "manebat", "manebamus", "manebatis", "manebant",
        "manebo", "manebis", "manebit", "manebimus", "manebitis", "manebunt",
        "mansi", "mansisti", "mansit", "mansimus", "mansistis", "manserunt",
        "manseram", "manseras", "manserat", "manseramus", "manseratis", "manserant",
        "mansero", "manseris", "manserit", "manserimus", "manseritis", "manserint",

        "maneor", "maneris", "manetur", "manemur", "manemini", "manentur",
        "manebar", "manebaris", "manebatur", "manebamur", "manebamini", "manebantur",
        "manebor", "maneberis", "manebitur", "manebimur", "manebimini", "manebuntur",
        "mansus sum", "mansus es", "mansus est", "mansi sumus", "mansi estis", "mansi sunt",
        "mansus eram", "mansus eras", "mansus erat", "mansi eramus", "mansi eratis", "mansi erant",
        "mansus ero", "mansus eris", "mansus erit", "mansi erimus", "mansi eritis", "mansi erunt",

        "maneam", "maneas", "maneat", "maneamus", "maneatis", "maneant",
        "manerem", "maneres", "maneret", "maneremus", "maneretis", "manerent",
        "manserim", "manseris", "manserit", "manserimus", "manseritis", "manserint",
        "mansissem", "mansisses", "mansisset", "mansissemus", "mansissetis", "mansissent",

        "mane", "manete",

        "manere", "maneri",
    ])])  # fmt: skip
    def test_secondconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("maneo", "manere", "mansi", "mansus", meaning="stay")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "desero", "deseris", "deserit", "deserimus", "deseritis", "deserunt",
        "deserebam", "deserebas", "deserebat", "deserebamus", "deserebatis", "deserebant",
        "deseram", "deseres", "deseret", "deseremus", "deseretis", "deserent",
        "deserui", "deseruisti", "deseruit", "deseruimus", "deseruistis", "deseruerunt",
        "deserueram", "deserueras", "deseruerat", "deserueramus", "deserueratis", "deseruerant",
        "deseruero", "deserueris", "deseruerit", "deseruerimus", "deserueritis", "deseruerint",

        "deseror", "desereris", "deseritur", "deserimur", "deserimini", "deseruntur",
        "deserebar", "deserebaris", "deserebatur", "deserebamur", "deserebamini", "deserebantur",
        "deserar", "desereris", "deseretur", "deseremur", "deseremini", "deserentur",
        "desertus sum", "desertus es", "desertus est", "deserti sumus", "deserti estis", "deserti sunt",
        "desertus eram", "desertus eras", "desertus erat", "deserti eramus", "deserti eratis", "deserti erant",
        "desertus ero", "desertus eris", "desertus erit", "deserti erimus", "deserti eritis", "deserti erunt",

        "deseram", "deseras", "deserat", "deseramus", "deseratis", "deserant",
        "desererem", "desereres", "desereret", "desereremus", "desereretis", "desererent",
        "deseruerim", "deserueris", "deseruerit", "deseruerimus", "deserueritis", "deseruerint",
        "deseruissem", "deseruisses", "deseruisset", "deseruissemus", "deseruissetis", "deseruissent",

        "desere", "deserite",

        "deserere", "deseri",
    ])])  # fmt: skip
    def test_thirdconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("desero", "deserere", "deserui", "desertus", meaning="desert")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "capio", "capis", "capit", "capimus", "capitis", "capiunt",
        "capiebam", "capiebas", "capiebat", "capiebamus", "capiebatis", "capiebant",
        "capiam", "capies", "capiet", "capiemus", "capietis", "capient",
        "cepi", "cepisti", "cepit", "cepimus", "cepistis", "ceperunt",
        "ceperam", "ceperas", "ceperat", "ceperamus", "ceperatis", "ceperant",
        "cepero", "ceperis", "ceperit", "ceperimus", "ceperitis", "ceperint",

        "capior", "caperis", "capitur", "capimur", "capimini", "capiuntur",
        "capiebar", "capiebaris", "capiebatur", "capiebamur", "capiebamini", "capiebantur",
        "capiar", "capieris", "capietur", "capiemur", "capiemini", "capientur",
        "captus sum", "captus es", "captus est", "capti sumus", "capti estis", "capti sunt",
        "captus eram", "captus eras", "captus erat", "capti eramus", "capti eratis", "capti erant",
        "captus ero", "captus eris", "captus erit", "capti erimus", "capti eritis", "capti erunt",

        "capiam", "capias", "capiat", "capiamus", "capiatis", "capiant",
        "caperem", "caperes", "caperet", "caperemus", "caperetis", "caperent",
        "ceperim", "ceperis", "ceperit", "ceperimus", "ceperitis", "ceperint",
        "cepissem", "cepisses", "cepisset", "cepissemus", "cepissetis", "cepissent",

        "cape", "capite",

        "capere", "capi",
    ])])  # fmt: skip
    def test_thirdioconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("capio", "capere", "cepi", "captus", meaning="take")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "aperio", "aperis", "aperit", "aperimus", "aperitis", "aperiunt",
        "aperiebam", "aperiebas", "aperiebat", "aperiebamus", "aperiebatis", "aperiebant",
        "aperiam", "aperies", "aperiet", "aperiemus", "aperietis", "aperient",
        "aperui", "aperuisti", "aperuit", "aperuimus", "aperuistis", "aperuerunt",
        "aperueram", "aperueras", "aperuerat", "aperueramus", "aperueratis", "aperuerant",
        "aperuero", "aperueris", "aperuerit", "aperuerimus", "aperueritis", "aperuerint",

        "aperior", "aperiris", "aperitur", "aperimur", "aperimini", "aperiuntur",
        "aperiebar", "aperiebaris", "aperiebatur", "aperiebamur", "aperiebamini", "aperiebantur",
        "aperiar", "aperieris", "aperietur", "aperiemur", "aperiemini", "aperientur",
        "apertus sum", "apertus es", "apertus est", "aperti sumus", "aperti estis", "aperti sunt",
        "apertus eram", "apertus eras", "apertus erat", "aperti eramus", "aperti eratis", "aperti erant",
        "apertus ero", "apertus eris", "apertus erit", "aperti erimus", "aperti eritis", "aperti erunt",

        "aperiam", "aperias", "aperiat", "aperiamus", "aperiatis", "aperiant",
        "aperirem", "aperires", "aperiret", "aperiremus", "aperiretis", "aperirent",
        "aperuerim", "aperueris", "aperuerit", "aperuerimus", "aperueritis", "aperuerint",
        "aperuissem", "aperuisses", "aperuisset", "aperuissemus", "aperuissetis", "aperuissent",

        "aperi", "aperite",

        "aperire", "aperiri",
    ])])  # fmt: skip
    def test_fourthconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("aperio", "aperire", "aperui", "apertus", meaning="open")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "veneo", "venis", "venit", "venimus", "venitis", "veneunt",
        "venibam", "venibas", "venibat", "venibamus", "venibatis", "venibant",
        "venibo", "venibis", "venibit", "venibimus", "venibitis", "venibunt",
        "venii", "venisti", "veniit", "veniimus", "venistis", "venierunt",
        "venieram", "venieras", "venierat", "venieramus", "venieratis", "venierant",
        "veniero", "venieris", "venierit", "venierimus", "venieritis", "venierint",

        "veneor", "veniris", "venitur", "venimur", "venimini", "veneuntur",
        "venibar", "venibaris", "venibatur", "venibamur", "venibamini", "venibantur",
        "venibor", "veniberis", "venibitur", "venibimur", "venibimini", "venibuntur",
        "venitus sum", "venitus es", "venitus est", "veniti sumus", "veniti estis", "veniti sunt",
        "venitus eram", "venitus eras", "venitus erat", "veniti eramus", "veniti eratis", "veniti erant",
        "venitus ero", "venitus eris", "venitus erit", "veniti erimus", "veniti eritis", "veniti erunt",

        "veneam", "veneas", "veneat", "veneamus", "veneatis", "veneant",
        "venirem", "venires", "veniret", "veniremus", "veniretis", "venirent",
        "venierim", "venieris", "venierit", "venierimus", "venieritis", "venierint",
        "venissem", "venisses", "venisset", "venissemus", "venissetis", "venissent",

        "veni", "venite",

        "venire", "veniri",
    ])])  # fmt: skip
    def test_irregularverb_eo(self, tense, voice, mood, person, number, expected):
        word = Verb("veneo", "venire", "venii", "venitus", meaning="be sold")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("word"), IRREGULAR_VERBS.keys())
    def test_irregularverb(self, word):
        pp = {
            "sum": ("sum", "esse", "fui", "futurus"),
            "possum": ("possum", "posse", "potui", None),
            "volo": ("volo", "velle", "volui", "voliturus"),
            "nolo": ("nolo", "nolle", "nolui", None),
            "fero": ("fero", "ferre", "tuli", "latus"),
            "adsum": ("adsum", "adesse", "adfui", None),
            "absum": ("absum", "abesse", "afui", None),
            "eo": ("eo", "ire", "ii", "itus"),
            "inquam": ("inquam", None, None, None),
        }[word]

        assert Verb(pp[0], pp[1], pp[2], pp[3], meaning="placeholder").endings == IRREGULAR_VERBS[word]


# TODO: Rework this to be more like pronouns
class TestIrregularVerbConjugation:
    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "sum", "es", "est", "sumus", "estis", "sunt",
        "eram", "eras", "erat", "eramus", "eratis", "erant",
        "ero", "eris", "erit", "erimus", "eritis", "erunt",
        "fui", "fuisti", "fuit", "fuimus", "fuistis", "fuerunt",
        "fueram", "fueras", "fuerat", "fueramus", "fueratis", "fuerant",
        "fuero", "fueris", "fuerit", "fuerimus", "fueritis", "fuerint",

        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,

        "sim", "sis", "sit", "simus", "sitis", "sint",
        "essem", "esses", "esset", "essemus", "essetis", "essent",
        "fuerim", "fueris", "fuerit", "fuerimus", "fueritis", "fuerint",
        "fuissem", "fuisses", "fuisset", "fuissemus", "fuissetis", "fuissent",

        "es", "este",

        "esse", None,
    ])])  # fmt: skip
    def test_irregular_verb_normal(self, tense, voice, mood, person, number, expected):
        word = Verb("sum", "esse", "fui", "futurus", meaning="be")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "eo", "is", "it", "imus", "itis", "eunt",
        "ibam", "ibas", "ibat", "ibamus", "ibatis", "ibant",
        "ibo", "ibis", "ibit", "ibimus", "ibitis", "ibunt",
        "ii", "isti", "iit", "iimus", "istis", "ierunt",
        "ieram", "ieras", "ierat", "ieramus", "ieratis", "ierant",
        "iero", "ieris", "ierit", "ierimus", "ieritis", "ierint",

        "eor", "iris", "itur", "imur", "imini", "euntur",
        "ibar", "ibaris", "ibatur", "ibamur", "ibamini", "ibantur",
        "ibor", "iberis", "ibitur", "ibimur", "ibimini", "ibuntur",
        "itus sum", "itus es", "itus est", "iti sumus", "iti estis", "iti sunt",
        "itus eram", "itus eras", "itus erat", "iti eramus", "iti eratis", "iti erant",
        "itus ero", "itus eris", "itus erit", "iti erimus", "iti eritis", "iti erunt",

        "eam", "eas", "eat", "eamus", "eatis", "eant",
        "irem", "ires", "iret", "iremus", "iretis", "irent",
        "ierim", "ieris", "ierit", "ierimus", "ieritis", "ierint",
        "issem", "isses", "isset", "issemus", "issetis", "issent",

        "i", "ite",
        "ire", "iri",
    ])])  # fmt: skip
    def test_irregular_verb_normal2(self, tense, voice, mood, person, number, expected):
        word = Verb("eo", "ire", "ii", "itus", meaning="go")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [VERB_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "elego", "elegas", "elegat", "elegamus", "elegatis", "elegant",
        "elegabam", "elegabas", "elegabat", "elegabamus", "elegabatis", "elegabant",
        "elegabo", "elegabis", "elegabit", "elegabimus", "elegabitis", "elegabunt",
        "elegavi", "elegavisti", "elegavit", "elegavimus", "elegavistis", "elegaverunt",
        "elegaveram", "elegaveras", "elegaverat", "elegaveramus", "elegaveratis", "elegaverant",
        "elegavero", "elegaveris", "elegaverit", "elegaverimus", "elegaveritis", "elegaverint",

        "elegor", "elegaris", "elegatur", "elegamur", "elegamini", "elegantur",
        "elegabar", "elegabaris", "elegabatur", "elegabamur", "elegabamini", "elegabantur",
        "elegabor", "elegaberis", "elegabitur", "elegabimur", "elegabimini", "elegabuntur",
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,

        "elegem", "eleges", "eleget", "elegemus", "elegetis", "elegent",
        "elegarem", "elegares", "elegaret", "elegaremus", "elegaretis", "elegarent",
        "elegaverim", "elegaveris", "elegaverit", "elegaverimus", "elegaveritis", "elegaverint",
        "elegavissem", "elegavisses", "elegavisset", "elegavissemus", "elegavissetis", "elegavissent",

        "elega", "elegate",

        "elegare", "elegari",
    ])])  # fmt: skip
    def test_irregular_verb_no_ppp(self, tense, voice, mood, person, number, expected):
        word = Verb("elego", "elegare", "elegavi", meaning="bequeath away")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected


DEPONENT_COMBINATIONS = (
    (Tense.PRESENT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PRESENT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PRESENT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PRESENT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PRESENT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PRESENT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.IMPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.IMPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.IMPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.IMPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.FUTURE, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.FUTURE, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.FUTURE, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.FUTURE, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.FUTURE, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.FUTURE, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.PLUPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.PLUPERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.SINGULAR),
    (Tense.FUTURE_PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 1, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 2, Number.PLURAL),
    (Tense.FUTURE_PERFECT, Voice.DEPONENT, Mood.INDICATIVE, 3, Number.PLURAL),
    (Tense.PRESENT, Voice.DEPONENT, Mood.INFINITIVE, None, None),
)


class TestDeponentConjugation:
    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [DEPONENT_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "conor", "conaris", "conatur", "conamur", "conamini", "conantur",
        "conabar", "conabaris", "conabatur", "conabamur", "conabamini", "conabantur",
        "conabor", "conaberis", "conabitur", "conabimur", "conabimini", "conabuntur",
        "conatus sum", "conatus es", "conatus est", "conati sumus", "conati estis", "conati sunt",
        "conatus eram", "conatus eras", "conatus erat", "conati eramus", "conati eratis", "conati erant",
        "conatus ero", "conatus eris", "conatus erit", "conati erimus", "conati eritis", "conati erunt",
        "conari",
    ])])  # fmt: skip
    def test_firstconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("conor", "conari", "conatus sum", meaning="try")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [DEPONENT_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "vereor", "vereris", "veretur", "veremur", "veremini", "verentur",
        "verebar", "verebaris", "verebatur", "verebamur", "verebamini", "verebantur",
        "verebor", "vereberis", "verebitur", "verebimur", "verebimini", "verebuntur",
        "veritus sum", "veritus es", "veritus est", "veriti sumus", "veriti estis", "veriti sunt",
        "veritus eram", "veritus eras", "veritus erat", "veriti eramus", "veriti eratis", "veriti erant",
        "veritus ero", "veritus eris", "veritus erit", "veriti erimus", "veriti eritis", "veriti erunt",
        "vereri",
    ])])  # fmt: skip
    def test_secondconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("vereor", "vereri", "veritus sum", meaning="fear")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [DEPONENT_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "sequor", "sequeris", "sequitur", "sequimur", "sequimini", "sequuntur",
        "sequebar", "sequebaris", "sequebatur", "sequebamur", "sequebamini", "sequebantur",
        "sequar", "sequeris", "sequetur", "sequemur", "sequemini", "sequentur",
        "secutus sum", "secutus es", "secutus est", "secuti sumus", "secuti estis", "secuti sunt",
        "secutus eram", "secutus eras", "secutus erat", "secuti eramus", "secuti eratis", "secuti erant",
        "secutus ero", "secutus eris", "secutus erit", "secuti erimus", "secuti eritis", "secuti erunt",
        "sequi",
    ])])  # fmt: skip
    def test_thirdconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("sequor", "sequi", "secutus sum", meaning="follow")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [DEPONENT_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "ingredior", "ingrederis", "ingreditur", "ingredimur", "ingredimini", "ingrediuntur",
        "ingrediebar", "ingrediebaris", "ingrediebatur", "ingrediebamur", "ingrediebamini", "ingrediebantur",
        "ingrediar", "ingredieris", "ingredietur", "ingrediemur", "ingrediemini", "ingredientur",
        "ingressus sum", "ingressus es", "ingressus est", "ingressi sumus", "ingressi estis", "ingressi sunt",
        "ingressus eram", "ingressus eras", "ingressus erat", "ingressi eramus", "ingressi eratis", "ingressi erant",
        "ingressus ero", "ingressus eris", "ingressus erit", "ingressi erimus", "ingressi eritis", "ingressi erunt",
        "ingredi",
    ])])  # fmt: skip
    def test_thirdioconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("ingredior", "ingredi", "ingressus sum", meaning="enter")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "person", "number", "expected"), [DEPONENT_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "orior", "oriris", "oritur", "orimur", "orimini", "oriuntur",
        "oriebar", "oriebaris", "oriebatur", "oriebamur", "oriebamini", "oriebantur",
        "oriar", "orieris", "orietur", "oriemur", "oriemini", "orientur",
        "orsus sum", "orsus es", "orsus est", "orsi sumus", "orsi estis", "orsi sunt",
        "orsus eram", "orsus eras", "orsus erat", "orsi eramus", "orsi eratis", "orsi erant",
        "orsus ero", "orsus eris", "orsus erit", "orsi erimus", "orsi eritis", "orsi erunt",
        "oriri",
    ])])  # fmt: skip
    def test_fourthconjugation(self, tense, voice, mood, person, number, expected):
        word = Verb("orior", "oriri", "orsus sum", meaning="rise")
        assert word.get(tense=tense, voice=voice, mood=mood, person=person, number=number) == expected


PARTICIPLE_COMBINATIONS = (
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.VOCATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.GENITIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.DATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ABLATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.NOMINATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.VOCATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.GENITIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.DATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ABLATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.VOCATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.GENITIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.DATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ABLATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.NOMINATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.VOCATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.GENITIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.DATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ABLATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.VOCATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.GENITIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.DATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ABLATIVE, Number.SINGULAR),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.NOMINATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.VOCATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.GENITIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.DATIVE, Number.PLURAL),
    (Tense.PRESENT, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ABLATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.VOCATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.GENITIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.DATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ABLATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.NOMINATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.VOCATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.GENITIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.DATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ABLATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.VOCATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.GENITIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.DATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ABLATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.NOMINATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.VOCATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.GENITIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.DATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ABLATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.VOCATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.GENITIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.DATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ABLATIVE, Number.SINGULAR),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.NOMINATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.VOCATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.GENITIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.DATIVE, Number.PLURAL),
    (Tense.PERFECT, Voice.PASSIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ABLATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.VOCATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.GENITIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.DATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ABLATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.NOMINATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.VOCATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.GENITIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.DATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.MASCULINE, Case.ABLATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.VOCATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.GENITIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.DATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ABLATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.NOMINATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.VOCATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.GENITIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.DATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.FEMININE, Case.ABLATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.NOMINATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.VOCATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ACCUSATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.GENITIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.DATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ABLATIVE, Number.SINGULAR),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.NOMINATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.VOCATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ACCUSATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.GENITIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.DATIVE, Number.PLURAL),
    (Tense.FUTURE, Voice.ACTIVE, Mood.PARTICIPLE, Gender.NEUTER, Case.ABLATIVE, Number.PLURAL),
)


class TestParticipleConjugation:
    @pytest.mark.parametrize(("tense", "voice", "mood", "participle_gender", "participle_case", "number", "expected"), [PARTICIPLE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "portans", "portans", "portantem", "portantis", "portanti", MultipleEndings(regular="portanti", absolute="portante"),
        "portantes", "portantes", "portantes", "portantium", "portantibus", "portantibus",
        "portans", "portans", "portantem", "portantis", "portanti", MultipleEndings(regular="portanti", absolute="portante"),
        "portantes", "portantes", "portantes", "portantium", "portantibus", "portantibus",
        "portans", "portans", "portans", "portantis", "portanti", MultipleEndings(regular="portanti", absolute="portante"),
        "portantia", "portantia", "portantia", "portantium", "portantibus", "portantibus",

        "portatus", "portate", "portatum", "portati", "portato", "portato",
        "portati", "portati", "portatos", "portatorum", "portatis", "portatis",
        "portata", "portata", "portatam", "portatae", "portatae", "portata",
        "portatae", "portatae", "portatas", "portatarum", "portatis", "portatis",
        "portatum", "portatum", "portatum", "portati", "portato", "portato",
        "portata", "portata", "portata", "portatorum", "portatis", "portatis",

        "portaturus", "portature", "portaturum", "portaturi", "portaturo", "portaturo",
        "portaturi", "portaturi", "portaturos", "portaturorum", "portaturis", "portaturis",
        "portatura", "portatura", "portaturam", "portaturae", "portaturae", "portatura",
        "portaturae", "portaturae", "portaturas", "portaturarum", "portaturis", "portaturis",
        "portaturum", "portaturum", "portaturum", "portaturi", "portaturo", "portaturo",
        "portatura", "portatura", "portatura", "portaturorum", "portaturis", "portaturis",
    ])])  # fmt: skip
    def test_participle_firstconjugation(self, tense, voice, mood, participle_gender, participle_case, number, expected):
        word = Verb("porto", "portare", "portavi", "portatus", meaning="carry")
        assert word.get(tense=tense, voice=voice, mood=mood, participle_gender=participle_gender, participle_case=participle_case, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "participle_gender", "participle_case", "number", "expected"), [PARTICIPLE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "docens", "docens", "docentem", "docentis", "docenti", MultipleEndings(regular="docenti", absolute="docente"),
        "docentes", "docentes", "docentes", "docentium", "docentibus", "docentibus",
        "docens", "docens", "docentem", "docentis", "docenti", MultipleEndings(regular="docenti", absolute="docente"),
        "docentes", "docentes", "docentes", "docentium", "docentibus", "docentibus",
        "docens", "docens", "docens", "docentis", "docenti", MultipleEndings(regular="docenti", absolute="docente"),
        "docentia", "docentia", "docentia", "docentium", "docentibus", "docentibus",

        "doctus", "docte", "doctum", "docti", "docto", "docto",
        "docti", "docti", "doctos", "doctorum", "doctis", "doctis",
        "docta", "docta", "doctam", "doctae", "doctae", "docta",
        "doctae", "doctae", "doctas", "doctarum", "doctis", "doctis",
        "doctum", "doctum", "doctum", "docti", "docto", "docto",
        "docta", "docta", "docta", "doctorum", "doctis", "doctis",

        "docturus", "docture", "docturum", "docturi", "docturo", "docturo",
        "docturi", "docturi", "docturos", "docturorum", "docturis", "docturis",
        "doctura", "doctura", "docturam", "docturae", "docturae", "doctura",
        "docturae", "docturae", "docturas", "docturarum", "docturis", "docturis",
        "docturum", "docturum", "docturum", "docturi", "docturo", "docturo",
        "doctura", "doctura", "doctura", "docturorum", "docturis", "docturis",
    ])])  # fmt: skip
    def test_participle_secondconjugation(self, tense, voice, mood, participle_gender, participle_case, number, expected):
        word = Verb("doceo", "docere", "docui", "doctus", meaning="teach")
        assert word.get(tense=tense, voice=voice, mood=mood, participle_gender=participle_gender, participle_case=participle_case, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "participle_gender", "participle_case", "number", "expected"), [PARTICIPLE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "trahens", "trahens", "trahentem", "trahentis", "trahenti", MultipleEndings(regular="trahenti", absolute="trahente"),
        "trahentes", "trahentes", "trahentes", "trahentium", "trahentibus", "trahentibus",
        "trahens", "trahens", "trahentem", "trahentis", "trahenti", MultipleEndings(regular="trahenti", absolute="trahente"),
        "trahentes", "trahentes", "trahentes", "trahentium", "trahentibus", "trahentibus",
        "trahens", "trahens", "trahens", "trahentis", "trahenti", MultipleEndings(regular="trahenti", absolute="trahente"),
        "trahentia", "trahentia", "trahentia", "trahentium", "trahentibus", "trahentibus",

        "tractus", "tracte", "tractum", "tracti", "tracto", "tracto",
        "tracti", "tracti", "tractos", "tractorum", "tractis", "tractis",
        "tracta", "tracta", "tractam", "tractae", "tractae", "tracta",
        "tractae", "tractae", "tractas", "tractarum", "tractis", "tractis",
        "tractum", "tractum", "tractum", "tracti", "tracto", "tracto",
        "tracta", "tracta", "tracta", "tractorum", "tractis", "tractis",

        "tracturus", "tracture", "tracturum", "tracturi", "tracturo", "tracturo",
        "tracturi", "tracturi", "tracturos", "tracturorum", "tracturis", "tracturis",
        "tractura", "tractura", "tracturam", "tracturae", "tracturae", "tractura",
        "tracturae", "tracturae", "tracturas", "tracturarum", "tracturis", "tracturis",
        "tracturum", "tracturum", "tracturum", "tracturi", "tracturo", "tracturo",
        "tractura", "tractura", "tractura", "tracturorum", "tracturis", "tracturis",
    ])])  # fmt: skip
    def test_participle_thirdconjugation(self, tense, voice, mood, participle_gender, participle_case, number, expected):
        word = Verb("traho", "trahere", "traxi", "tractus", meaning="begin")
        assert word.get(tense=tense, voice=voice, mood=mood, participle_gender=participle_gender, participle_case=participle_case, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "participle_gender", "participle_case", "number", "expected"), [PARTICIPLE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "occipiens", "occipiens", "occipientem", "occipientis", "occipienti", MultipleEndings(regular="occipienti", absolute="occipiente"),
        "occipientes", "occipientes", "occipientes", "occipientium", "occipientibus", "occipientibus",
        "occipiens", "occipiens", "occipientem", "occipientis", "occipienti", MultipleEndings(regular="occipienti", absolute="occipiente"),
        "occipientes", "occipientes", "occipientes", "occipientium", "occipientibus", "occipientibus",
        "occipiens", "occipiens", "occipiens", "occipientis", "occipienti", MultipleEndings(regular="occipienti", absolute="occipiente"),
        "occipientia", "occipientia", "occipientia", "occipientium", "occipientibus", "occipientibus",

        "occeptus", "occepte", "occeptum", "occepti", "occepto", "occepto",
        "occepti", "occepti", "occeptos", "occeptorum", "occeptis", "occeptis",
        "occepta", "occepta", "occeptam", "occeptae", "occeptae", "occepta",
        "occeptae", "occeptae", "occeptas", "occeptarum", "occeptis", "occeptis",
        "occeptum", "occeptum", "occeptum", "occepti", "occepto", "occepto",
        "occepta", "occepta", "occepta", "occeptorum", "occeptis", "occeptis",

        "occepturus", "occepture", "occepturum", "occepturi", "occepturo", "occepturo",
        "occepturi", "occepturi", "occepturos", "occepturorum", "occepturis", "occepturis",
        "occeptura", "occeptura", "occepturam", "occepturae", "occepturae", "occeptura",
        "occepturae", "occepturae", "occepturas", "occepturarum", "occepturis", "occepturis",
        "occepturum", "occepturum", "occepturum", "occepturi", "occepturo", "occepturo",
        "occeptura", "occeptura", "occeptura", "occepturorum", "occepturis", "occepturis",
    ])])  # fmt: skip
    def test_participle_mixedconjugation(self, tense, voice, mood, participle_gender, participle_case, number, expected):
        word = Verb("occipio", "occipere", "occepi", "occeptus", meaning="begin")
        assert word.get(tense=tense, voice=voice, mood=mood, participle_gender=participle_gender, participle_case=participle_case, number=number) == expected

    @pytest.mark.parametrize(("tense", "voice", "mood", "participle_gender", "participle_case", "number", "expected"), [PARTICIPLE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "audiens", "audiens", "audientem", "audientis", "audienti", MultipleEndings(regular="audienti", absolute="audiente"),
        "audientes", "audientes", "audientes", "audientium", "audientibus", "audientibus",
        "audiens", "audiens", "audientem", "audientis", "audienti", MultipleEndings(regular="audienti", absolute="audiente"),
        "audientes", "audientes", "audientes", "audientium", "audientibus", "audientibus",
        "audiens", "audiens", "audiens", "audientis", "audienti", MultipleEndings(regular="audienti", absolute="audiente"),
        "audientia", "audientia", "audientia", "audientium", "audientibus", "audientibus",

        "auditus", "audite", "auditum", "auditi", "audito", "audito",
        "auditi", "auditi", "auditos", "auditorum", "auditis", "auditis",
        "audita", "audita", "auditam", "auditae", "auditae", "audita",
        "auditae", "auditae", "auditas", "auditarum", "auditis", "auditis",
        "auditum", "auditum", "auditum", "auditi", "audito", "audito",
        "audita", "audita", "audita", "auditorum", "auditis", "auditis",

        "auditurus", "auditure", "auditurum", "audituri", "audituro", "audituro",
        "audituri", "audituri", "audituros", "auditurorum", "audituris", "audituris",
        "auditura", "auditura", "audituram", "auditurae", "auditurae", "auditura",
        "auditurae", "auditurae", "audituras", "auditurarum", "audituris", "audituris",
        "auditurum", "auditurum", "auditurum", "audituri", "audituro", "audituro",
        "auditura", "auditura", "auditura", "auditurorum", "audituris", "audituris",
    ])])  # fmt: skip
    def test_participle_fourthconjugation(self, tense, voice, mood, participle_gender, participle_case, number, expected):
        word = Verb("audio", "audire", "audivi", "auditus", meaning="hear")
        assert word.get(tense=tense, voice=voice, mood=mood, participle_gender=participle_gender, participle_case=participle_case, number=number) == expected


class TestIrregularParticipleConjugation:
    @pytest.mark.parametrize(("tense", "voice", "mood", "participle_gender", "participle_case", "number", "expected"), [PARTICIPLE_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "elegans", "elegans", "elegantem", "elegantis", "eleganti", MultipleEndings(regular="eleganti", absolute="elegante"),
        "elegantes", "elegantes", "elegantes", "elegantium", "elegantibus", "elegantibus",
        "elegans", "elegans", "elegantem", "elegantis", "eleganti", MultipleEndings(regular="eleganti", absolute="elegante"),
        "elegantes", "elegantes", "elegantes", "elegantium", "elegantibus", "elegantibus",
        "elegans", "elegans", "elegans", "elegantis", "eleganti", MultipleEndings(regular="eleganti", absolute="elegante"),
        "elegantia", "elegantia", "elegantia", "elegantium", "elegantibus", "elegantibus",

        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,

        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
        None, None, None, None, None, None,
    ])])  # fmt: skip
    def test_irregular_participle_no_ppp(self, tense, voice, mood, participle_gender, participle_case, number, expected):
        word = Verb("elego", "elegare", "elegavi", meaning="bequeath away")
        assert word.get(tense=tense, voice=voice, mood=mood, participle_gender=participle_gender, participle_case=participle_case, number=number) == expected
