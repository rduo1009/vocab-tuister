def getInflection(
    lemma: str, tag: str, inflect_oov: bool = True
) -> tuple[str, ...]: ...
def getLemma(
    word: str, upos: str, lemmatize_oov: bool = True
) -> tuple[str, ...]: ...
