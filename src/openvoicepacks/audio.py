"""Module for audio data handling in OpenVoicePacks."""

import logging
from dataclasses import dataclass
from pathlib import Path

from pydub import AudioSegment

from openvoicepacks.utils import validate_file_path

_logger = logging.getLogger(__name__)


@dataclass
class AudioData:
    """Encapsulates audio data and its properties for encoding/decoding.

    Args:
        data (bytes): The raw audio byte data.
        rate (int, optional): The sample rate of the audio data.
            Defaults to 16000 Hz.
        width (int, optional): The sample width in bytes.
            Defaults to 2 bytes (16-bit audio).
        channels (int, optional): The number of audio channels.
            Defaults to 1 (mono).
    """

    data: bytes
    rate: int = 16000
    width: int = 2
    channels: int = 1

    def write_wav(self, file: str | Path, output_rate: int = 16000) -> str | Path:
        """Write WAVE-encoded audio data to a file path or file-like object.

        Args:
            file (str or Path): File path or file-like object to write audio data to.
            output_rate (int, optional): The sample rate to write the audio data at.
                Defaults to 16000 Hz.

        Returns:
            str | Path: The file path or file-like object written to.
        """
        validate_file_path(file)
        if not isinstance(output_rate, int) or output_rate <= 0:
            raise ValueError("output_rate must be a positive integer")

        # Uses ffmpeg via pydub to write the WAV file
        # See: https://github.com/jiaaro/pydub/blob/master/API.markdown
        sound = AudioSegment(
            data=self.data,
            sample_width=self.width,
            frame_rate=self.rate,
            channels=self.channels,
        )
        sound.export(
            file,
            format="wav",
            bitrate="16k",
            parameters=["-ar", str(output_rate)],
        )
        _logger.debug('Wrote audio data to "%s"', str(file))
        return file


@dataclass
class SoundFile:
    """Represents a single sound asset, including text, audio, and path.

    Attributes:
        path: Relative path for output (e.g. "EN/hello.wav").
        text: Text to synthesize.
        audio: Audio data for the sound.
        voicemodel: Voice model used for synthesis.
    """

    path: str
    text: str
    audio: AudioData | None = None
    voicemodel: object | None = None

    def __repr__(self) -> str:
        """Return a string representation of the SoundFile."""
        audio_status = "yes" if self.audio else "no"
        return f"<SoundFile path={self.path!r} text={self.text!r} audio={audio_status}>"
