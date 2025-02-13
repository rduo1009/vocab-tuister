# ruff: noqa: S404, S607, S603

import json
import os
import signal
import subprocess
import time
from pathlib import Path

import pytest
import requests

SERVER_URL = "http://127.0.0.1:5500"

VOCAB_FILE = Path(__file__).parent / "testdata" / "test-list.txt"
VOCAB_LIST = VOCAB_FILE.read_text(encoding="utf-8")

SESSION_CONFIG_FILE = Path(__file__).parent / "testdata" / "test-config.json"
SESSION_CONFIG = json.loads(SESSION_CONFIG_FILE.read_text(encoding="utf-8"))

os.environ["VOCAB_TUISTER_RANDOM_SEED"] = "10"


def _wait_for_server(url, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)  # noqa: S113
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            pass
        time.sleep(0.5)
    return False


@pytest.fixture
def server_process():
    process = subprocess.Popen(["python3", "-m", "src", "-v", "-v", "-v", "-p", "5500"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        assert _wait_for_server(SERVER_URL), "Server did not start in time"
        yield process
    finally:
        process.send_signal(signal.SIGINT)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

        assert process.returncode == 0, "Server did not terminate cleanly"


def _remove_first_n_chars(text: str, n: int) -> str:
    return "\n".join(line[n:] for line in text.splitlines())


def test_cli_normal(server_process, snapshot):
    vocab_response = requests.post(f"{SERVER_URL}/send-vocab", data=VOCAB_LIST, timeout=5)
    assert vocab_response.status_code == 200
    assert vocab_response.text == snapshot

    session_response = requests.post(f"{SERVER_URL}/session", json=SESSION_CONFIG, timeout=5)
    assert session_response.status_code == 200
    assert session_response.json() == snapshot

    server_process.send_signal(signal.SIGINT)
    stdout = server_process.communicate(timeout=5)[0]
    stdout = _remove_first_n_chars(stdout, n=21)
    assert stdout == snapshot
