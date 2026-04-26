# pyright: reportUnknownParameterType=false, reportUnknownArgumentType=false, reportMissingParameterType=false

from src.core.transfero.words import adj_to_adv


def test_adjtoadv():
    assert adj_to_adv("happy") == "happily"
    assert adj_to_adv("great") == "greatly"
    assert adj_to_adv("monotonous") == "monotonously"


def test_adjtoadv_fallback():
    assert adj_to_adv("spiny") == "spinily"
    assert adj_to_adv("basic") == "basically"
    assert adj_to_adv("belittle") == "belittly"
    assert adj_to_adv("house") == "housely"
