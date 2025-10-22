"""Unit tests for the AudioData class in openvoicepacks.audio.

Current tests:
- Initialization of AudioData objects.
- Writing audio data to WAV files.
"""

from pathlib import Path

import magic
import pytest

from openvoicepacks.audio import AudioData, SoundFile

WAV_CONFIG = {
    "data": b"00",
    "rate": 16000,
    "width": 2,
    "channels": 1,
}


class TestAudioData:
    """Test suite for the AudioData class."""

    @pytest.fixture
    def audio_data(self) -> AudioData:
        """Return a sample AudioData object."""
        return AudioData(
            data=WAV_CONFIG["data"],
            rate=WAV_CONFIG["rate"],
            width=WAV_CONFIG["width"],
            channels=WAV_CONFIG["channels"],
        )

    @pytest.fixture
    def tmp_file(self, tmp_path: Path) -> Path:
        """Return a temporary file path for testing."""
        return tmp_path / "test_output.wav"

    class TestInitialization:
        """Test suite for AudioData initialization."""

        def test_object_initialization(self, audio_data: AudioData) -> None:
            """Given valid audio data, when initialized, then properties are correct."""
            assert audio_data.data == WAV_CONFIG["data"], "Data does not match."
            assert audio_data.rate == WAV_CONFIG["rate"], "Rate does not match."
            assert audio_data.width == WAV_CONFIG["width"], "Width does not match."
            assert audio_data.channels == WAV_CONFIG["channels"], (
                "Channels does not match."
            )

    class TestWriteWav:
        """Test suite for the write_wav method in AudioData."""

        def test_sound_data_is_valid(
            self, audio_data: AudioData, tmp_file: Path
        ) -> None:
            """Given audio data, when written to a WAV file, then the file is valid."""
            audio_data.write_wav(tmp_file)
            assert tmp_file.exists(), "WAV file was not created successfully."
            mime = magic.Magic(mime=True)
            assert mime.from_file(tmp_file) == "audio/x-wav", "WAV file is not valid."

        def test_invalid_output_rate(
            self, audio_data: AudioData, tmp_file: Path
        ) -> None:
            """Given audio data with an invalid output rate, ValueError is raised."""
            for bad_rate in [0, -1, 1.5, "16000", None]:
                with pytest.raises(
                    ValueError, match="output_rate must be a positive integer"
                ):
                    audio_data.write_wav(tmp_file, output_rate=bad_rate)


class TestSoundFile:
    """Tests for the SoundFile class."""

    class DummyAudio:
        """Dummy audio class for testing."""

    class DummyVoiceModel:
        """Dummy voice model class for testing."""

    def test_basic_initialisation(self) -> None:
        """Given path and text, SoundFile initializes correctly."""
        sf = SoundFile(path="greeting", text="hello")
        assert sf.path == "greeting"
        assert sf.text == "hello"
        assert sf.audio is None
        assert sf.voicemodel is None
        assert repr(sf) == "<SoundFile path='greeting' text='hello' audio=no>"

    def test_initialisation_with_kwargs(self) -> None:
        """Given path, text, audio, and voicemodel, SoundFile initializes correctly."""
        audio = self.DummyAudio()
        voicemodel = self.DummyVoiceModel()
        sf = SoundFile(
            path="farewell", text="goodbye", audio=audio, voicemodel=voicemodel
        )
        assert sf.path == "farewell"
        assert sf.text == "goodbye"
        assert sf.audio is audio
        assert sf.voicemodel is voicemodel
        assert repr(sf) == "<SoundFile path='farewell' text='goodbye' audio=yes>"

    def test_repr_audio_absent(self) -> None:
        """Given no audio, __repr__ indicates audio is absent."""
        sf = SoundFile(path="test", text="something")
        assert "audio=no" in repr(sf)

    def test_repr_audio_present(self) -> None:
        """Given audio present, __repr__ indicates audio is present."""
        sf = SoundFile(path="test", text="something", audio=object())
        assert "audio=yes" in repr(sf)
