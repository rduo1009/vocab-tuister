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


def setup_tests(monkeypatch, port, vocab_file_info, session_config_info):
    monkeypatch.setattr("src.server.app.vocab_list", None)

    server_url = f"http://127.0.0.1:{port}"

    vocab_file = Path(__file__).parent / "testdata" / f"test-{vocab_file_info}-list.txt"
    vocab_list = vocab_file.read_text(encoding="utf-8")

    session_config_file = Path(__file__).parent / "testdata" / f"test-{session_config_info}-config.json"
    session_config = json.loads(session_config_file.read_text(encoding="utf-8"))

    cli_process = threading.Thread(target=run_cli, args=(port,), daemon=True)
    cli_process.start()

    return server_url, vocab_list, session_config, cli_process


@pytest.mark.integration
def test_cli_normal(snapshot, monkeypatch):
    server_url, vocab_list, session_config, cli_process = setup_tests(monkeypatch, 5500, "regular", "regular")

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


@pytest.mark.integration
def test_cli_error_list(snapshot, monkeypatch):
    server_url, vocab_list, session_config, cli_process = setup_tests(monkeypatch, 5501, "error", "regular")

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


@pytest.mark.integration
def test_cli_error_config(snapshot, monkeypatch):
    server_url, vocab_list, session_config, cli_process = setup_tests(monkeypatch, 5502, "regular", "error")
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
