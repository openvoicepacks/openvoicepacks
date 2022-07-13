"""Unit tests for VoicePack classes and wrapper in openvoicepacks.voicepack.

Current tests:
- Initialization of VoicePack objects with minimal and full parameters.
- Validation of the worklist() method for flat and nested sound dictionaries.
"""

from datetime import datetime

import pytest

from openvoicepacks.voicepack import VoicePack


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
            vp = VoicePack(name="test", sounds=sounds)
            worklist = vp.worklist()
            assert isinstance(worklist, list)
            assert len(worklist) == 2
            assert ("greeting", "hello.wav") in worklist
            assert ("farewell", "goodbye.wav") in worklist

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
            }
            vp = VoicePack(name="test", sounds=sounds)
            worklist = vp.worklist()
            assert isinstance(worklist, list)
            assert len(worklist) == 4
            assert ("MORNING/greeting", "good morning") in worklist
            assert ("MORNING/farewell", "see you later") in worklist
            assert ("EVENING/greeting", "good evening") in worklist
            assert ("EVENING/farewell", "good night") in worklist
