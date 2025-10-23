"""Unit tests for VoiceModel classes and wrapper in openvoicepacks.voice.

Most tests here are for validation and correct delegation to the appropriate
provider-specific VoiceModel class.

As these are mostly data classes, there is not much logic to test outside of
VoiceModelBase.

All testing should ideally be done through the VoiceModel wrapper class, and
not the provider-specific classes directly.

Current tests:
- Correct delegation to provider-specific classes.
- Validation of provider, option, and language format.
"""

from copy import deepcopy

import pytest
from pydantic_core import ValidationError

from openvoicepacks.voicemodels import (
    PiperVoiceModel,
    PollyVoiceModel,
    VoiceModel,
)

VALID_MODELS = [
    {
        "type": PollyVoiceModel,
        "data": {
            "voice": "Amy",
            "language": "en-GB",
            "provider": "polly",
            "option": "standard",
        },
    },
    {
        "type": PiperVoiceModel,
        "data": {
            "voice": "Alan",
            "language": "en_GB",
            "provider": "piper",
            "option": "medium",
        },
    },
]


@pytest.fixture(params=VALID_MODELS, ids=[m["type"].__name__ for m in VALID_MODELS])
def model_config(request: pytest.FixtureRequest) -> dict[str, object]:
    """Return a valid model config for testing."""
    return request.param


class TestVoiceModel:
    """Tests for the VoiceModel wrapper class."""

    def test_wrapper(self, model_config: object) -> None:
        """Given a valid config, wrapper delegates to correct class."""
        data = deepcopy(model_config["data"])
        vm = VoiceModel(**data)
        # Ensure voice is always lowercase in the output
        data["voice"] = data["voice"].lower()
        # Check all fields are correctly set
        assert vm.voice == data["voice"]
        assert vm.provider == data["provider"]
        assert vm.option == data["option"]
        assert vm.language == data["language"]
        assert isinstance(vm._model, model_config["type"])
        assert vm.dict() == data

    def test_option(self, model_config: object) -> None:
        """Given a config without 'option', the correct default is used."""
        data = deepcopy(model_config["data"])
        # Remove option from input data to test defaulting
        option = data["option"]
        data.pop("option", None)
        vm = VoiceModel(**data)
        assert vm.option == option


class TestVoiceModelValidation:
    """Tests for validation in the VoiceModel wrapper class."""

    def test_invalid_provider(self) -> None:
        """Given an unknown provider, wrapper raises ValueError."""
        with pytest.raises(ValueError, match="Unknown provider: test"):
            VoiceModel(
                voice="test", language="en_GB", provider="test", option="standard"
            )

    def test_invalid_option(self) -> None:
        """Given an invalid option, a ValidationError is raised."""
        option = "invalid"
        # This only needs to be tested for one provider as each provider
        # inherits from the same base class which performs the validation.
        with pytest.raises(ValidationError):
            VoiceModel(voice="Alan", provider="piper", language="en_GB", option=option)

    @pytest.mark.parametrize(
        "language", ["en", "enGB", "en_GB_en", "en--GB", "_GB", "en_"]
    )
    def test_invalid_language_format(self, language: str) -> None:
        """Given an invalid language format, a ValidationError is raised."""
        with pytest.raises(ValidationError):
            VoiceModel(voice="Alan", provider="piper", language=language)
