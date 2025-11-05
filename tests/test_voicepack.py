"""Unit tests for VoicePack classes and wrapper in openvoicepacks.voicepack.

Current tests:
- Initialization of VoicePack objects with minimal and full parameters.
- Validation of the worklist() method for flat and nested sound dictionaries.
"""

import io
from datetime import datetime
from pathlib import Path
from textwrap import dedent

import pytest
import yaml

from openvoicepacks.audio import SoundFile
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
                "greeting": "hello",
                "farewell": "goodbye",
            }
            expected = [
                {"path": "greeting", "text": "hello"},
                {"path": "farewell", "text": "goodbye"},
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

    class TestYAML:
        """Tests for VoicePack YAML output."""

        def test_yaml_output(self, sample_data: dict[str, str | int]) -> None:
            """Given a VoicePack, yaml() returns expected YAML string."""
            vp = VoicePack(**sample_data)
            yaml_str = vp.yaml()
            assert isinstance(yaml_str, str)
            yaml_data = yaml.safe_load(yaml_str)
            assert yaml_data["name"] == sample_data["name"]
            assert yaml_data["description"] == sample_data["description"]
            assert yaml_data["creator"] == sample_data["creator"]
            assert yaml_data["contact"] == sample_data["contact"]

        def test_yaml_schema(self, sample_data: dict[str, str | int]) -> None:
            """Given a VoicePack, the YAML output conforms to the schema."""
            vp = VoicePack(**sample_data)
            yaml_str = vp.yaml()
            yaml_data = yaml.safe_load(yaml_str)
            # This will raise ValidationError if the schema does not match
            model = VoicePack(**yaml_data)
            assert model.name == sample_data["name"]

    class TestSave:
        """Tests for VoicePack save method."""

        @pytest.fixture
        def tmp_file_path(self, tmp_path: str) -> str:
            """Temporary file path for testing save."""
            return str(tmp_path / "test_voicepack.yaml")

        @pytest.fixture
        def default_file_path(self, sample_data: dict[str, str | int]) -> str:
            """Default file path derived from packname."""
            packname = f"{sample_data['name'].replace(' ', '_')}.yaml"
            yield packname
            Path(packname).unlink(missing_ok=True)

        def test_save_creates_file(
            self, sample_data: dict[str, str | int], tmp_file_path: str
        ) -> None:
            """Given a filename, save() creates a YAML file."""
            vp = VoicePack(**sample_data)
            saved_path = vp.save(tmp_file_path)
            assert saved_path == tmp_file_path
            with Path.open(saved_path, encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f.read())
            assert yaml_data["name"] == sample_data["name"]

        def test_save_default_filename(
            self, sample_data: dict[str, str | int], default_file_path: str
        ) -> None:
            """Given no filename, save() uses default derived from packname."""
            vp = VoicePack(**sample_data)
            saved_path = vp.save()
            assert saved_path == default_file_path
            with Path.open(saved_path, encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f.read())
            assert yaml_data["name"] == sample_data["name"]

    class TestMerge:
        """Tests for VoicePack merge method."""

        def test_merge_voicepacks(self) -> None:
            """Given two VoicePacks, merge() combines their sounds correctly."""
            parent_sounds = {
                "greeting": "hello",
                "farewell": "goodbye",
                "alerts": {
                    "low_battery": "battery low",
                    "signal_lost": "signal lost",
                },
            }
            child_sounds = {
                "greeting": "hi",  # This should override parent's greeting
                "notifications": {
                    "message_received": "you have a message",
                },
                "alerts": {
                    "custom_alert": "custom alert",
                },
            }
            expected_sounds = {
                "greeting": "hi",  # Child's greeting takes precedence
                "farewell": "goodbye",
                "alerts": {
                    "low_battery": "battery low",
                    "signal_lost": "signal lost",
                    "custom_alert": "custom alert",
                },
                "notifications": {
                    "message_received": "you have a message",
                },
            }
            parent_vp = VoicePack(name="parent", sounds=parent_sounds)
            child_vp = VoicePack(name="child", sounds=child_sounds)
            child_vp.merge(parent_vp)
            assert child_vp.sounds == expected_sounds


class TestVoicePackFromCSV:
    """Tests for voicepack_from_csv utility."""

    def test_valid_csv(self) -> None:
        """Given valid CSV data, returns a VoicePack object with expected fields."""
        csv_content = dedent("""\
            "String ID","Source text","Filename","Path","Translation"
            "1","0","morning.wav","","Morning"
            "2","1","afternoon.wav","alerts","Afternoon"
            "3","1","night.wav","alerts","Night"
        """)
        csv_data = io.StringIO(csv_content)
        vp = voicepack_from_csv(csv_data)
        assert hasattr(vp, "sounds")
        assert vp.sounds["morning"] == "Morning"
        assert vp.sounds["alerts"]["afternoon"] == "Afternoon"
        assert vp.sounds["alerts"]["night"] == "Night"

    def test_missing_field(self) -> None:
        """Given CSV missing required fields, raises ValueError."""
        bad_csv = """"Filename","Translation"\nhello.wav,Hello\n"""
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
