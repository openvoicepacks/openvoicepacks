"""Unit tests for utility functions in openvoicepacks.utils.

Current tests:
- voicepack_from_csv: Check valid CSV and missing required fields.
- voicepack_from_yaml: Check valid YAML conversion.
- json_from_url: Check valid URL, invalid URL, and non-JSON response.
- validate_file_path: Check valid path, non-existent or non-writable directory,
  empty string, invalid type.
"""

import io
import json
from pathlib import Path
from textwrap import dedent
from unittest.mock import MagicMock, patch

import pytest
import yaml

from openvoicepacks.utils import (
    json_from_url,
    validate_file_path,
    voicepack_from_csv,
    voicepack_from_yaml,
)


class TestVoicePackFromCSV:
    """Tests for voicepack_from_csv utility."""

    def test_valid_csv(self) -> None:
        """Given valid CSV data, returns a VoicePack object with expected fields."""
        csv_content = dedent("""\
            Filename,Path,Translation
            morning.wav,,Morning
            afternoon.wav,alerts,Afternoon
            night.wav,alerts,Night
        """)
        csv_data = io.StringIO(csv_content)
        vp = voicepack_from_csv(csv_data)
        assert hasattr(vp, "sounds")
        assert vp.sounds["morning"] == "Morning"
        assert vp.sounds["alerts"]["afternoon"] == "Afternoon"
        assert vp.sounds["alerts"]["night"] == "Night"

    def test_missing_field(self) -> None:
        """Given CSV missing required fields, raises ValueError."""
        bad_csv = """Filename,Translation\nhello.wav,Hello\n"""
        csv_data = io.StringIO(bad_csv)
        with pytest.raises(ValueError, match="CSV not formatted correctly"):
            voicepack_from_csv(csv_data)


class TestVoicePackFromYAML:
    """Tests for voicepack_from_yaml utility."""

    @pytest.fixture
    def voicepack_dict(self) -> dict:
        """Reusable dict for YAML/JSON tests."""
        return {
            "ovp_schema": 1,
            "name": "TestPack",
            "description": "A test pack",
            "sounds": {
                "hello": "Hello",
                "alerts": {"goodbye": "Goodbye"},
            },
        }

    def test_valid_yaml(self, voicepack_dict: dict) -> None:
        """Given valid YAML, returns a VoicePack object matching the dict."""
        yaml_data = yaml.dump(voicepack_dict)
        vp = voicepack_from_yaml(yaml_data)
        assert vp.name == voicepack_dict["name"]
        assert vp.description == voicepack_dict["description"]
        assert vp.sounds == voicepack_dict["sounds"]


class TestJsonFromUrl:
    """Tests for json_from_url utility."""

    @patch("openvoicepacks.utils.urlopen")
    def test_valid_json(self, mock_urlopen: MagicMock) -> None:
        """Given a valid URL, returns parsed JSON."""
        mock_response = io.BytesIO(json.dumps({"foo": "bar"}).encode())
        mock_urlopen.return_value.__enter__.return_value = mock_response
        result = json_from_url("http://example.com/data.json")
        assert result == {"foo": "bar"}

    @patch("openvoicepacks.utils.urlopen")
    def test_invalid_url(self, mock_urlopen: MagicMock) -> None:
        """Given an invalid URL, raises ValueError."""
        mock_urlopen.side_effect = Exception("Network error")
        with pytest.raises(ValueError, match="Could not fetch JSON data"):
            json_from_url("http://bad-url")

    @patch("openvoicepacks.utils.urlopen")
    def test_non_json_response(self, mock_urlopen: MagicMock) -> None:
        """Given a URL returning non-JSON, raises ValueError."""
        mock_response = io.BytesIO(b"not json")
        mock_urlopen.return_value.__enter__.return_value = mock_response
        with pytest.raises(ValueError, match="Could not fetch JSON data"):
            json_from_url("http://example.com/notjson")


class TestValidateFilePath:
    """Tests for validate_file_path utility."""

    def test_valid_path(self, tmp_path: Path) -> None:
        """Given a valid writable path, does not raise."""
        file_path = tmp_path / "file.txt"
        validate_file_path(file_path)
        validate_file_path(str(file_path))

    def test_nonexistent_directory(self, tmp_path: Path) -> None:
        """Given a non-existent directory, raises ValueError."""
        bad_path = tmp_path / "doesnotexist" / "file.txt"
        with pytest.raises(ValueError, match="does not exist"):
            validate_file_path(bad_path)

    def test_non_writable_directory(self, tmp_path: Path) -> None:
        """Given a non-writable directory, raises ValueError."""
        with (
            patch("os.access", return_value=False),
            pytest.raises(ValueError, match="is not writable"),
        ):
            validate_file_path(tmp_path / "file.txt")

    def test_empty_string(self) -> None:
        """Given an empty string, raises ValueError."""
        with pytest.raises(ValueError, match="must not be empty"):
            validate_file_path("")

    def test_invalid_type(self) -> None:
        """Given a non-string/non-Path, raises TypeError."""
        with pytest.raises(TypeError, match="must be a string or Path object"):
            validate_file_path(123)
