"""Module for managing voice pack configurations.

Voicepacks represent collections of sound/filename pairs, along with metadata used for
packaging and distribution, and a VoiceModel configuration for TTS synthesis.
"""

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from openvoicepacks.voicemodel import VoiceModel


class VoicePack(BaseModel, validate_assignment=True, arbitrary_types_allowed=True):
    """Represents voice pack configuration for OpenVoicePacks, initialised from a dict.

    This is the main wrapper class for voice packs in OpenVoicePacks. It holds metadata
    about the voice pack, a nested dictionary of sounds, and an optional VoiceModel
    configuration for TTS synthesis.

    Attributes:
        ovp_schema (int): Schema version, for future use.
        name (str): Name of voice pack.
        description (str): Voice pack description (optional).
        creator (str): Creator name (optional).
        contact (str): Contact information (optional).
        packname (str): Filename (optional), defaults to name with underscores.
        model (VoiceModel | None): Optional VoiceModel configuration.
        sounds (dict): Nested dictionary of sounds.
        creation_date (datetime): Timestamp of creation.
    """

    name: str
    ovp_schema: int = 1
    description: str = ""
    creator: str = ""
    contact: str = ""
    model: VoiceModel | None = None
    packname: str = Field(default_factory=lambda data: data["name"].replace(" ", "_"))
    sounds: dict = Field(default={}, repr=False)
    creation_date: datetime = Field(default=datetime.now(UTC), repr=False)

    def _flatten_sounds(
        self, d: dict, parent_keys: list[str] | None = None
    ) -> list[tuple[str, str]]:
        """Recursively flattens a nested dict into a list of (key_path, value) tuples.

        Key path is joined by '/' and directories are made uppercase to conform to
        EdgeTX/OpenTX conventions.
        """
        if parent_keys is None:
            parent_keys = []

        for i, k in enumerate(parent_keys):
            parent_keys[i] = k.upper()  # Ensure directory keys are uppercase
        items = []
        for k, v in d.items():
            key_str = str(k)
            new_keys = [*parent_keys, key_str]
            if isinstance(v, dict):
                items.extend(self._flatten_sounds(v, new_keys))
            else:
                key_path = "/".join(new_keys)
                items.append((key_path, v))
        return items

    def worklist(self) -> list[tuple[str, str]]:
        """Return a flattened list of all sounds in the voice pack.

        Each item is a tuple of (key_path, value) where key_path is the
        full path to the sound joined by '/'.
        """
        return self._flatten_sounds(self.sounds)
