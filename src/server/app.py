"""The Flask API that sends questions to the client."""

# ruff: noqa: D103, PLW0603

from __future__ import annotations

import json
import logging
import traceback
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from flask import Flask, Response, render_template, request
from platformdirs import PlatformDirs
from waitress import serve
from werkzeug.exceptions import BadRequest

from ..core.lego.cache import cache_vocab_file
from ..core.rogo.asker import ask_question_without_sr
from ..core.rogo.type_aliases import SessionConfig, Settings
from ..utils.typeddict_validator import (
    DictExtraKeyError,
    DictIncorrectTypeError,
    DictMissingKeyError,
    validate_typeddict,
)
from ._json_encode import QuestionClassEncoder

if TYPE_CHECKING:
    from ..core.lego.misc import VocabList

logger = logging.getLogger(__name__)

dirs = PlatformDirs("vocab-tuister", "rduo1009")
app = Flask(__name__)
vocab_list: VocabList | None = None
settings: Settings | None = None


@app.errorhandler(BadRequest)
def handle_bad_request(e: BadRequest) -> tuple[str, int]:
    logger.error(
        "%s\n%s",
        e.description,
        "\n".join(traceback.format_tb(e.__traceback__)),
    )
    return f"Bad request: {e}", 400


def _get_settings() -> Settings:
    settings_file = Path(dirs.user_config_path) / "settings.json"

    try:
        with settings_file.open("r", encoding="utf-8") as f:
            raw_settings = json.load(f)
    except FileNotFoundError as e:
        raise BadRequest(
            f"Settings file not found at {settings_file}. (InvalidSettingsError)"
        ) from e

    try:
        _ = validate_typeddict(raw_settings, Settings)

    except DictMissingKeyError as e:
        keys_str = ", ".join(f"'{k}'" for k in sorted(e.missing_keys))
        raise BadRequest(
            f"Required settings are missing: {keys_str}. (InvalidSessionConfigError)"
        ) from e

    except DictExtraKeyError as e:
        keys_str = ", ".join(f"'{k}'" for k in sorted(e.extra_keys))
        raise BadRequest(
            f"Unrecognised settings were provided: {keys_str}. (InvalidSessionConfigError)"
        ) from e

    return raw_settings


@app.route("/")
def info():
    return render_template(
        "index.html.jinja",
        vocab_list=(str(vocab) for vocab in vocab_list.vocab)
        if vocab_list
        else None,
        vocab_list_raw=str(vocab_list),
    )


@app.route("/send-vocab", methods=["POST"])
def send_vocab():
    global vocab_list

    try:
        logger.info("Reading vocab file.")
        vocab_list_text = StringIO(request.get_data().decode("utf-8"))
        # TODO: Allow user to customise whether to compress in settings
        vocab_list, _ = cache_vocab_file(
            vocab_list_text, dirs.user_cache_path, compress=True
        )
    except Exception as e:
        raise BadRequest(f"{type(e).__name__}: {e}").with_traceback(
            e.__traceback__
        ) from e

    return "Vocab file received."


def _generate_questions_json(
    vocab_list: VocabList, question_amount: int, session_config: SessionConfig
) -> str:
    def _rearrange[T](d: dict[str, T]) -> dict[str, str | dict[str, T]]:
        question_type = cast("str", d.pop("question_type"))
        return {"question_type": question_type, question_type: d}

    assert settings is not None
    json_list = [
        _rearrange(json.loads(json.dumps(question, cls=QuestionClassEncoder)))
        for question in ask_question_without_sr(
            vocab_list, question_amount, session_config, settings
        )
    ]
    return json.dumps(json_list)


@app.route("/session", methods=["POST"])
def create_session():
    if not vocab_list:
        raise BadRequest("Vocab file has not been provided.")

    logger.info("Validating settings.")
    session_config: dict[str, Any] = request.get_json()
    try:
        question_amount = session_config.pop("number-of-questions")
    except KeyError as e:
        raise BadRequest(
            "Required config is missing: 'number-of-questions'. "
            "(InvalidSessionConfigError)"
        ) from e

    if not isinstance(question_amount, int):
        raise BadRequest(
            "Invalid session config: 'number-of-questions' must be "
            f"an integer (got type {type(question_amount).__name__}). "
            "(InvalidSessionConfigError)"
        )

    try:
        _ = validate_typeddict(session_config, SessionConfig)
    except DictMissingKeyError as e:
        keys_str = ", ".join(f"'{k}'" for k in sorted(e.missing_keys))
        raise BadRequest(
            f"Required config is missing: {keys_str}. (InvalidSessionConfigError)"
        ) from e

    except DictExtraKeyError as e:
        keys_str = ", ".join(f"'{k}'" for k in sorted(e.extra_keys))
        raise BadRequest(
            f"Unrecognised config was provided: {keys_str}. "
            "(InvalidSessionConfigError)"
        ) from e

    except DictIncorrectTypeError as e:
        type_error_details: list[str] = []
        for field, detail in sorted(e.incorrect_types.items()):
            expected_type_str = str(detail.expected)
            actual_type_str = (
                detail.actual.__name__
                if hasattr(detail.actual, "__name__")
                else str(detail.actual)
            )
            type_error_details.append(
                f"Expected type {expected_type_str} for '{field}', but received"
                f" type {actual_type_str}"
            )
        raise BadRequest(
            f"{'; '.join(type_error_details)}. (InvalidSessionConfigError)"
        ) from e

    logger.info("Returning %d questions.", question_amount)
    try:
        return Response(
            _generate_questions_json(
                vocab_list,
                question_amount,
                cast("SessionConfig", session_config),  # pyright: ignore[reportInvalidCast]
            ),
            mimetype="application/json",
        )
    except Exception as e:
        raise BadRequest(f"{type(e).__name__}: {e}").with_traceback(
            e.__traceback__
        ) from e


def main_dev(port: int, *, debug: bool = False):
    global settings
    settings = _get_settings()
    app.run(host="127.0.0.1", port=port, debug=debug)


def main(port: int):
    global settings
    settings = _get_settings()
    serve(app, host="127.0.0.1", port=port)
