"""Module for CLI interface."""

import click

from openvoicepacks.plugin_registry import providers as ovp_providers
from openvoicepacks.utils import metadata


@click.group()
def ovp() -> None:
    """OpenVoicePacks command line interface."""


@click.command()
@click.option(
    "-s", "--short", default=False, is_flag=True, help="Display short version."
)
def version(short: bool) -> None:  # NOQA: FBT001
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


ovp.add_command(version)
ovp.add_command(providers)
