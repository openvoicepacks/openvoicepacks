"""Module for managing voice models from various TTS providers.

A VoiceModel represents a specific voice configuration for a TTS provider,
encapsulating attributes like voice name/ID, language, and any provider-specific
options.

It allows a standardised interface for interacting with different TTS providers.

```mermaid
classDiagram
    class VoiceModel {
        <<Interface>>
        +_model: PiperVoiceModel or PollyVoiceModel
        +__init__(**data)
        +__getattr__(name)
        +dict()
    }
    class BaseVoiceModel {
        <<Abstract>>
        +voice: str
        +language: str
        #valid_options: list
        -validate_option(v: str) -> str
    }
    class PiperVoiceModel {
        <<Abstract>>
        +provider: str = "piper"
        +option: str = "medium"
        #valid_options: list
    }
    class PollyVoiceModel {
        <<Abstract>>
        +provider: str = "polly"
        +option: str = "standard"
        #valid_options: list
    }
    VoiceModel --> PiperVoiceModel : wraps
    VoiceModel --> PollyVoiceModel : wraps
    PiperVoiceModel --|> BaseVoiceModel : inherits
    PollyVoiceModel --|> BaseVoiceModel : inherits
```
"""

from typing import ClassVar

from pydantic import BaseModel, field_validator


class VoiceModel:
    """Wrapper for provider-specific voice models.

    This class wraps around provider-specific voice model classes to provide a unified
    interface. It delegates attribute access and methods to the underlying provider
    model.

    Arguments:
        **data: The keyword arguments to initialize the appropriate voice model.

    Attributes:
        _model (VoiceModelBase): The underlying provider-specific voice model instance.
    """

    def __init__(self, **data: object) -> None:
        """Initialise the wrapper and delegate to the correct provider model."""
        provider = data.get("provider")
        match provider:
            case "polly":
                self._model = PollyVoiceModel(**data)
            case "piper":
                self._model = PiperVoiceModel(**data)
            case "generic":
                self._model = BaseVoiceModel(**data)
            case _:
                msg = f"Unknown provider: {provider}"
                raise ValueError(msg)

    def __getattr__(self, name: str) -> object:
        """Delegate attribute access to the underlying provider model."""
        return getattr(self._model, name)

    # NOTE: It might be necessary to also add _setattr__ if we want to allow
    # modifying attributes of the underlying model.

    def dict(self) -> dict:
        """Return the dict representation of the underlying provider model."""
        return self._model.model_dump()


class BaseVoiceModel(BaseModel):
    """Base model for voice attributes and language validation.

    This class should be inherited by provider-specific voice model classes.
    """

    # NOTE: It might be better to store some of this in the provider class,
    # and then pull it from there, rather than duplicating in each voice model.
    provider: str
    option: str
    voice: str
    language: str
    valid_options: ClassVar[set[str]] = {""}

    @field_validator("voice", mode="after")
    @classmethod
    def _lowercase_voice(cls, v: str) -> str:
        """Ensure voice field is always lowercase."""
        return v.lower()

    @field_validator("language", mode="after")
    @classmethod
    def _language(cls, v: str) -> str:
        """Ensure the language code is valid and properly formatted.

        Accepts formats like 'en_GB' or 'en-GB'.

        Arguments:
            v (str): The language code to validate.

        Returns:
            str: The validated language code.

        Raises:
            ValueError: If the language code is not in the correct format.
        """
        lang_parts = v.replace("-", "_").split("_")
        lang_parts_expected = 2
        # TODO: Check that parts are valid ISO codes. Should be two-letter ISO 639-1 for
        # language and two-letter ISO 3166-1 alpha-2 for region.
        if len(lang_parts) != lang_parts_expected or not all(lang_parts):
            raise ValueError("language must be in the format 'xx_YY' or 'xx-YY'")
        return v

    @field_validator("option", mode="before")
    @classmethod
    def _validate_option(cls, v: str) -> str:
        """Validate Polly option field.

        If no option is provided, the first valid option is used as the default.

        Arguments:
            v (str): The option value to validate.

        Returns:
            str: The validated option value.

        Raises:
            ValueError: If the option is not valid.
        """
        v = v.lower()
        if v not in cls.valid_options:
            msg = f"Invalid option: {v}"
            raise ValueError(msg)
        return v


class PollyVoiceModel(BaseVoiceModel):
    """Voice model for Amazon Polly provider.

    Attributes:
        voice (str): The voice name/ID.
        provider (str): The TTS provider, always 'polly' for this class.
        language (str): The language code in the format 'xx_YY' or 'xx-YY'.
        option (str): The type of Polly model.
            One of 'standard', 'neural', 'long-form', 'generative'.
    """

    provider: str = "polly"
    option: str = "standard"
    valid_options: ClassVar[set[str]] = {
        "standard",
        "neural",
        "long-form",
        "generative",
    }


class PiperVoiceModel(BaseVoiceModel):
    """Voice model for Piper provider.

    Attributes:
        voice (str): The voice name/ID.
        provider (str): The TTS provider, always 'piper' for this class.
        language (str): The language code in the format 'xx_YY' or 'xx-YY'.
        option (str): The quality option for the Piper model.
            One of 'x_low', 'low', 'medium', 'high'.
    """

    provider: str = "piper"
    option: str = "medium"
    valid_options: ClassVar[set[str]] = {"medium", "x_low", "low", "high"}
