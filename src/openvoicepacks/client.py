"""Module for CLI interface."""

import click

from openvoicepacks.plugin_registry import providers as ovp_providers
from openvoicepacks.utils import metadata
from openvoicepacks.voicemodel import VoiceModel
from openvoicepacks.voicepack import VoicePack


@click.group()
def ovp() -> None:
    """OpenVoicePacks command line interface.

    Generate and customize complete voice packs for OpenTX and EdgeTX radios.
    """


@click.command()
@click.option(
    "-s", "--short", default=False, is_flag=True, help="Display short version."
)
def version(short: bool) -> None:
    """Display the OpenVoicePacks version."""
    msg = metadata["version"] if short else f"{metadata['name']} {metadata['version']}"
    click.echo(msg)


@click.command()
def providers() -> None:
    """List registered providers."""
    if not ovp_providers:
        click.echo("No TTS providers registered.")
        return
    click.echo("Registered TTS providers:")
    for provider in ovp_providers.values():
        msg = "".join(
            (
                f"- {provider.__name__} ",
                f"({provider.provider} {provider.version}): {provider.description}",
            )
        )
        click.echo(msg)


_CLI = {
    "create": {
        "template": {
            "help": "Template voice pack to base the voice pack on.",
        },
    }
}

provider_choices = ["generic"]
provider_choices.extend(p.provider for p in ovp_providers.values())


@click.command()
def merge() -> None:
    """Merge together multiple voicepacks."""
    raise NotImplementedError("Merge command not yet implemented.")


@click.command()
@click.option(
    "-n",
    "--name",
    prompt="Enter the name of the new voice pack",
    help="Name of the voice pack you are creating.",
)
@click.option(
    "-p",
    "--provider",
    prompt="TTS provider to use",
    type=click.Choice(provider_choices, case_sensitive=False),
    default=provider_choices[0],
    help="TTS provider for the voice pack.",
)
@click.option(
    "-o",
    "--packname",
    help="Filename for the voice pack (optional).",
)
def init(name: str, provider: str, packname: str) -> None:
    """Create a new voicepack config file.

    Create a new voicepack config file, allowing you to specify the sounds you want to
    include as well as the TTS provider and voice model to use, and some additional
    metadata.

    When options are not provided, you will be prompted to enter them interactively.
    """
    click.echo(f"Creating new voicepack '{name}' with provider '{provider}'...")
    model = VoiceModel(provider=provider, voice="default")
    voicepack = VoicePack(name=name, model=model, packname=(packname or name))
    file = voicepack.save()
    click.echo(f"Voicepack '{name}' created successfully at '{file}'.")


@click.command()
def check() -> None:
    """Check the validity of a voice pack file.

    This command verifies that the specified voice pack file is valid.
    It checks for correct structure, required fields, and proper formatting.

    Filetypes supported: YAML, JSON, CSV.
    """
    raise NotImplementedError("Check command not yet implemented.")


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("-o", "--output", default=".", help="Output directory.")
@click.option(
    "-d",
    "--dry-run",
    show_default=True,
    is_flag=True,
    help="Perform a dry run without actual processing.",
)
@click.option(
    "-z",
    "--zip",
    show_default=True,
    is_flag=True,
    help="Output voicepack as a zip file.",
)
def build(filepath: click.Path, output: str, dry_run: bool, compress: bool) -> None:
    """Build an installable voice pack from a config file.

    Filepath: Can be a file containing YAML, JSON, or CSV data.
    """
    click.echo(filepath)


ovp.add_command(version)
ovp.add_command(providers)
ovp.add_command(init)
ovp.add_command(merge)
ovp.add_command(check)
ovp.add_command(build)
