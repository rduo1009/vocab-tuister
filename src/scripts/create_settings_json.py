"""Create sample setting json to allow go code to be generated."""

import json
from pathlib import Path
from typing import Any, get_args, get_origin

from pydantic import BaseModel

from src.core.rogo.type_aliases import SessionConfig


def _to_kebab(snake: str) -> str:
    return snake.replace("_", "-")


def _zero_value_for_type(typ: type[Any] | None) -> Any:
    origin = get_origin(typ) or typ

    # Handle optionals (unwrap to inner type)
    if origin is None and typ is None:
        return None
    if origin is type(None):
        return None
    if origin is not None and origin is not typ:
        args = get_args(typ)
        if args:
            return _zero_value_for_type(args[0])

    if origin in {int, float}:
        return origin(0)
    if origin is bool:
        return False
    if origin is str:
        return ""
    if origin in {list, set, tuple}:
        return origin()  # pyright: ignore[reportUnknownVariableType]
    if origin is dict:
        return {}
    if isinstance(origin, type) and issubclass(origin, BaseModel):
        return {
            k: _zero_value_for_type(v.annotation)
            for k, v in origin.model_fields.items()
        }

    return None  # Fallback for unknown types


def _model_zero_values(model: type[BaseModel]) -> dict[str, Any]:
    return {
        _to_kebab(name): _zero_value_for_type(field.annotation)
        for name, field in model.model_fields.items()
    }


if __name__ == "__main__":
    filename: str = "Settings_sample.json"
    output_path: Path = Path(Path(__file__).parent / "json_output" / filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)  # needed?

    d = _model_zero_values(SessionConfig)
    with output_path.open("w", encoding="utf-8") as output_file:
        output_file.write(json.dumps(d) + "\n")
        d["number-of-questions"] = 0
        output_file.write(json.dumps(d) + "\n")
