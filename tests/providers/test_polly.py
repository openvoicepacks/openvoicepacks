"""Test suite for the Polly TTS provider.

Only tests that are specific to Polly should go here. Most provider tests should be in
tests/providers/test_all.py to ensure consistency across all providers.

Current tests:
- AWS session handling.
- Handling invalid SSML input.
"""

import boto3
import botocore.exceptions
import pytest

from openvoicepacks.providers import Polly
from openvoicepacks.voicemodels import VoiceModel


class TestPolly:
    """Test suite for the Polly TTS provider"""

    @pytest.fixture
    def polly_model(self) -> VoiceModel:
        """Given a test, returns a Polly voice object."""
        return VoiceModel(
            voice="Amy",
            language="en_GB",
            provider="polly",
            option="standard",
        )

    class TestSession:
        """Test suite for AWS session handling in Polly."""

        def test_existing_session(self) -> None:
            """Given an existing AWS session, Polly client uses it."""
            session = boto3.Session()
            polly = Polly(session=session)
            assert polly.session is session, (
                "Polly client did not use existing session."
            )

        def test_invalid_session(self) -> None:
            """Given invalid AWS credentials, an error is raised."""
            session = boto3.session.Session(
                aws_access_key_id="dummy",  # Require dummy credentials for testing
                aws_secret_access_key="dummy",  # NOQA: S106
                aws_session_token="dummy",  # NOQA: S106
            )
            with pytest.raises(
                (
                    botocore.exceptions.NoCredentialsError,
                    botocore.exceptions.ClientError,
                ),
            ):
                Polly(session=session)

    class TestSynthesise:
        """Test suite for the synthesise() method in Polly."""

        def test_invalid_string(self, polly_model: VoiceModel) -> None:
            """Given an invalid string, synthesise raises an error."""
            instance = Polly()
            with pytest.raises(
                (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError),
            ):
                instance.synthesise("<ssml_invalid_tag>", polly_model)
