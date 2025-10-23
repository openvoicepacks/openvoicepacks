"""Module for managing voice pack configurations and supporting utilities.

Voicepacks represent collections of sound/filename pairs, along with metadata used for
packaging and distribution, and a VoiceModel configuration for TTS synthesis.

This module includes the VoicePack class, which encapsulates all relevant data and
methods for handling voice packs, as well as utility functions for converting from CSV
and YAML formats into VoicePack objects.
"""

import csv
import io
from datetime import UTC, datetime
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, field_validator

from openvoicepacks import template_env
from openvoicepacks.audio import SoundFile
from openvoicepacks.voicemodels import VoiceModel


class VoicePack(BaseModel, validate_assignment=True, arbitrary_types_allowed=True):
    """Represents voice pack configuration for OpenVoicePacks.

    This is the main class for voice packs in OpenVoicePacks. It holds metadata about
    the voice pack, a nested dictionary of sounds, and an optional VoiceModel
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
        based_on (list[str]): Optional reference to parent voice packs.
    """

    name: str
    ovp_schema: int = 1
    description: str = ""
    creator: str = ""
    contact: str = ""
    model: dict | VoiceModel | None = None
    packname: str = Field(default_factory=lambda data: data["name"].replace(" ", "_"))
    sounds: dict = Field(default={}, repr=False)
    creation_date: datetime = Field(default=datetime.now(UTC), repr=False)
    based_on: list[str] = Field(default=[], repr=False)

    @field_validator("packname", mode="after")
    @classmethod
    def _packname(cls, v: str) -> str:
        """Ensure the packname is valid and properly formatted.

        Args:
            v (str): The packname to validate.

        Returns:
            str: The validated packname.
        """
        v = v.replace(" ", "_").lower()  # Replace spaces with underscores and lowercase
        p = Path(v)
        return p.with_suffix("").name  # Ensure no file extension

    def _flatten_sounds(
        self, d: dict, parent_keys: list[str] | None = None
    ) -> list["SoundFile"]:
        """Recursively flattens a nested dict into a list of SoundFile objects.

        Key path is joined by '/' and directories are made uppercase to conform to
        EdgeTX/OpenTX conventions.

        Args:
            d (dict): The current level of the sounds dictionary.
            parent_keys (list[str] | None): List of parent keys for path construction.
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
                items.append(SoundFile(path=key_path, text=v))
        return items

    def worklist(self) -> list[SoundFile]:
        """Return a flattened list of all sounds in the voice pack.

        Each item is a SoundFile object representing the sound.
        """
        # return self._flatten_sounds(self.sounds)
        return self._flatten_sounds(self.sounds)

    def yaml(self) -> str:
        """Return the voice pack data as a YAML document."""
        template = template_env.get_template("voicepack.yaml.jinja")
        return template.render(voicepack=self)

    def save(self, filename: str | None = None) -> str:
        """Save the voicepack data to a YAML file.

        Args:
            filename (str): The filename to save the voice pack to.

        The filename is derived from the packname attribute with a .yaml extension if
        not specified.

        Returns:
            str: The filename the voice pack was saved to.
        """
        # Default filename to packname.yaml if not specified.
        if not filename:
            filename = f"{self.packname}.yaml"

        with Path.open(filename, "w", encoding="utf-8") as f:
            f.write(self.yaml())
        return filename

    def merge(self, parent: object) -> None:
        """Merge another VoicePack into this one.

        Args:
            parent (VoicePack): The parent VoicePack to merge from.

        The sounds from the parent VoicePack are merged into this one. Existing sounds
        in this VoicePack take precedence over those in the parent.
        """

        def merge_dicts(primary: dict, parent: dict) -> dict:
            """Recursively merge two nested dictionaries.

            Args:
                primary (dict): The first dictionary (takes precedence).
                parent (dict): The second dictionary.

            Returns:
                dict: The merged dictionary.
            """
            result = dict(parent)  # Start with parent's keys and values
            for k, v in primary.items():
                if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                    result[k] = merge_dicts(v, result[k])
                else:
                    result[k] = v
            return result

        self.sounds = merge_dicts(self.sounds, parent.sounds)
        self.based_on.append(parent.packname)


def voicepack_from_csv(csv_data: dict) -> VoicePack:
    """Convert CSV data from EdgeTX/OpenTX community to a VoicePack object.

    Args:
        csv_data (dict): The CSV data to convert.

    Returns:
        VoicePack: The converted VoicePack object.

    Raises:
        ValueError: If the CSV data is not formatted correctly.
    """
    # Since the CSV format does not include metadata, we set some defaults.
    data = {
        "ovp_schema": 1,
        "name": "Unnamed",
        "description": "Imported from CSV",
        "sounds": {},
    }

    if isinstance(csv_data, str):
        csv_data = io.StringIO(csv_data)

    # Load CSV data as a list of dicts where each field is a key.
    csv_dict = csv.DictReader(csv_data)

    # Check CSV data is in the correct format.
    required_fields = ["Filename", "Path", "Translation"]
    for field in required_fields:
        if field not in csv_dict.fieldnames:
            raise ValueError("CSV not formatted correctly")

    # Convert the CSV data into the standard OSP format.
    for row in csv_dict:
        filename = row.get("Filename").replace(".wav", "")
        string = row.get("Translation")
        path = row.get("Path").lower()

        # If there is a path attribute set, nest the values inside that.
        if len(path) > 0:
            if path not in data["sounds"]:
                data["sounds"][path] = {}
            data["sounds"][path][filename] = string
        else:
            data["sounds"][filename] = string

    return VoicePack.model_validate(data)


def voicepack_from_yaml(yaml_data: dict) -> VoicePack:
    """Convert YAML data to a VoicePack object.

    Args:
        yaml_data (dict): The YAML data to convert.

    Returns:
        VoicePack: The converted VoicePack object.
    """
    data = yaml.safe_load(yaml_data)
    return VoicePack.model_validate(data)
