"""JSON persistence and application logging."""

import json
import logging
from pathlib import Path

DEFAULT_PATH = Path("data/gradebook.json")
LOG_PATH = Path("logs/app.log")


def get_logger() -> logging.Logger:
    """Return the configured application logger."""
    logger = logging.getLogger("gradebook")
    if not logger.handlers:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s"
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def load_data(path: str | Path = DEFAULT_PATH) -> dict:
    """Load gradebook data; return an empty structure when no file exists."""
    logger = get_logger()
    file_path = Path(path)
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError("The gradebook JSON root must be an object.")
        data.setdefault("students", [])
        data.setdefault("courses", [])
        data.setdefault("enrollments", [])
        logger.info("Loaded gradebook data from %s", file_path)
        return data
    except FileNotFoundError:
        logger.info("No data file found at %s; starting with empty data", file_path)
        return {"students": [], "courses": [], "enrollments": []}
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON in %s: %s", file_path, exc)
        raise ValueError(
            f"Could not read {file_path}: invalid JSON. "
            "Restore a valid file or run the seed script."
        ) from exc
    except OSError:
        logger.exception("Unable to read %s", file_path)
        raise


def save_data(data: dict, path: str | Path = DEFAULT_PATH) -> None:
    """Save gradebook data as formatted JSON."""
    logger = get_logger()
    file_path = Path(path)
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = file_path.with_suffix(file_path.suffix + ".tmp")
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        temporary_path.replace(file_path)
        logger.info("Saved gradebook data to %s", file_path)
    except OSError:
        logger.exception("Unable to save %s", file_path)
        raise
