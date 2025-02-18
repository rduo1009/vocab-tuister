import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import contextlib
import json
import os
import threading
from pathlib import Path
from time import sleep

import pytest
import requests
from src.__main__ import cli


def run_cli(port):
    with contextlib.suppress(KeyboardInterrupt):
        cli(["-v", "-v", "-v", "-p", str(port)])


@pytest.mark.integration
def test_cli_normal(caplog, snapshot, monkeypatch):
    monkeypatch.setattr("src.server.app.vocab_list", None)

    server_url = "http://127.0.0.1:5500"

    vocab_file = Path(__file__).parent / "testdata" / "test-regular-list.txt"
    vocab_list = vocab_file.read_text(encoding="utf-8")

    session_config_file = Path(__file__).parent / "testdata" / "test-regular-config.json"
    session_config = json.loads(session_config_file.read_text(encoding="utf-8"))

    cli_process = threading.Thread(target=run_cli, args=(5500,), daemon=True)
    cli_process.start()

    try:
        sleep(5)

        vocab_response = requests.post(f"{server_url}/send-vocab", data=vocab_list, timeout=5)
        assert vocab_response.status_code == 200
        assert vocab_response.text == snapshot

        session_response = requests.post(f"{server_url}/session", json=session_config, timeout=5)
        assert session_response.status_code == 200
        assert session_response.json() == snapshot

    finally:
        sleep(5)

        cli_process.join(timeout=10)

    assert caplog.text == snapshot


@pytest.mark.integration
def test_cli_error_list(caplog, snapshot, monkeypatch):
    monkeypatch.setattr("src.server.app.vocab_list", None)

    server_url = "http://127.0.0.1:5501"

    vocab_file = Path(__file__).parent / "testdata" / "test-error-list.txt"
    vocab_list = vocab_file.read_text(encoding="utf-8")

    session_config_file = Path(__file__).parent / "testdata" / "test-regular-config.json"
    session_config = json.loads(session_config_file.read_text(encoding="utf-8"))

    cli_process = threading.Thread(target=run_cli, args=(5501,), daemon=True)
    cli_process.start()

    try:
        sleep(5)

        vocab_response = requests.post(f"{server_url}/send-vocab", data=vocab_list, timeout=5)
        assert vocab_response.status_code == 400
        assert vocab_response.text == snapshot

        try:
            session_response = requests.post(f"{server_url}/session", json=session_config, timeout=5)
            session_response.raise_for_status()

            pytest.fail("Expected an error but request succeeded.")

        except requests.exceptions.HTTPError:
            if session_response.status_code == 400:
                assert session_response.status_code == 400
                assert session_response.text == snapshot
            else:
                raise

        except requests.exceptions.RequestException:
            raise

    finally:
        sleep(5)

        cli_process.join(timeout=10)

    assert caplog.text == snapshot


@pytest.mark.integration
def test_cli_error_config(caplog, snapshot, monkeypatch):
    monkeypatch.setattr("src.server.app.vocab_list", None)

    server_url = "http://127.0.0.1:5502"

    vocab_file = Path(__file__).parent / "testdata" / "test-regular-list.txt"
    vocab_list = vocab_file.read_text(encoding="utf-8")

    session_config_file = Path(__file__).parent / "testdata" / "test-error-config.json"
    session_config = json.loads(session_config_file.read_text(encoding="utf-8"))

    cli_process = threading.Thread(target=run_cli, args=(5502,), daemon=True)
    cli_process.start()

    try:
        sleep(5)

        vocab_response = requests.post(f"{server_url}/send-vocab", data=vocab_list, timeout=5)
        assert vocab_response.status_code == 200
        assert vocab_response.text == snapshot

        try:
            session_response = requests.post(f"{server_url}/session", json=session_config, timeout=5)
            session_response.raise_for_status()

            pytest.fail("Expected an error but request succeeded.")

        except requests.exceptions.HTTPError:
            if session_response.status_code == 400:
                assert session_response.status_code == 400
                assert session_response.text == snapshot
            else:
                raise

        except requests.exceptions.RequestException:
            raise

    finally:
        sleep(5)

        cli_process.join(timeout=10)

    assert caplog.text == snapshot
