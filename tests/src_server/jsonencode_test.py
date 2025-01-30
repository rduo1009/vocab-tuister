import os
import sys  # noqa: E401

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import json

from src.core.accido.misc import Case, EndingComponents, Mood, Number, Tense, Voice
from src.core.rogo.question_classes import MultipleChoiceEngToLatQuestion, MultipleChoiceLatToEngQuestion, ParseWordCompToLatQuestion, ParseWordLatToCompQuestion, PrincipalPartsQuestion, TypeInEngToLatQuestion, TypeInLatToEngQuestion
from src.server.json_encode import QuestionClassEncoder


def test_encode_multiplechoice_engtolat():
    assert json.dumps(MultipleChoiceEngToLatQuestion(answer="hic", prompt="this", choices=("agricola", "puella", "hic")), cls=QuestionClassEncoder, sort_keys=True) == '{"answer": "hic", "choices": ["agricola", "puella", "hic"], "prompt": "this", "question_type": "MultipleChoiceEngToLatQuestion"}'


def test_encode_multiplechoice_lattoeng():
    assert json.dumps(MultipleChoiceLatToEngQuestion(answer="boy", prompt="puer", choices=("light", "from", "boy")), cls=QuestionClassEncoder, sort_keys=True) == '{"answer": "boy", "choices": ["light", "from", "boy"], "prompt": "puer", "question_type": "MultipleChoiceLatToEngQuestion"}'


def test_encode_parseword_compttolat():
    assert (
        json.dumps(ParseWordCompToLatQuestion(prompt="name: nomen, nominis, (n)", components=EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, string="nominative singular"), main_answer="nomen", answers={"nomen"}), cls=QuestionClassEncoder, sort_keys=True)
        == '{"answers": ["nomen"], "components": "nominative singular", "main_answer": "nomen", "prompt": "name: nomen, nominis, (n)", "question_type": "ParseWordCompToLatQuestion"}'
    )


def test_encode_parseword_lattocomp():
    components = EndingComponents(tense=Tense.PERFECT, voice=Voice.ACTIVE, mood=Mood.INDICATIVE, number=Number.SINGULAR, person=3, string="perfect active indicative singular 3rd person")
    assert (
        json.dumps(ParseWordLatToCompQuestion(prompt="cepit", dictionary_entry="take: capio, capere, cepi", main_answer=components, answers={components}), cls=QuestionClassEncoder, sort_keys=True)
        == '{"answers": ["perfect active indicative singular 3rd person"], "dictionary_entry": "take: capio, capere, cepi", "main_answer": "perfect active indicative singular 3rd person", "prompt": "cepit", "question_type": "ParseWordLatToCompQuestion"}'
    )


def test_encode_principalparts():
    assert json.dumps(PrincipalPartsQuestion(prompt="capio", principal_parts=("capio", "capere", "cepi", "captus")), cls=QuestionClassEncoder, sort_keys=True) == '{"principal_parts": ["capio", "capere", "cepi", "captus"], "prompt": "capio", "question_type": "PrincipalPartsQuestion"}'


def test_encode_typein_engtolat():
    assert json.dumps(TypeInEngToLatQuestion(prompt="house", main_answer="domus", answers={"domus", "villa"}), cls=QuestionClassEncoder, sort_keys=True) in {
        '{"answers": ["domus", "villa"], "main_answer": "domus", "prompt": "house", "question_type": "TypeInEngToLatQuestion"}',
        '{"answers": ["villa", "domus"], "main_answer": "domus", "prompt": "house", "question_type": "TypeInEngToLatQuestion"}',
    }


def test_encode_typein_lattoeng():
    assert json.dumps(TypeInLatToEngQuestion(prompt="domus", main_answer="house", answers={"house", "home"}), cls=QuestionClassEncoder, sort_keys=True) in {
        '{"answers": ["house", "home"], "main_answer": "house", "prompt": "domus", "question_type": "TypeInLatToEngQuestion"}',
        '{"answers": ["home", "house"], "main_answer": "house", "prompt": "domus", "question_type": "TypeInLatToEngQuestion"}',
    }


def test_encode_not_available():
    assert json.dumps(("test", "test"), cls=QuestionClassEncoder, sort_keys=True) == '["test", "test"]'
