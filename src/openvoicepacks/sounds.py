"""SoundFile class for OpenVoicePacks.

Encapsulates all metadata and audio data for a single sound.
"""

from openvoicepacks.audio import AudioData
from openvoicepacks.voicemodel import VoiceModel


class SoundFile:
    """Represents a single sound asset, including text, audio, and path.

    Attributes:
        audio: Audio data for the sound.
        voicemodel: Voice model used for synthesis.
    """

    audio: AudioData | None = None
    voicemodel: VoiceModel | None = None
    path: str
    text: str

    def __init__(self, path: str, text: str, **kwargs: dict[str, object]) -> None:
        """Initialize SoundFile with metadata and optional audio.

        Arguments:
            path: Relative path for output (e.g. "en/hello.wav").
            text: Text to synthesize.
            kwargs: Additional keyword arguments.
        Kwargs:
            audio: Raw WAV bytes (None until synthesized).
            voicemodel: VoiceModel used for synthesis.
        """
        self.path = path
        self.text = text
        self.audio = kwargs.get("audio")
        self.voicemodel = kwargs.get("voicemodel")

    def __repr__(self) -> str:
        """Return a string representation of the SoundFile."""
        audio_status = "yes" if self.audio else "no"
        return f"<SoundFile path={self.path!r} text={self.text!r} audio={audio_status}>"
