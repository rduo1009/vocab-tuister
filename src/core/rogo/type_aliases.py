"""Contains type aliases used by rogo."""

# pyright: reportUnannotatedClassAttribute=false

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, StrictBool

from src.core.accido.endings import Word

type Vocab = list[Word]


def _to_kebab(snake: str) -> str:
    return snake.replace("_", "-")


class Settings(BaseModel):
    """Global settings for vocab-tuister."""

    model_config = ConfigDict(
        extra="forbid",
        validate_by_name=False,
        validate_by_alias=True,
        alias_generator=_to_kebab,
    )

    cache_vocab_lists: StrictBool
    include_synonyms: StrictBool
    include_similar_words: StrictBool
