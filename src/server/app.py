"""The Flask API that sends questions to the client."""

# ruff: noqa: D103

import json
from io import StringIO

from flask import Flask, Response, request
from waitress import serve
from werkzeug.exceptions import BadRequest

from .._vendor.typeddict_validator import (
    DictMissingKeyException,
    DictValueTypeMismatchException,
    validate_typeddict,
)
from ..core.lego.exceptions import (
    InvalidVocabDumpError,
    InvalidVocabFileFormatError,
)
from ..core.lego.misc import VocabList
from ..core.lego.reader import _read_vocab_file_internal
from ..core.rogo.asker import ask_question_without_sr
from ..core.rogo.type_aliases import Settings
from .json_encode import QuestionClassEncoder

app = Flask(__name__)
vocab_list: VocabList


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return f"Bad request: {e}", 400


@app.route("/")
def root():
    return "Hello World!"


@app.route("/send-vocab", methods=["POST"])
def send_vocab():
    global vocab_list  # noqa: PLW0603

    try:
        vocab_list = VocabList(
            _read_vocab_file_internal(
                StringIO(request.get_data().decode("utf-8"))
            )
        )
    except (
        InvalidVocabDumpError,
        InvalidVocabFileFormatError,
        FileNotFoundError,
    ) as e:
        raise BadRequest(f"{e} ({type(e).__name__})") from e

    return "Vocab list received."


@app.route("/session", methods=["POST"])
def create_session():
    if not vocab_list:
        raise BadRequest("Vocab list has not been provided.")

    settings = request.get_json()
    try:
        question_amount = settings["number-of-questions"]
        del settings["number-of-questions"]
        validate_typeddict(settings, Settings)
    except (
        DictMissingKeyException,
        DictValueTypeMismatchException,
        KeyError,
    ) as e:
        raise BadRequest(
            "The settings provided are not valid. (InvalidSettingsError)"
        ) from e

    return Response(
        (
            json.dumps(
                question,
                cls=QuestionClassEncoder,
            )
            for question in ask_question_without_sr(
                vocab_list, question_amount, settings
            )
        ),
        mimetype="text/json",
    )


def main_dev(port, *, debug=False):
    app.run(host="127.0.0.1", port=port, debug=debug)


def main(port):
    serve(app, host="127.0.0.1", port=port)
