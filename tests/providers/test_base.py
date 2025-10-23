"""Tests for the TTS provider base class.

Only tests that are specific to the base class should go here. Most provider tests
should be in tests/providers/test_all.py to ensure consistency across all providers.

Current tests:
- Validation of text input.
- Validation of VoiceModel objects.
- Ensuring unimplemented methods raise NotImplementedError.
"""

import pytest

from openvoicepacks.providers import Provider
from openvoicepacks.voicemodels import VoiceModel


@pytest.fixture
def generic_model() -> VoiceModel:
    """Return a valid VoiceModel for testing."""
    return VoiceModel(voice="test", language="en_GB", provider="generic", option="")


class TestProviderValidation:
    """Validation tests for the Provider base class."""

    class TestCheckModel:
        """Tests for the check_model() method of the Provider class."""

        def test_valid_model(self, generic_model: VoiceModel) -> None:
            """Given a valid model, check_model() passes."""
            Provider().check_model(generic_model)

        def test_invalid_model(self) -> None:
            """Given an invalid model, check_model() raises TypeError."""
            with pytest.raises(TypeError, match="Model must be a VoiceModel object"):
                Provider().check_model(None)

        def test_incorrect_model(self, generic_model: VoiceModel) -> None:
            """Given an incorrect model, check_model() raises ValueError."""
            vm = generic_model
            vm.provider = "wrong_provider"
            with pytest.raises(
                ValueError, match="Model must be compatible with this provider"
            ):
                Provider().check_model(vm)

    class TestCheckText:
        """Tests for the check_text() method of the Provider class."""

        def test_valid_text(self) -> None:
            """Given a valid string, check_text() passes."""
            Provider().check_text("Valid text")

        def test_invalid_text(self) -> None:
            """Given an invalid string, check_text() raises ValueError."""
            with pytest.raises(ValueError, match="Text must be a non-empty string"):
                Provider().check_text(None)


class TestProviderStubs:
    """Tests for unimplemented methods in the Provider base class."""

    def test_synthesise(self, generic_model: VoiceModel) -> None:
        """Given a call to synthesise(), NotImplementedError is raised."""
        with pytest.raises(
            NotImplementedError, match="Subclasses must implement this method"
        ):
            Provider().synthesise("Test text", generic_model)
