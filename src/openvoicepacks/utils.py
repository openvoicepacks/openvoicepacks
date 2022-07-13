"""Helper functions for OpenVoicePacks.

Includes file path validation.
"""

import csv
import json
import os
from pathlib import Path
from urllib.request import urlopen

import yaml

from openvoicepacks.voicepack import VoicePack


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

    Arguments:
        url (str): The URL to fetch JSON data from.

    Returns:
        dict | list: The JSON data retrieved from the URL.

    Raises:
        ValueError: If the URL is invalid or the data cannot be fetched.
    """
    try:
        with urlopen(url) as response:  # NOQA: S310
            return json.load(response)
    except Exception as e:
        msg = f"Could not fetch JSON data from URL '{url}': {e}"
        raise ValueError(msg) from e


def voicepack_from_csv(csv_data: dict) -> VoicePack:
    """Convert CSV data from EdgeTX/OpenTX community to a VoicePack object.

    Args:
        csv_data (dict): The CSV data to convert.

    Returns:
        VoicePack: The converted VoicePack object.

    Raises:
        ValueError: If the CSV data is not formatted correctly.
    """
    # Since the CSV format does not include metadata, we set some defaults.
    data = {
        "ovp_schema": 1,
        "name": "Unnamed",
        "description": "Imported from CSV",
        "sounds": {},
    }

    # Load CSV data as a list of dicts where each field is a key.
    csv_dict = csv.DictReader(csv_data)

    # Check CSV data is in the correct format.
    required_fields = ["Filename", "Path", "Translation"]
    for field in required_fields:
        if field not in csv_dict.fieldnames:
            raise ValueError("CSV not formatted correctly")

    # Convert the CSV data into the standard OSP format.
    for row in csv_dict:
        filename = row.get("Filename").replace(".wav", "")
        string = row.get("Translation")
        path = row.get("Path").lower()

        # If there is a path attribute set, nest the values inside that.
        if len(path) > 0:
            if path not in data["sounds"]:
                data["sounds"][path] = {}
            data["sounds"][path][filename] = string
        else:
            data["sounds"][filename] = string

    return VoicePack(**data)


def voicepack_from_yaml(yaml_data: dict) -> VoicePack:
    """Convert YAML data to a VoicePack object.

    Args:
        yaml_data (dict): The YAML data to convert.

    Returns:
        VoicePack: The converted VoicePack object.
    """
    data = yaml.safe_load(yaml_data)
    return VoicePack(**data)
