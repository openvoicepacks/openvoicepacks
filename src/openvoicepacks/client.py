"""Module for CLI interface."""

import click

from openvoicepacks import metadata


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


ovp.add_command(version)

if __name__ == "__main__":
    ovp()
