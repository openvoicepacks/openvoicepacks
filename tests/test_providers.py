"""Tests for the TTS provider base class.

Only tests that are specific to the base class should go here. Most provider tests
should be in tests/plugins/test_all.py to ensure consistency across all providers.

Current tests:
- Validation of text input.
- Validation of VoiceModel objects.
- Ensuring unimplemented methods raise NotImplementedError.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from openvoicepacks.providers import Provider
from openvoicepacks.voicemodel import VoiceModel


@pytest.fixture
def generic_model() -> VoiceModel:
    """Return a valid VoiceModel for testing."""
    return VoiceModel(
        voice="test", language="en_GB", provider="generic", option="standard"
    )


class TestProviderValidation:
    """Validation tests for the Provider base class."""

    class TestCheckModel:
        """Tests for the check_model() method of the Provider base class."""

        class DummyModel:
            """Simulate a model with a provider attribute."""

            def __init__(self, provider: object) -> None:  # NOQA: D107
                self.provider = provider

        def test_valid_model(self) -> None:
            """Given a valid model, check_model() passes."""
            model = self.DummyModel(Provider)
            Provider().check_model(model)

        def test_check_model_invalid_provider(self) -> None:
            """Given a model, if the provider does not match, ValueError is raised."""

            class OtherProvider:
                pass

            model = self.DummyModel(OtherProvider)
            with pytest.raises(ValueError, match="must be compatible"):
                Provider().check_model(model)

        def test_none_model(self) -> None:
            """Given an invalid model, AttributeError is raised."""
            with pytest.raises(AttributeError):
                Provider().check_model(None)

    class TestCheckText:
        """Tests for the check_text() method of the Provider base class."""

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


class TestProviderAttributes:
    """Tests for Provider class attributes and defaults."""

    def test_class_attributes(self) -> None:
        """Given class attributes, they have correct default values."""
        assert Provider.description == "A generic text-to-speech provider."
        assert Provider.version == "local"
        assert Provider.provider == "generic"
        assert Provider.valid_options == {"standard"}
        assert Provider.default_option == "standard"
        assert isinstance(Provider.capabilities, set)

    def test_instance_attributes(self) -> None:
        """Given an instance of Provider, it has no unexpected attributes."""
        p = Provider()
        # Provider has no instance attributes by default
        assert not hasattr(p, "model") or p.model is None


class TestProviderProcess:
    """Tests for the process method of Provider."""

    def test_process_calls_write_wav(self, generic_model: VoiceModel) -> None:
        """Given a call to process(), synthesise() is called and write_wav() is used."""
        p = Provider()
        # Patch synthesise to return a mock AudioData with a write_wav method
        mock_audio = MagicMock()
        p.synthesise = MagicMock(return_value=mock_audio)
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
        try:
            p.process(tmp_path, "text", generic_model)
            p.synthesise.assert_called_once_with("text", generic_model)
            mock_audio.write_wav.assert_called_once_with(tmp_path)
        finally:
            Path.unlink(tmp_path)
