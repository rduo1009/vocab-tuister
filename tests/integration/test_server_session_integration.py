# pyright: basic
# pyright: reportUnknownParameterType=false, reportUnknownArgumentType=false, reportMissingParameterType=false

import json
from pathlib import Path

import pytest
from src.core.rogo.type_aliases import Settings
from src.server.app import app


def setup_tests(monkeypatch, port, vocab_file_info, session_config_info):
    class _Dirs:
        user_config_path = Path(__file__).parent / "testdata"
        user_cache_path = Path(__file__).parent / "testdata" / "cache"

    monkeypatch.setattr("src.server.app.vocab_list", None)
    monkeypatch.setattr("src.server.app.dirs", _Dirs)
    monkeypatch.setattr("src.server.app.settings", Settings.model_validate_json((Path(_Dirs.user_config_path) / "settings.json").read_text()))

    server_url = f"http://127.0.0.1:{port}"

    vocab_file = Path(__file__).parent / "testdata" / f"test-{vocab_file_info}-list.txt"
    vocab_list = vocab_file.read_text(encoding="utf-8")

    session_config_file = Path(__file__).parent / "testdata" / f"test-{session_config_info}-config.json"
    session_config = json.loads(session_config_file.read_text(encoding="utf-8"))

    app_test = app.test_client()
    return server_url, vocab_list, session_config, app_test


@pytest.mark.integration
def test_cli_normal(snapshot, monkeypatch):
    server_url, vocab_list, session_config, app_test = setup_tests(monkeypatch, 5600, "regular", "regular")

    vocab_response = app_test.post(f"{server_url}/send-vocab", data=vocab_list)
    assert vocab_response.status_code == 200
    assert vocab_response.text == snapshot

    config_response = app_test.post(f"{server_url}/send-config", json=session_config)
    assert config_response.status_code == 200
    assert config_response.text == snapshot

    session_response = app_test.get(f"{server_url}/session")
    assert session_response.status_code == 200
    assert session_response.json == snapshot


@pytest.mark.integration
def test_cli_error_list(snapshot, monkeypatch):
    server_url, vocab_list, session_config, app_test = setup_tests(monkeypatch, 5601, "error", "regular")

    vocab_response = app_test.post(f"{server_url}/send-vocab", data=vocab_list)
    assert vocab_response.status_code == 400
    assert vocab_response.json == snapshot

    config_response = app_test.post(f"{server_url}/send-config", json=session_config)
    assert config_response.status_code == 200
    assert config_response.text == snapshot

    session_response = app_test.get(f"{server_url}/session")
    assert session_response.status_code == 500
    assert session_response.get_data(as_text=True) == snapshot


@pytest.mark.integration
def test_cli_error_missing1_config(snapshot, monkeypatch):
    server_url, vocab_list, session_config, app_test = setup_tests(monkeypatch, 5602, "regular", "errormissing1")

    vocab_response = app_test.post(f"{server_url}/send-vocab", data=vocab_list)
    assert vocab_response.status_code == 200
    assert vocab_response.text == snapshot

    config_response = app_test.post(f"{server_url}/send-config", json=session_config)
    assert config_response.status_code == 400
    assert config_response.get_data(as_text=True) == snapshot


@pytest.mark.integration
def test_cli_error_missing2_config(snapshot, monkeypatch):
    server_url, vocab_list, session_config, app_test = setup_tests(monkeypatch, 5603, "regular", "errormissing2")

    vocab_response = app_test.post(f"{server_url}/send-vocab", data=vocab_list)
    assert vocab_response.status_code == 200
    assert vocab_response.text == snapshot

    config_response = app_test.post(f"{server_url}/send-config", json=session_config)
    assert config_response.status_code == 400
    assert config_response.get_data(as_text=True) == snapshot


@pytest.mark.integration
def test_cli_error_extra_config(snapshot, monkeypatch):
    server_url, vocab_list, session_config, app_test = setup_tests(monkeypatch, 5604, "regular", "errorextra")

    vocab_response = app_test.post(f"{server_url}/send-vocab", data=vocab_list)
    assert vocab_response.status_code == 200
    assert vocab_response.text == snapshot

    config_response = app_test.post(f"{server_url}/send-config", json=session_config)
    assert config_response.status_code == 400
    assert config_response.get_data(as_text=True) == snapshot


@pytest.mark.integration
def test_cli_error_type1_config(snapshot, monkeypatch):
    server_url, vocab_list, session_config, app_test = setup_tests(monkeypatch, 5605, "regular", "errortype1")

    vocab_response = app_test.post(f"{server_url}/send-vocab", data=vocab_list)
    assert vocab_response.status_code == 200
    assert vocab_response.text == snapshot

    config_response = app_test.post(f"{server_url}/send-config", json=session_config)
    assert config_response.status_code == 400
    assert config_response.get_data(as_text=True) == snapshot


@pytest.mark.integration
def test_cli_error_type2_config(snapshot, monkeypatch):
    server_url, vocab_list, session_config, app_test = setup_tests(monkeypatch, 5606, "regular", "errortype2")

    vocab_response = app_test.post(f"{server_url}/send-vocab", data=vocab_list)
    assert vocab_response.status_code == 200
    assert vocab_response.text == snapshot

    config_response = app_test.post(f"{server_url}/send-config", json=session_config)
    assert config_response.status_code == 400
    assert config_response.get_data(as_text=True) == snapshot
