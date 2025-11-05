"""Base class for TTS providers.

Provides a standard interface for text-to-speech providers in OpenVoicePacks.
All providers should inherit from this class and implement the synthesise method.

"""

from typing import ClassVar, Protocol

from openvoicepacks.audio import AudioData


class VoiceModelProtocol(Protocol):
    """Protocol for VoiceModel objects used by TTS providers.

    This is used to ensure that all voice models have a consistent interface.

    Attributes:
        provider (str): The name of the TTS provider.
        voice (str): The voice identifier.
        language (str): The language code.
        option (str): Additional provider-specific options.
        extras (dict): Additional provider-specific parameters.
    """

    provider: str
    voice: str
    language: str
    option: str
    extras: dict


class Provider:
    """Base class for TTS providers.

    TTS provider classes should inherit from this and implement the _synthesise method
    as well as update the class variables.

    Class attributes:
        name (str): Name of the provider.
        description (str): Description of the provider.
        version (str): Version of the provider.
        provider (str): Unique identifier for the provider.
        capabilities (set): Set of capabilities supported by the provider.
    """

    description: ClassVar[str] = "A generic text-to-speech provider."
    version: ClassVar[str] = "local"
    provider: ClassVar[str] = "generic"
    capabilities: ClassVar[set[str]] = set()
    valid_options: ClassVar[set[str]] = {"standard"}
    default_option: ClassVar[str] = "standard"

    def check_text(self, text: str) -> None:
        """Check if the provided text is valid.

        Args:
            text (str): The text to check.
        """
        if not isinstance(text, str) or len(text) == 0:
            raise ValueError("Text must be a non-empty string")

    def check_model(self, model: VoiceModelProtocol) -> None:
        """Check if the provided model is valid for this provider.

        Args:
            model (VoiceModel): The VoiceModel object to check.
        """
        if model.provider is not self.__class__:
            msg = (
                f"Model must be compatible with this provider. "
                f"Got '{model.provider}', expected '{self.__class__}'"
            )
            raise ValueError(msg)

    def synthesise(self, text: str, model: VoiceModelProtocol) -> AudioData:
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
        self.check_model(model)

        # Synthesise and return audio data.
        return self._synthesise(text, model)

    def _synthesise(self, text: str, model: VoiceModelProtocol) -> AudioData:
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
