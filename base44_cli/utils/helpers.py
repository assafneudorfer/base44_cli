"""Helper utilities for Base44 CLI."""

import json
from pathlib import Path
from typing import Any


def load_json_file(file_path: str) -> Any:
    """Load data from JSON file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path) as f:
        return json.load(f)


def save_json_file(data: Any, file_path: str, pretty: bool = True) -> None:
    """Save data to JSON file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        if pretty:
            json.dump(data, f, indent=2, default=str)
        else:
            json.dump(data, f, default=str)


def parse_json_string(json_str: str) -> Any:
    """Parse JSON string safely."""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")


def confirm_action(message: str) -> bool:
    """Ask user for confirmation."""
    response = input(f"{message} (y/N): ").strip().lower()
    return response in ("y", "yes")
