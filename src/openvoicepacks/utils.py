"""Helper functions for OpenVoicePacks.

Includes metadata, file path validation, and JSON fetching from URLs.
"""

import json
import os
from importlib.metadata import metadata as meta
from pathlib import Path
from urllib.request import urlopen

# Package metadata, originates from pyproject.toml
metadata = meta("openvoicepacks").json

# Convert project_url list to a dictionary
metadata["url"] = {}
for item in metadata["project_url"]:
    key, value = item.split(", ", 1)
    metadata["url"][key] = value


def validate_file_path(file_path: str | Path) -> None:
    """Validate that the file path is a non-empty string or Path and writable.

    Args:
        file_path (str | Path): The file path to validate.

    Raises:
        ValueError: If the file path is not a non-empty string/Path or not writable.
    """
    if isinstance(file_path, Path):
        dir_path = file_path.parent or Path()
    elif isinstance(file_path, str):
        if not file_path:
            raise ValueError("file_path must not be empty")
        dir_path = Path(file_path).parent or Path()
    else:
        raise TypeError("file_path must be a string or Path object")
    if not dir_path.exists():
        msg = f"Directory '{dir_path}' does not exist"
        raise ValueError(msg)
    if not os.access(str(dir_path), os.W_OK):
        msg = f"Directory '{dir_path}' is not writable"
        raise ValueError(msg)


def json_from_url(url: str) -> dict | list:
    """Fetch and return JSON data from a given URL.

    Args:
        url (str): The URL to fetch JSON data from.

    Returns:
        dict | list: The JSON data retrieved from the URL.

    Raises:
        ValueError: If the URL is invalid or the data cannot be fetched.
    """
    if not url.startswith(("http:", "https:")):
        raise ValueError("URL must start with 'http:' or 'https:'")

    with urlopen(url) as response:  # NOQA: S310
        return json.load(response)


def text_from_url(url: str) -> str:
    """Fetch and return text data from a given URL.

    Args:
        url (str): The URL to fetch text data from.

    Returns:
        str: The text data retrieved from the URL.
    """
    if not url.startswith(("http:", "https:")):
        raise ValueError("URL must start with 'http:' or 'https:'")

    with urlopen(url) as response:  # NOQA: S310
        return response.read().decode("utf-8")
