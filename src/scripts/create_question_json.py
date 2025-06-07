"""Create sample vocab-tuister server outputs to allow go code to be generated."""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Final

from src.core.lego.misc import VocabList
from src.core.lego.reader import _read_vocab_file_internal
from src.core.rogo.rules import CLASS_RULES
from src.server.app import generate_questions_sample_json

if TYPE_CHECKING:
    from collections.abc import Generator

    from src.core.rogo.type_aliases import Settings

QUESTION_TYPE_SETTINGS: Final[tuple[str, ...]] = tuple(CLASS_RULES.keys())

DEFAULT_VOCAB_LIST: Final[StringIO] = StringIO("""
@ Verb
hear: audio, audire, audivi, auditus
take: capio, capere, cepi, captus

@ Noun
girl: puella, puellae, (f)
boy: puer, pueri, (m)
name: nomen, nominis, (n)

@ Adjective
large: ingens, ingentis, (3-1)
happy: laetus, laeta, laetum, (2-1-2)

@ Regular
into: in
from: e

@ Pronoun
this: hic, haec, hoc
that: ille
""")

DEFAULT_SETTINGS: Settings = {
    "exclude-verb-present-active-indicative": False,
    "exclude-verb-imperfect-active-indicative": False,
    "exclude-verb-future-active-indicative": False,
    "exclude-verb-perfect-active-indicative": False,
    "exclude-verb-pluperfect-active-indicative": False,
    "exclude-verb-future-perfect-active-indicative": False,
    "exclude-verb-present-passive-indicative": False,
    "exclude-verb-imperfect-passive-indicative": False,
    "exclude-verb-future-passive-indicative": False,
    "exclude-verb-perfect-passive-indicative": False,
    "exclude-verb-pluperfect-passive-indicative": False,
    "exclude-verb-future-perfect-passive-indicative": False,
    "exclude-verb-present-active-infinitive": False,
    "exclude-verb-present-passive-infinitive": False,
    "exclude-verb-present-active-imperative": False,
    "exclude-verb-present-active-subjunctive": False,
    "exclude-verb-imperfect-active-subjunctive": False,
    "exclude-verb-perfect-active-subjunctive": False,
    "exclude-verb-pluperfect-active-subjunctive": False,
    "exclude-verb-singular": False,
    "exclude-verb-plural": False,
    "exclude-verb-1st-person": False,
    "exclude-verb-2nd-person": False,
    "exclude-verb-3rd-person": False,
    "exclude-participles": False,
    "exclude-participle-present-active": False,
    "exclude-participle-perfect-passive": False,
    "exclude-participle-future-active": False,
    "exclude-participle-masculine": False,
    "exclude-participle-feminine": False,
    "exclude-participle-neuter": False,
    "exclude-participle-nominative": False,
    "exclude-participle-vocative": False,
    "exclude-participle-accusative": False,
    "exclude-participle-genitive": False,
    "exclude-participle-dative": False,
    "exclude-participle-ablative": False,
    "exclude-participle-singular": False,
    "exclude-participle-plural": False,
    "exclude-noun-nominative": False,
    "exclude-noun-vocative": False,
    "exclude-noun-accusative": False,
    "exclude-noun-genitive": False,
    "exclude-noun-dative": False,
    "exclude-noun-ablative": False,
    "exclude-noun-singular": False,
    "exclude-noun-plural": False,
    "exclude-adjective-masculine": False,
    "exclude-adjective-feminine": False,
    "exclude-adjective-neuter": False,
    "exclude-adjective-nominative": False,
    "exclude-adjective-vocative": False,
    "exclude-adjective-accusative": False,
    "exclude-adjective-genitive": False,
    "exclude-adjective-dative": False,
    "exclude-adjective-ablative": False,
    "exclude-adjective-singular": False,
    "exclude-adjective-plural": False,
    "exclude-adjective-positive": False,
    "exclude-adjective-comparative": False,
    "exclude-adjective-superlative": False,
    "exclude-adverbs": False,
    "exclude-adverb-positive": False,
    "exclude-adverb-comparative": False,
    "exclude-adverb-superlative": False,
    "exclude-pronoun-masculine": False,
    "exclude-pronoun-feminine": False,
    "exclude-pronoun-neuter": False,
    "exclude-pronoun-nominative": False,
    "exclude-pronoun-vocative": False,
    "exclude-pronoun-accusative": False,
    "exclude-pronoun-genitive": False,
    "exclude-pronoun-dative": False,
    "exclude-pronoun-ablative": False,
    "exclude-pronoun-singular": False,
    "exclude-pronoun-plural": False,
    "exclude-nouns": False,
    "exclude-verbs": False,
    "exclude-deponents": False,
    "exclude-adjectives": False,
    "exclude-pronouns": False,
    "exclude-regulars": False,
    "exclude-verb-first-conjugation": False,
    "exclude-verb-second-conjugation": False,
    "exclude-verb-third-conjugation": False,
    "exclude-verb-fourth-conjugation": False,
    "exclude-verb-mixed-conjugation": False,
    "exclude-verb-irregular-conjugation": False,
    "exclude-noun-first-declension": False,
    "exclude-noun-second-declension": False,
    "exclude-noun-third-declension": False,
    "exclude-noun-fourth-declension": False,
    "exclude-noun-fifth-declension": False,
    "exclude-noun-irregular-declension": False,
    "exclude-adjective-212-declension": False,
    "exclude-adjective-third-declension": False,
    "english-subjunctives": True,
    "include-typein-engtolat": False,
    "include-typein-lattoeng": False,
    "include-parse": False,
    "include-inflect": False,
    "include-principal-parts": False,
    "include-multiplechoice-engtolat": False,
    "include-multiplechoice-lattoeng": False,
    "number-multiplechoice-options": 3,
}

QUESTION_AMOUNT: Final[int] = 2000  # seems reasonable


def _generate_questions_wrap(
    vocab_list: VocabList, question_amount: int, settings: Settings
) -> Generator[str]:
    for question in generate_questions_sample_json(
        vocab_list=vocab_list,
        question_amount=question_amount,
        settings=settings,
    ):
        question_dict = json.loads(question)
        del question_dict["question_type"]
        question_updated = json.dumps(question_dict)
        yield question_updated


if __name__ == "__main__":
    # Clear output directory
    output_dir = Path(__file__).parent / "json_output/questions"

    if output_dir.exists():
        for delete_file in output_dir.iterdir():
            if delete_file.is_file():
                delete_file.unlink()
    else:
        output_dir.mkdir(parents=True, exist_ok=True)

    # Create sample vocab list
    vocab: VocabList = VocabList(
        _read_vocab_file_internal(DEFAULT_VOCAB_LIST), ""
    )

    # Create json files
    for setting in QUESTION_TYPE_SETTINGS:
        DEFAULT_SETTINGS[setting] = True

        data_generator: Generator[str] = _generate_questions_wrap(
            vocab_list=vocab,
            question_amount=QUESTION_AMOUNT,
            settings=DEFAULT_SETTINGS,
        )
        filename: str = f"{CLASS_RULES[setting].value}_sample.json"
        output_path: Path = Path(
            Path(__file__).parent / "json_output" / "questions" / filename
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)  # needed?

        with output_path.open("w", encoding="utf-8") as output_file:
            for data_str in data_generator:
                output_file.write(data_str + "\n")

        DEFAULT_SETTINGS[setting] = False
