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

import locale
from collections.abc import Callable, Generator

import pytest

from openvoicepacks.providers import Provider
from openvoicepacks.voicemodel import VoiceModel


@pytest.fixture
def set_locale() -> Generator[Callable[[str], None]]:
    """Fixture to temporarily set and restore locale."""
    orig = locale.setlocale(locale.LC_ALL)

    def _set(new_locale: str) -> None:
        locale.setlocale(locale.LC_ALL, new_locale)

    yield _set
    locale.setlocale(locale.LC_ALL, orig)


class TestVoiceModel:
    """Tests for the VoiceModel class."""

    def test_full(self) -> None:
        """Given full valid input, creates VoiceModel."""
        vm = VoiceModel(
            provider="generic", voice="Test", language="en_GB", option="standard"
        )
        assert vm.provider.__class__ == Provider.__class__

    def test_locale(self, set_locale: Callable[[str], None]) -> None:
        """Given no language, system locale is used."""
        lang = "en_GB"
        set_locale(lang)
        vm = VoiceModel(
            provider="generic",
            voice="Test",
        )
        assert vm.language == lang

    def test_option(self) -> None:
        """Given no option, provider default is used."""
        vm = VoiceModel(
            provider="generic",
            voice="Test",
        )
        assert vm.option == "standard"


class TestVoiceModelValidation:
    """Tests for VoiceModel class validation."""

    def test_invalid_provider(self) -> None:
        """Given an unknown provider, wrapper raises ValueError."""
        with pytest.raises(ValueError, match="Unknown provider: test"):
            VoiceModel(voice="test", provider="test")

    def test_invalid_option(self) -> None:
        """Given an invalid option, a ValueError is raised."""
        option = "invalid"
        # This only needs to be tested for one provider as each provider
        # inherits from the same base class which performs the validation.
        with pytest.raises(ValueError, match=f"Invalid option: {option}"):
            VoiceModel(voice="Test", provider="generic", option=option)

    @pytest.mark.parametrize(
        "language", ["en", "enGB", "en_GB_en", "en--GB", "_GB", "en_", "en_GB.UTF8"]
    )
    def test_invalid_language_format(self, language: str) -> None:
        """Given an invalid language format, a ValueError is raised."""
        with pytest.raises(ValueError, match="must be in the format"):
            VoiceModel(voice="Test", provider="generic", language=language)
