"""Base class for TTS providers.

Provides a standard interface for text-to-speech providers in OpenVoicePacks.
All providers should inherit from this class and implement the synthesise method.

"""

import logging
from typing import ClassVar

from openvoicepacks.audio import AudioData
from openvoicepacks.voicemodels import VoiceModel

_logger = logging.getLogger(__name__)


class ProviderError(Exception):
    """Custom exception for provider-related errors."""


class Provider:
    """Base class for TTS providers.

    TTS provider classes should inherit from this and implement the synthesise method.
    """

    provider: ClassVar[str] = "generic"
    capabilities: ClassVar[set[str]] = set()
    model: VoiceModel | None = None

    def check_text(self, text: str) -> None:
        """Check if the provided text is valid.

        Args:
            text (str): The text to check.
        """
        if not isinstance(text, str) or len(text) == 0:
            raise ValueError("Text must be a non-empty string")

    def check_model(self, model: VoiceModel) -> None:
        """Check if the provided model is valid for this provider.

        Args:
            model (VoiceModel): The VoiceModel object to check.
        """
        if not isinstance(model, VoiceModel):
            raise TypeError("Model must be a VoiceModel object")
        if model.provider != self.provider:
            msg = (
                f"Model must be compatible with this provider."
                f"Got '{model.provider}', expected '{self.provider}'"
            )
            raise ValueError(msg)

    def synthesise(self, text: str, model: VoiceModel = None) -> AudioData:
        """Synthesise speech from text using the specified VoiceModel object.

        Args:
            text (str): The text phrase to be synthesised.
            model (VoiceModel): VoiceModel object representing the voice model to use.

        Returns:
            AudioData: AudioData object containing the audio byte data and sample rate.

        Raises:
            ValueError: If text is not a non-empty string.
            TypeError: If voice is not a Voice object.
        """
        # Check input parameters.
        self.check_text(text)
        if model is None:
            if self.model is None:
                raise ValueError("No default voice set for this provider")
            _logger.debug("Using default voice: %s", self.model.voice)
            model = self.model
        self.check_model(model)

        # Synthesise and return audio data.
        return self._synthesise(text, model)

    def _synthesise(self, text: str, model: VoiceModel) -> AudioData:
        """Stub method for synthesising speech from text using a VoiceModel object.

        Subclasses must implement this method and output an AudioData object.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def process(self, path: str, *args: object, **kwargs: object) -> None:
        """Synthesise audio from text and write to the given file path.

        Args:
            path (str): The file path to write the output audio data to.
            *args: Additional positional arguments for synthesise().
            **kwargs: Additional keyword arguments for synthesise().
        """
        audio_data: AudioData = self.synthesise(*args, **kwargs)
        audio_data.write_wav(path)
