# pyright: basic
# pyright: reportUnknownParameterType=false, reportUnknownArgumentType=false, reportMissingParameterType=false

import asyncio
import json
from pathlib import Path

import pytest
from grpclib import GRPCError
from src.core.rogo.type_aliases import Settings
from src.pb.vocab_tuister.v1 import CreateSessionRequest, SessionConfig, VerifyConfigRequest, VerifyVocabRequest
from src.server.app import VocabTesterService, run


@pytest.fixture
def setup_tests(monkeypatch):
    async def _setup(port, vocab_file_info, session_config_info):
        class _Dirs:
            user_config_path = Path(__file__).parent / "testdata"
            user_cache_path = Path(__file__).parent / "testdata" / "cache"

        monkeypatch.setattr("src.server.app.dirs", _Dirs)
        monkeypatch.setattr("src.server.app.settings", Settings.model_validate_json((Path(_Dirs.user_config_path) / "settings.json").read_text()))

        server_url = f"127.0.0.1:{port}"

        vocab_file = Path(__file__).parent / "testdata" / f"test-{vocab_file_info}-list.txt"
        vocab_text = vocab_file.read_text(encoding="utf-8")

        session_config_file = Path(__file__).parent / "testdata" / f"test-{session_config_info}-config.json"
        session_config_dict = json.loads(session_config_file.read_text(encoding="utf-8"))
        session_config = SessionConfig.from_dict(session_config_dict)

        task = asyncio.create_task(run(port))
        await asyncio.sleep(0.2)

        return server_url, vocab_text, session_config, task

    return _setup


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cli_normal(snapshot, setup_tests):
    _, vocab_text, session_config, server = await setup_tests(5600, "regular", "regular")

    client = VocabTesterService()

    vocab_response = await client.verify_vocab(VerifyVocabRequest(vocab_text=vocab_text))
    assert vocab_response.to_dict() == snapshot

    config_response = await client.verify_config(VerifyConfigRequest(number_of_questions=50, session_config=session_config))
    assert config_response.to_dict() == snapshot

    stream = client.create_session(CreateSessionRequest(vocab_list=vocab_text, number_of_questions=50, session_config=session_config))

    session_response = [msg.to_dict() async for msg in stream]
    assert session_response == snapshot

    server.cancel()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cli_error_list(snapshot, setup_tests):
    _, vocab_text, _, server = await setup_tests(5601, "error", "regular")

    client = VocabTesterService()

    with pytest.raises(GRPCError) as exc_info:
        await client.verify_vocab(VerifyVocabRequest(vocab_text=vocab_text))

    assert exc_info.value == snapshot

    server.cancel()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cli_error_numberquestions1_config(snapshot, setup_tests):
    _, _, session_config, server = await setup_tests(5600, "regular", "regular")

    client = VocabTesterService()

    with pytest.raises(GRPCError) as exc_info:
        await client.verify_config(VerifyConfigRequest(number_of_questions=-1, session_config=session_config))

    assert exc_info.value == snapshot

    server.cancel()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cli_error_numberquestions2_config(snapshot, setup_tests):
    _, vocab_text, session_config, server = await setup_tests(5600, "regular", "regular")

    client = VocabTesterService()
    stream = client.create_session(CreateSessionRequest(vocab_list=vocab_text, number_of_questions=-1, session_config=session_config))

    with pytest.raises(GRPCError) as exc_info:
        [msg.to_dict() async for msg in stream]

    assert exc_info.value == snapshot

    server.cancel()
