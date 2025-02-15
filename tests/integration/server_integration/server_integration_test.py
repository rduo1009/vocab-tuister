import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import json
import os
import threading
from pathlib import Path
from time import sleep

import pytest
import requests
from src.__main__ import cli

SERVER_URL = "http://127.0.0.1:5500"

VOCAB_FILE = Path(__file__).parent / "testdata" / "test-list.txt"
VOCAB_LIST = VOCAB_FILE.read_text(encoding="utf-8")

SESSION_CONFIG_FILE = Path(__file__).parent / "testdata" / "test-config.json"
SESSION_CONFIG = json.loads(SESSION_CONFIG_FILE.read_text(encoding="utf-8"))


def _remove_first_n_chars(text: str, n: int) -> str:
    return "\n".join(line[n:] for line in text.splitlines())


def _run_cli():
    cli(["-v", "-v", "-v", "-p", "5500"])


@pytest.mark.integration
def test_cli_normal(caplog, snapshot):
    cli_process = threading.Thread(target=_run_cli, daemon=True)
    cli_process.start()

    try:
        sleep(5)

        vocab_response = requests.post(f"{SERVER_URL}/send-vocab", data=VOCAB_LIST, timeout=5)
        assert vocab_response.status_code == 200
        assert vocab_response.text == snapshot

        session_response = requests.post(f"{SERVER_URL}/session", json=SESSION_CONFIG, timeout=5)
        assert session_response.status_code == 200
        assert session_response.json() == snapshot

    finally:
        sleep(5)

        shutdown_response = requests.get(f"{SERVER_URL}/shutdown", timeout=5)
        assert shutdown_response.status_code == 200
        assert shutdown_response.text == snapshot

    assert caplog.text == snapshot
