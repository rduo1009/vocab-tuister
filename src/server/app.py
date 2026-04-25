"""The Flask API that sends questions to the client."""

# ruff: noqa: D103, PLW0603

import json
import logging
import traceback
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

from flask import Flask, jsonify, request
from platformdirs import PlatformDirs
from pydantic import ValidationError
from waitress import serve
from werkzeug.exceptions import InternalServerError

from ..core.lego.cache import cache_vocab_file
from ..core.lego.exceptions import InvalidVocabFileFormatError
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
question_amount: int | None = None
session_config: SessionConfig | None = None
settings: Settings | None = None


class ErrorResponse(TypedDict):
    """Error returned to the TUI.

    Note that the TUI will need to handle `details` differently depending on
    the value of `error`.
    """

    error: str
    message: str
    details: str


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
    except FileNotFoundError as e:  # these should be fatal errors
        raise InvalidSettingsError(
            f"Settings file not found at {settings_file}."
        ) from e
    except ValidationError as e:
        raise InvalidSettingsError(f"Invalid settings: {e}") from e


@app.route("/health", methods=["GET"])
def health():
    return "OK", 200


@app.route("/send-vocab", methods=["POST"])
def send_vocab():
    global vocab_list

    logger.info("Reading vocab file.")
    vocab_list_text = StringIO(request.get_data().decode("utf-8"))
    try:
        assert settings is not None
        vocab_list, _ = cache_vocab_file(
            vocab_list_text,
            cache_folder=dirs.user_cache_path,
            compress=settings.cache_vocab_lists,
        )
    except InvalidVocabFileFormatError as e:
        logger.exception("Invalid vocab file format.")
        return ErrorResponse(
            error="InvalidVocabFileFormatError",
            message=f"{e.message} (error on line {e.line_number})",
            details=json.dumps({
                "line-number": e.line_number,
                "msg": e.message,
            }),
        ), 400

    # TODO: Eventually return table of vocab here.
    return "Vocab file received."


@app.route("/send-config", methods=["POST"])
def send_config():
    global question_amount, session_config

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
        return (
            ErrorResponse(
                error="InvalidSessionConfigError",
                message="Invalid session config: 'number-of-questions' must be an integer.",
                details=json.dumps([  # trying to mimic return of ValidationError.json()
                    {
                        "type": "int_type",
                        "loc": ("number-of-questions"),
                        "msg": "Input should be a valid integer",
                    }  # fields 'input' and 'url' missing as they won't be used
                ]),
            ),
            400,
        )

    try:
        session_config = SessionConfig.model_validate(session_config)
    except ValidationError as e:
        logger.exception("Invalid session config.")
        return ErrorResponse(
            error="InvalidSessionConfigError",
            message=f"Invalid session config: {e!s}",
            details=e.json(),
        ), 400

    return "Session config received."


def _generate_questions_json(
    vocab_list: VocabList, question_amount: int, session_config: SessionConfig
):
    assert settings is not None
    return [
        json.loads(json.dumps(question, cls=QuestionClassEncoder))
        for question in ask_question_without_sr(
            vocab_list, question_amount, session_config, settings
        )
    ]


@app.route("/session", methods=["GET"])
def create_session():
    if not vocab_list:
        raise ValueError("Vocab file has not been provided.")

    if not question_amount:
        raise ValueError("The number of questions has not been provided.")

    if not session_config:
        raise ValueError("Session config has not been provided.")

    logger.info("Returning %d questions.")
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
