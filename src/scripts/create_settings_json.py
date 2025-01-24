"""Create sample setting json to allow go code to be generated."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, get_type_hints

from src.core.rogo.type_aliases import Settings


def _create_default_typed_dict(
    typed_dict_class: type[Settings],
) -> Settings:
    defaults: dict[str, Any] = {}
    type_hints = get_type_hints(typed_dict_class)

    for field, field_type in type_hints.items():
        if field_type == str:
            defaults[field] = ""
        elif field_type == int:
            defaults[field] = 0
        elif field_type == bool:
            defaults[field] = False
        elif field_type == float:
            defaults[field] = 0.0
        elif isinstance(field_type, type) and issubclass(field_type, list):
            defaults[field] = []
        elif isinstance(field_type, type) and issubclass(field_type, dict):
            defaults[field] = {}
        else:
            defaults[field] = None  # Default for other types

    return typed_dict_class(**defaults)


if __name__ == "__main__":
    filename: str = "Settings_sample.json"
    output_path: Path = Path(Path(__file__).parent / "json_output" / filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)  # needed?

    d: Settings = _create_default_typed_dict(Settings)
    with output_path.open("w", encoding="utf-8") as output_file:
        output_file.write(json.dumps(d) + "\n")
        d["number-of-questions"] = 0  # type: ignore[typeddict-unknown-key]
        output_file.write(json.dumps(d) + "\n")
