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
from unittest.mock import MagicMock, patch

import pytest

from openvoicepacks.utils import (
    json_from_url,
    validate_file_path,
)


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
