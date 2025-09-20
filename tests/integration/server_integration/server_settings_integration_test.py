# pyright: basic
# pyright: reportUnknownParameterType=false, reportUnknownArgumentType=false, reportMissingParameterType=false

import contextlib
import threading
import time
from pathlib import Path

import pytest
from src.__main__ import cli
from src.server.exceptions import InvalidSettingsError


def run_cli(port):
    with contextlib.suppress(KeyboardInterrupt):
        cli(["-v", "-v", "-v", "-p", str(port)])


def setup_tests(monkeypatch, port, settings_info):
    class _Dirs:
        user_config_path = Path(__file__).parent / "testdata" / f"test-{settings_info}-settings"
        user_cache_path = Path(__file__).parent / "testdata" / "cache"

    monkeypatch.setattr("src.server.app.vocab_list", None)
    monkeypatch.setattr("src.server.app.dirs", _Dirs)

    run_cli(port)


@pytest.mark.integration
def test_cli_normal_settings(monkeypatch):
    thread = threading.Thread(target=lambda: setup_tests(monkeypatch, 5510, "regular"), daemon=True)
    thread.start()

    time.sleep(2)


@pytest.mark.integration
def test_cli_error_missing_settings(snapshot, monkeypatch):
    with pytest.raises(InvalidSettingsError) as error:
        setup_tests(monkeypatch, 5511, "errormissing")
    assert str(error.value) == snapshot


@pytest.mark.integration
def test_cli_error_extra_settings(snapshot, monkeypatch):
    with pytest.raises(InvalidSettingsError) as error:
        setup_tests(monkeypatch, 5512, "errorextra")
    assert str(error.value) == snapshot


@pytest.mark.integration
def test_cli_error_type_settings(snapshot, monkeypatch):
    with pytest.raises(InvalidSettingsError) as error:
        setup_tests(monkeypatch, 5513, "errortype")
    assert str(error.value) == snapshot
