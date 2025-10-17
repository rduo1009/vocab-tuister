"""Create sample setting json to allow go code to be generated."""

import json
from pathlib import Path

from src.core.rogo.type_aliases import SessionConfig

if __name__ == "__main__":
    filename: str = "Settings_sample.json"
    output_path: Path = Path(Path(__file__).parent / "json_output" / filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)  # needed?

    d = SessionConfig.model_construct().model_dump()
    with output_path.open("w", encoding="utf-8") as output_file:
        output_file.write(json.dumps(d) + "\n")
        d["number-of-questions"] = 0
        output_file.write(json.dumps(d) + "\n")
