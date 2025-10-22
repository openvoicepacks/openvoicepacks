"""Unit tests for VoicePack classes and wrapper in openvoicepacks.voicepack.

Current tests:
- Initialization of VoicePack objects with minimal and full parameters.
- Validation of the worklist() method for flat and nested sound dictionaries.
"""

import io
from datetime import datetime
from textwrap import dedent

import pytest
import yaml

from openvoicepacks.sounds import SoundFile
from openvoicepacks.voicepack import VoicePack, voicepack_from_csv, voicepack_from_yaml


class TestVoicePack:
    """Tests for the VoicePack wrapper class."""

    @pytest.fixture
    def sample_data(self) -> dict[str, str | int]:
        """Sample YAML data for testing."""
        return {
            "ovp_schema": 1,
            "name": "test with space",
            "description": "Default English (UK) voice pack",
            "creator": "Your Name",
            "contact": "yourname@youremail.local",
        }

    class TestInitialisation:
        """Tests for VoicePack initialisation."""

        def test_basic_initialisation(self) -> None:
            """Given minimal parameters, VoicePack can be initialised."""
            vp = VoicePack(name="test")
            assert isinstance(vp, VoicePack)

        def test_full_initialisation(self, sample_data: dict[str, str | int]) -> None:
            """Given full parameters, VoicePack can be initialised."""
            vp = VoicePack(**sample_data)
            assert isinstance(vp, VoicePack)
            assert vp.packname == sample_data["name"].replace(" ", "_")
            assert isinstance(vp.creation_date, datetime)

    class TestWorklist:
        """Tests for VoicePack worklist method."""

        def test_empty_sounds(self) -> None:
            """Given no sounds, worklist returns empty list."""
            vp = VoicePack(name="test")
            worklist = vp.worklist()
            assert isinstance(worklist, list)
            assert len(worklist) == 0

        def test_flat_sounds(self) -> None:
            """Given flat sounds dict, worklist returns correct list."""
            sounds = {
                "greeting": "hello.wav",
                "farewell": "goodbye.wav",
            }
            expected = [
                {"path": "greeting", "text": "hello.wav"},
                {"path": "farewell", "text": "goodbye.wav"},
            ]
            vp = VoicePack(name="test", sounds=sounds)
            worklist = vp.worklist()
            assert isinstance(worklist, list)
            assert len(worklist) == 2
            for item, exp in zip(worklist, expected, strict=True):
                assert isinstance(item, SoundFile)
                assert item.path == exp["path"]
                assert item.text == exp["text"]

        def test_nested_sounds(self) -> None:
            """Given nested sounds dict, worklist returns flattened list."""
            sounds = {
                "morning": {
                    "greeting": "good morning",
                    "farewell": "see you later",
                },
                "evening": {
                    "greeting": "good evening",
                    "farewell": "good night",
                },
                "greeting": "hello",
                "farewell": "goodbye",
            }
            expected = [
                {"path": "MORNING/greeting", "text": "good morning"},
                {"path": "MORNING/farewell", "text": "see you later"},
                {"path": "EVENING/greeting", "text": "good evening"},
                {"path": "EVENING/farewell", "text": "good night"},
                {"path": "greeting", "text": "hello"},
                {"path": "farewell", "text": "goodbye"},
            ]
            vp = VoicePack(name="test", sounds=sounds)
            worklist = vp.worklist()
            assert isinstance(worklist, list)
            assert len(worklist) == 6
            for item, exp in zip(worklist, expected, strict=True):
                assert isinstance(item, SoundFile)
                assert item.path == exp["path"]
                assert item.text == exp["text"]


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
