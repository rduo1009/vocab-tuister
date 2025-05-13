"""The Flask API that sends questions to the client."""

# ruff: noqa: D103

from __future__ import annotations

import json
import logging
import traceback
from io import StringIO
from typing import TYPE_CHECKING, Any, cast

from flask import Flask, Response, render_template, request
from waitress import serve
from werkzeug.exceptions import BadRequest

from ..core.lego.misc import VocabList
from ..core.lego.reader import _read_vocab_file_internal
from ..core.rogo.asker import ask_question_without_sr
from ..core.rogo.type_aliases import Settings
from ..utils.typeddict_validator import validate_typeddict
from .json_encode import QuestionClassEncoder

if TYPE_CHECKING:
    from collections.abc import Generator

logger = logging.getLogger(__name__)

app = Flask(__name__)
vocab_list: VocabList | None = None


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    logger.error(
        "%s\n%s",
        e.description,
        "\n".join(traceback.format_tb(e.__traceback__)),
    )
    return f"Bad request: {e}", 400


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
    global vocab_list  # noqa: PLW0603

    try:
        logger.info("Reading vocab list.")
        vocab_list_text = StringIO(request.get_data().decode("utf-8"))
        vocab_list = VocabList(
            _read_vocab_file_internal(vocab_list_text),
            vocab_list_text.getvalue(),
        )
    except Exception as e:
        raise BadRequest(f"{type(e).__name__}: {e}").with_traceback(
            e.__traceback__
        ) from e

    return "Vocab list received."


def generate_questions_sample_json(
    vocab_list: VocabList, question_amount: int, settings: Settings
) -> Generator[str]:
    return (
        json.dumps(question, cls=QuestionClassEncoder)
        for question in ask_question_without_sr(
            vocab_list, question_amount, settings
        )
    )


def _generate_questions_json(
    vocab_list: VocabList, question_amount: int, settings: Settings
) -> str:
    def _rearrange[T](d: dict[str, T]) -> dict[str, str | dict[str, T]]:
        question_type = cast("str", d.pop("question_type"))
        return {"question_type": question_type, question_type: d}

    json_list = [
        _rearrange(json.loads(json.dumps(question, cls=QuestionClassEncoder)))
        for question in ask_question_without_sr(
            vocab_list, question_amount, settings
        )
    ]
    return json.dumps(json_list)


@app.route("/session", methods=["POST"])
def create_session():
    if not vocab_list:
        raise BadRequest("Vocab list has not been provided.")

    logger.info("Validating settings.")
    settings: dict[str, Any] = request.get_json()
    try:
        question_amount = settings.pop("number-of-questions")
        validate_typeddict(settings, Settings)
    except (ExceptionGroup, KeyError) as e:
        error_message_detail = str(e)
        if isinstance(e, ExceptionGroup):
            error_message_detail = "; ".join(
                str(sub_ex) for sub_ex in e.exceptions
            )

        raise BadRequest(
            f"The settings provided are not valid: {error_message_detail} (InvalidSettingsError)"
        ) from e

    logger.info("Returning %d questions.", question_amount)
    try:
        return Response(
            _generate_questions_json(
                vocab_list, question_amount, cast("Settings", settings)
            ),
            mimetype="application/json",
        )
    except Exception as e:
        raise BadRequest(f"{type(e).__name__}: {e}").with_traceback(
            e.__traceback__
        ) from e


def main_dev(port, *, debug=False):
    app.run(host="127.0.0.1", port=port, debug=debug)


def main(port):
    serve(app, host="127.0.0.1", port=port)
