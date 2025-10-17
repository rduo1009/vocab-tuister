"""The Flask API that sends questions to the client."""

# ruff: noqa: D103, PLW0603

import json
import logging
import traceback
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, cast

from flask import Flask, jsonify, render_template, request
from platformdirs import PlatformDirs
from pydantic import ValidationError
from waitress import serve
from werkzeug.exceptions import BadRequest, InternalServerError

from ..core.lego.cache import cache_vocab_file
from ..core.rogo.asker import ask_question_without_sr
from ..core.rogo.type_aliases import SessionConfig, Settings
from ..core.transfero.synonyms import setup_wn
from ._json_encode import QuestionClassEncoder
from .exceptions import InvalidSettingsError

if TYPE_CHECKING:
    from ..core.lego.misc import VocabList

logger = logging.getLogger(__name__)

dirs = PlatformDirs("vocab-tuister", "rduo1009")
app = Flask(__name__)
vocab_list: VocabList | None = None
settings: Settings | None = None


@app.errorhandler(InternalServerError)
def handle_internal_server_error(e: InternalServerError):
    original_e = e.original_exception

    if original_e is None:
        logger.error("%s", e)
        return "500 Internal Server Error", 500

    tb = "".join(
        traceback.format_exception(
            type(original_e), original_e, original_e.__traceback__
        )
    )
    logger.error("%s", tb)

    return f"500 Internal Server Error: {original_e}", 500


def _get_settings() -> Settings:
    settings_file = Path(dirs.user_config_path) / "settings.json"
    try:
        return Settings.model_validate_json(settings_file.read_text())
    except FileNotFoundError as e:
        raise InvalidSettingsError(
            f"Settings file not found at {settings_file}."
        ) from e
    except ValidationError as e:
        raise InvalidSettingsError(f"Invalid settings: {e}") from e


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
    payload = request.get_json()
    question_amount = payload["number-of-questions"]
    session_config = payload["config"]

    if not isinstance(question_amount, int):
        logger.error(
            "Invalid session config: 'number-of-questions' must be an "
            "integer (got type %s).",
            type(question_amount).__name__,
        )
        return {
            "error": "InvalidSessionConfigError",
            "details": None,
        }, 400  # TODO: do this

    try:
        session_config = SessionConfig.model_validate(session_config)
    except ValidationError as e:
        logger.exception("Invalid session config.")
        return {"error": "InvalidSessionConfigError", "details": e.json()}, 400

    logger.info("Returning %d questions.", question_amount)
    return jsonify(
        _generate_questions_json(vocab_list, question_amount, session_config)
    )


def main_dev(port: int, *, debug: bool = False):
    global settings
    settings = _get_settings()
    if settings.include_synonyms:
        setup_wn()
    app.run(host="127.0.0.1", port=port, debug=debug)


def main(port: int):
    global settings
    settings = _get_settings()
    if settings.include_synonyms:
        setup_wn()
    serve(app, host="127.0.0.1", port=port)
