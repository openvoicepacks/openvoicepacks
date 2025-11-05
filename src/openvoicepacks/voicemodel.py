"""Module for managing voice models from various TTS providers.

A VoiceModel represents a specific voice configuration for a TTS provider,
encapsulating attributes like voice name/ID, language, and any provider-specific
options.

It allows a standardised interface for interacting with different TTS providers.
"""

import locale
import re

from attr import Attribute, define, field

from openvoicepacks.plugin_registry import get_provider_class


@define
class VoiceModel:
    """Wrapper for provider-specific voice models."""

    provider: str = field(converter=get_provider_class)
    voice: str = field(converter=str.lower)
    language: str = field(converter=str)
    option: str = field(converter=str.lower)
    extras: dict = field(factory=dict)

    @option.default
    def _set_default_option(self) -> str:
        """Set the default option based on the provider's default."""
        return self.provider.default_option

    @option.validator
    def _check_option(self, attr: Attribute, value: str) -> None:
        """Validate option field against provider-specific valid options.

        Args:
            attr: The attribute being validated.
            value (str): The option value to validate.

        Raises:
            ValueError: If the option is not valid for the provider.
        """
        if value.lower() not in self.provider.valid_options:
            msg = f"Invalid {attr.name}: {value}"
            raise ValueError(msg)

    @language.default
    def _set_default_language(self) -> str:
        """Set the default language based on the system locale."""
        lang, _ = locale.getlocale()
        return lang if lang else "en_US"

    @language.validator
    def _check_language(self, attr: Attribute, value: str) -> None:
        """Ensure the language code is valid and properly formatted using regex.

        Accepts formats like 'en_GB' or 'en-GB'.

        Args:
            attr: The attribute being validated.
            value (str): The language code to validate.

        Raises:
            ValueError: If the language code is not in the correct format.
        """
        # Match two lowercase letters, underscore or hyphen, two uppercase letters.
        # This ensures that strings are valid ISO codes (two-letter ISO 639-1 for
        # language and two-letter ISO 3166-1 alpha-2 for region).
        if not re.match(r"^[a-z]{2}[-_][A-Z]{2}$", value):
            msg = f"{attr.name} must be in the format 'xx_YY' or 'xx-YY'"
            raise ValueError(msg)
