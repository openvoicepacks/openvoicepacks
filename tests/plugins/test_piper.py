"""Test suite for the Piper TTS provider.

Only tests that are specific to Piper should go here. Most provider tests should be in
tests/providers/test_all.py to ensure consistency across all providers.

Current tests:
- Synthesising audio from text whilst downloading a new voice model.
- Downloading valid and invalid voice models.
"""

import pytest

from openvoicepacks.audio import AudioData
from openvoicepacks.plugins.piper import Piper
from openvoicepacks.voicemodel import VoiceModel


class TestPiper:
    """Test suite for the Piper TTS provider."""

    @pytest.fixture
    def piper_model(self) -> VoiceModel:
        """Given a test, returns a Piper voice object."""
        return VoiceModel(
            voice="Alan",
            language="en_GB",
            provider="piper",
            option="medium",
        )

    @pytest.fixture
    def piper_tmp(self, tmp_path: str) -> Piper:
        """Given a test, returns a Piper instance with a temp install directory."""
        instance = Piper()
        instance.install_dir = tmp_path
        return instance

    class TestSynthesise:
        """Test suite for the synthesise() method in Piper."""

        @pytest.mark.slow
        def test_fresh_install(self, piper_tmp: Piper, piper_model: VoiceModel) -> None:
            """Given a fresh install, downloads model and processes the request."""
            assert isinstance(
                piper_tmp.synthesise("Test Fresh Install", piper_model),
                AudioData,
            ), "Audio data is not a valid AudioData object."

    class TestDownloadVoiceModel:
        """Test suite for the download_voice() method in Piper."""

        @pytest.mark.slow
        def test_valid_voice_model(
            self, piper_tmp: Piper, piper_model: VoiceModel
        ) -> None:
            """Given a valid voice model ID, download_voice() downloads the model."""
            model = piper_model
            model_name = f"{model.language}-{model.voice}-{model.option}"
            model_path = piper_tmp.install_dir / f"{model_name}.onnx"
            piper_tmp.download_voice(model_name)
            assert model_path.exists(), (
                "VoiceModel model was not downloaded successfully."
            )

        def test_invalid_voice_model(
            self, piper_tmp: Piper, piper_model: VoiceModel
        ) -> None:
            """Given an invalid voice model ID, download_voice() raises an error."""
            model = piper_model
            model_name = f"{model.language}-{model.voice}_invalid-{model.option}"
            with pytest.raises(ValueError, match="is not available"):
                piper_tmp.download_voice(model_name)
