"""The Flask API that sends questions to the client."""

# ruff:file-ignore[undocumented-public-function, global-statement]

from __future__ import annotations

import asyncio
import logging
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Final, override

from grpclib import GRPCError
from grpclib.const import Status
from grpclib.health.service import Health
from grpclib.server import Server
from grpclib.utils import graceful_exit
from platformdirs import PlatformDirs
from pydantic import ValidationError

from ..core.lego.cache import cache_vocab_file
from ..core.lego.exceptions import InvalidVocabFileFormatError
from ..core.rogo.asker import ask_question_without_sr
from ..core.rogo.type_aliases import Settings
from ..core.transfero.synonyms import setup_wn
from ..pb.vocab_tuister.v1 import (
    CreateSessionResponse,
    VerifyConfigResponse,
    VerifyVocabResponse,
    VocabTesterServiceBase,
)
from .exceptions import InvalidSettingsError

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from ..pb.vocab_tuister.v1 import (
        CreateSessionRequest,
        VerifyConfigRequest,
        VerifyVocabRequest,
    )

logger = logging.getLogger(__name__)

dirs = PlatformDirs("vocab-tuister", "rduo1009")

settings: Settings | None = None
HOST: Final[str] = "127.0.0.1"


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


class VocabTesterService(VocabTesterServiceBase):
    """VocabTesterServicer provides an implementation of the methods of
    the VocabTesterServiceStub stub.
    """  # ruff:ignore[missing-blank-line-after-summary]

    @override
    async def verify_vocab(
        self, message: VerifyVocabRequest
    ) -> VerifyVocabResponse:
        try:
            assert settings is not None
            _, _ = cache_vocab_file(
                StringIO(message.vocab_text),
                cache_folder=dirs.user_cache_path,
                compress=settings.cache_vocab_lists,
            )
        except InvalidVocabFileFormatError as e:
            logger.exception("Invalid vocab file format.")
            raise GRPCError(
                Status.INVALID_ARGUMENT,
                f"{e.message} (error on line {e.line_number})",
            ) from e

        return VerifyVocabResponse()

    @override
    async def verify_config(
        self, message: VerifyConfigRequest
    ) -> VerifyConfigResponse:
        if message.number_of_questions <= 0:
            raise GRPCError(
                Status.INVALID_ARGUMENT,
                "number_of_questions must be at least 1",
            )

        assert message.session_config is not None
        if message.session_config.number_multiplechoice_options <= 1:
            raise GRPCError(
                Status.INVALID_ARGUMENT,
                "number_multiplechoice_options must be at least 2",
            )

        # Otherwise, thanks to pydantic type checking, this will always work!
        return VerifyConfigResponse()

    @override
    async def create_session(
        self, message: CreateSessionRequest
    ) -> AsyncIterator[CreateSessionResponse]:
        if message.number_of_questions <= 0:
            raise GRPCError(
                Status.INVALID_ARGUMENT,
                "number_of_questions must be at least 1",
            )

        assert message.session_config is not None
        if message.session_config.number_multiplechoice_options <= 1:
            raise GRPCError(
                Status.INVALID_ARGUMENT,
                "number_multiplechoice_options must be at least 2",
            )

        assert settings is not None

        vocab_list, _ = cache_vocab_file(
            StringIO(message.vocab_list),
            cache_folder=dirs.user_cache_path,
            compress=settings.cache_vocab_lists,
        )

        assert message.session_config is not None

        try:
            for question in ask_question_without_sr(
                vocab_list,
                message.number_of_questions,
                message.session_config,
                settings,
            ):
                yield CreateSessionResponse(question)

        except Exception as e:
            logger.exception("Error while generating session questions: %s", e)  # ruff:ignore[verbose-log-message]
            raise GRPCError(
                Status.INTERNAL, f"Failed while generating questions: {e}"
            ) from e


async def run(port: int):
    service = VocabTesterService()
    health = Health()
    server = Server([service, health])
    with graceful_exit([server]):
        await server.start(HOST, port)
        logger.info("Server running on %s:%d", HOST, port)
        await server.wait_closed()


def main(port: int):
    global settings
    settings = _get_settings()
    if settings.include_synonyms:
        setup_wn()

    asyncio.run(run(port))
