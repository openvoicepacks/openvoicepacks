"""Test suite for tests that should work on all TTS providers.

This is the main test suite for provider functionality that is common across all
providers. Specific provider tests should be in their own test files to cover provider-
specific functionality.

Current tests:
- Initialization of provider instances.
- Setting VoiceModel objects.
- Synthesising audio from text with and without specifying a model.
- Writing audio data to WAV files.
"""

import pytest

from openvoicepacks.audio import AudioData
from openvoicepacks.providers import Piper, Polly
from openvoicepacks.voicemodels import VoiceModel

VALID_CONFIGS = [
    {
        "type": Polly,
        "model": VoiceModel(
            voice="Amy",
            language="en_GB",
            provider="polly",
            option="standard",
        ),
    },
    {
        "type": Piper,
        "model": VoiceModel(
            voice="Alan",
            language="en_GB",
            provider="piper",
            option="medium",
        ),
    },
]


@pytest.fixture(params=VALID_CONFIGS, ids=[m["type"].__name__ for m in VALID_CONFIGS])
def provider_config(request: object) -> dict[str, object]:
    """Return a valid model config for testing."""
    return request.param


class TestAllProviders:
    """Test suite for tests that should work on all TTS providers."""

    class TestInitialisation:
        """Test suite for the initialisation of provider instances."""

        def test_init(self, provider_config: dict[str, object]) -> None:
            """Given no arguments, provider instance is created successfully."""
            expected_type = provider_config["type"]
            instance = expected_type()
            assert isinstance(instance, expected_type), (
                f"{expected_type.__name__} client was not created successfully."
            )

        def test_voicemodel(self, provider_config: dict[str, object]) -> None:
            """Given a valid VoiceModel, provider instance accepts it."""
            expected_type = provider_config["type"]
            instance = expected_type()
            instance.voice = provider_config["model"]
            assert isinstance(instance, expected_type), (
                f"{expected_type.__name__} client was not created successfully."
            )
            assert isinstance(instance.voice, VoiceModel), (
                f"{expected_type.__name__} voice was not set successfully."
            )

    class TestSynthesise:
        """Test suite for the synthesise() method of provider instances."""

        def test_valid_string_and_model(
            self, provider_config: dict[str, object]
        ) -> None:
            """Given a valid string and model, synthesise() processes the request."""
            expected_type = provider_config["type"]
            provider_model = provider_config["model"]
            instance = expected_type()
            assert isinstance(
                instance.synthesise("Test Valid String", provider_model),
                AudioData,
            ), "Audio data is not a valid AudioData object."

        def test_valid_string_only(self, provider_config: dict[str, object]) -> None:
            """Given a valid string, synthesise() processes the request."""
            expected_type = provider_config["type"]
            instance = expected_type()
            instance.model = provider_config["model"]
            assert isinstance(
                instance.synthesise("Test Valid String"),
                AudioData,
            ), "Audio data is not a valid AudioData object."

        def test_no_default_model(self, provider_config: dict[str, object]) -> None:
            """Given no model, synthesise() raises an error."""
            expected_type = provider_config["type"]
            instance = expected_type()
            with pytest.raises(
                ValueError, match="No default voice set for this provider"
            ):
                instance.synthesise("Test String Without Model")

        def test_no_string(self, provider_config: dict[str, object]) -> None:
            """Given no string, synthesise() raises an error."""
            expected_type = provider_config["type"]
            provider_model = provider_config["model"]
            instance = expected_type()
            with pytest.raises(ValueError, match="Text must be a non-empty string"):
                instance.synthesise("", provider_model)

    class TestProcess:
        """Test suite for the process() method of provider instances."""

        def test_write_wave(
            self, tmp_path: str, provider_config: dict[str, object]
        ) -> None:
            """Given valid parameters, process() writes valid WAV file to given path."""
            out_path = tmp_path / "test.wav"
            expected_type = provider_config["type"]
            provider_model = provider_config["model"]
            instance = expected_type()
            instance.process(str(out_path), "Test Write Wav", provider_model)
            assert out_path.exists(), "WAV file was not created."
