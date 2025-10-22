"""Unit tests for SoundFile class in openvoicepacks.sounds."""

from openvoicepacks.sounds import SoundFile


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
