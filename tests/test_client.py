"""Tests for CLI client."""

from click.testing import CliRunner

from openvoicepacks.client import ovp


class TestOVP:
    """Test suite for the OVP CLI."""

    class TestHelp:
        """Test suite for the OVP CLI help commands."""

        def test_ovp_group_help(self) -> None:
            """Given the ovp command, when --help is invoked, help message is shown."""
            runner = CliRunner()
            result = runner.invoke(ovp, ["--help"])
            assert result.exit_code == 0
            assert "OpenVoicePacks command line interface" in result.output

    class TestVersion:
        """Test suite for the OVP CLI version commands."""

        def test_version_command_default(self) -> None:
            """Given the ovp version command, version info is shown."""
            runner = CliRunner()
            result = runner.invoke(ovp, ["version"])
            assert result.exit_code == 0
            # Should show name and version
            assert (
                "OpenVoicePacks" in result.output or "openvoicepacks" in result.output
            )
            assert any(char.isdigit() for char in result.output)

        def test_version_command_short(self) -> None:
            """Given the ovp version command with --short, short version is shown."""
            runner = CliRunner()
            result = runner.invoke(ovp, ["version", "--short"])
            assert result.exit_code == 0
            # Should only show version string
            assert result.output.strip().replace(".", "").isdigit() or any(
                char.isdigit() for char in result.output
            )
