"""AWS Polly TTS provider for OpenVoicePacks."""

import logging
from typing import ClassVar

import boto3

from openvoicepacks.audio import AudioData
from openvoicepacks.voicemodel import VoiceModel

from .base import Provider

_logger = logging.getLogger(__name__)


class Polly(Provider):
    """AWS Polly text-to-speech service client.

    Provides speech synthesis using AWS Polly cloud service.

    Args:
        session (boto3.session.Session, optional):
            A boto3 session object. If not provided, a default session is created.
    """

    provider: ClassVar[str] = "polly"
    capabilities: ClassVar[set[str]] = {"text", "ssml"}
    session: boto3.session.Session = boto3.session.Session()

    def __init__(self, session: boto3.session.Session = None) -> None:
        """Initialise the Polly TTS provider.

        Args:
            session (boto3.session.Session, optional):
                A boto3 session object. If not provided, a default session is created.
        """
        # Override the default session if one is provided
        if session:
            self.session = session

        # Authenticate to AWS
        sts = self.session.client("sts")
        caller = sts.get_caller_identity()
        _logger.info("Authenticated to AWS as '%s'.", caller["Arn"])
        self._client = self.session.client("polly")

    def _synthesise(self, text: str, model: VoiceModel) -> AudioData:
        """Synthesise speech data using AWS Polly.

        Args:
            text (str): The (optionally SSML-enabled) text phrase to be synthesised.
            model (VoiceModel): The VoiceModel object representing the voice model to use.

        Returns:
            AudioData: A AudioData object containing the audio byte data and sample rate.
        """
        # FIXME: SSML may not work with all voice engines. This may need to be moved to
        # the VoiceModel object so users can provide their own SSML when needed.
        # NOTE: Now that we have the capabilities field, we can check if the voice supports SSML.
        # Regex to check string: (</*[a-z =_0-9"]+/*>)
        ssml = f'<speak>{text}<break strength="weak"/></speak>'
        sample_rate = 16000
        language = model.language.replace("_", "-")  # Polly expects hyphens

        # Perform synthesis
        response: dict = self._client.synthesize_speech(
            Text=ssml,
            VoiceId=model.voice.capitalize(),
            LanguageCode=language,
            Engine=model.option,
            TextType="ssml",
            OutputFormat="pcm",
        )

        # Return the audio data as a AudioData object (16-bit PCM)
        _logger.info('Successfully completed synthesis of "%s".', text)
        return AudioData(data=response["AudioStream"].read(), rate=sample_rate)
