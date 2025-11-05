"""Piper TTS provider plugin for OpenVoicePacks."""

import logging
from pathlib import Path
from typing import ClassVar

import piper
import piper.download_voices

from openvoicepacks.audio import AudioData
from openvoicepacks.providers import Provider, VoiceModelProtocol
from openvoicepacks.utils import json_from_url, metadata

_logger = logging.getLogger(__name__)


class Piper(Provider):
    """Piper text-to-speech service client.

    Provides speech synthesis using local Piper models.

    Attributes:
        install_dir (str): Directory where Piper voice models are installed.
            Defaults to '.cache/piper'.
    """

    description: ClassVar[str] = "Piper TTS provider using local ONNX models."
    version: ClassVar[str] = metadata["version"]
    provider: ClassVar[str] = "piper"
    capabilities: ClassVar[set[str]] = {"text"}
    default_option: ClassVar[str] = "medium"
    valid_options: ClassVar[set[str]] = {"x_low", "low", "medium", "high"}

    install_dir: str = ".cache/piper"

    # TODO: Validate that install_dir base dir exists and is writable.

    # TODO: Add in more filtering options.
    # TODO: Implement in download_voice().
    # def list_voices(self, family=None, region=None) -> list:
    #     """Return a list of available Piper voice models.

    #     Returns:
    #         list:
    #             A list of available Piper voice model IDs.

    #     """
    #     with urlopen(piper.download_voices.VOICES_JSON) as response:
    #         voices_dict = json.load(response)

    #     # Return only the voice IDs with quality of medium
    #     filtered_list = list(
    #         filter(
    #             lambda x: voices_dict[x].get("qual") == "medium", voices_dict.keys()
    #         )
    #     )

    #     # Further filter by language family and region if specified
    #     if family:
    #         filtered_list = list(
    #             filter(
    #                 lambda x: voices_dict[x]
    #                 .get("language")
    #                 .get("family")
    #                 == family,
    #                 filtered_list,
    #             )
    #         )
    #         if region:
    #             filtered_list = list(
    #                 filter(
    #                     lambda x: voices_dict[x].get("language").get("region")
    #                     == region,
    #                     filtered_list,
    #                 )
    #             )
    #     return sorted(filtered_list)

    def _synthesise(self, text: str, model: VoiceModelProtocol) -> AudioData:
        """Synthesise speech data using Piper TTS service.

        Args:
            text (str): The text phrase to be synthesised.
            model (VoiceModel): VoiceModel object representing the voice model to use.

        Returns:
            AudioData: AudioData object containing the audio byte data and sample rate.
        """
        # FIXME: Format the model string correctly.
        language = model.language.replace("-", "_")  # Piper expects underscores
        model_name = f"{language}-{model.voice}-{model.option}"

        # Download the voice model if not already available
        # TODO: Consider moving model_path to a method.
        model_path = Path(f"{self.install_dir}/{model_name}.onnx")
        if not model_path.exists():
            _logger.info("Voice model not found, downloading...")
            self.download_voice(model_name)

        # Perform synthesis
        piper_voice: piper.PiperVoice = piper.PiperVoice.load(model_path)
        response: piper.SynthesisResult = next(
            piper_voice.synthesize(
                text,
                piper.SynthesisConfig(
                    volume=1.0,
                    length_scale=1.0,
                    noise_scale=1.0,
                    noise_w_scale=1.0,
                    normalize_audio=False,
                ),
            ),
        )

        # Return the audio data as a AudioData object (16-bit PCM)
        _logger.info('Successfully completed synthesis of "%s".', text)
        return AudioData(data=response.audio_int16_bytes, rate=response.sample_rate)

    def download_voice(self, model_name: str) -> None:
        """Download a voice model for Piper TTS.

        Args:
            model_name (str): The name of the voice model to download.
        """
        _logger.debug('Ensuring voice model "%s" is available.', model_name)

        # Check if the model is available for download
        voices_dict = json_from_url(piper.download_voices.VOICES_JSON)
        if model_name not in sorted(voices_dict.keys()):
            msg = f'Voice model "{model_name}" is not available.'
            _logger.error(msg)
            raise ValueError(msg)

        # Download the voice model
        _logger.info('Downloading voice model "%s".', model_name)
        install_dir: Path = Path(self.install_dir)
        install_dir.mkdir(parents=True, exist_ok=True)
        piper.download_voices.download_voice(model_name, download_dir=install_dir)


PROVIDER = Piper
