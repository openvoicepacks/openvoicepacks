"""Invoke tasks using the Invoke library.

This module defines a set of tasks for managing the development workflow of the project,
including formatting, linting, testing, documentation generation, building, and
publishing.

Each task is decorated with `@task` from the Invoke library, allowing for easy execution
from the command line. Tasks can be run individually or as part of a sequence, and
they support various options to customize their behavior.

Usage:
    - To run a specific task, use the command:
        inv <task_name> [options]
    - To see a list of available tasks, use:
        inv --list
    - To get help on a specific task, use:
        inv <task_name> --help
"""

import os

from invoke import Context, task

OCI_IMAGE_NAME = "openvoicepacks"
OCI_BUILDER = os.getenv("OCI_BUILDER", "buildah")


# TODO: Consider swapping fix flag to --check for fmt and lint.
@task(
    aliases=(["format"]),
    help={"fix": "Automatically fix formatting issues."},
)
def fmt(command: Context, *, fix: bool = True) -> None:
    """Format code."""
    cmd = "ruff format"
    if not fix:
        cmd += " --diff"
    command.run(f"{cmd}", pty=True)


@task(help={"fix": "Automatically fix linting issues."})
def lint(command: Context, *, fix: bool = True) -> None:
    """Run lint tests."""
    cmd = "ruff check"
    if fix:
        cmd += " --fix"
    command.run(cmd, pty=True)


@task(aliases=(["coverage"]))
def cov(command: Context) -> None:
    """Run code coverage report generation."""
    command.run("coverage report -m", pty=True)


@task(
    help={
        "all": "Run full test suite, including slow tests.",
        "benchmark": "Run benchmarks for the test suite.",
    },
)
def unit(command: Context, *, all_: bool = False, benchmark: bool = False) -> None:
    """Run unit tests."""
    cmd = "pytest"
    if not all_:
        cmd += " -m 'not slow'"
    if benchmark:
        cmd += " --durations=5 --durations-min=1.0"
    command.run(cmd, pty=True)


@task(aliases=["pre-commit"])
def pre(command: Context) -> None:
    """Run pre-commit checks."""
    command.run("pre-commit run --all-files", pty=True)


@task(
    help={
        "all": "Run full test suite, including slow tests.",
        "fix": "After checking formatting and linting, make the necessary changes.",
    },
)
def test(command: Context, *, all_: bool, fix: bool) -> None:
    """Run full test suite."""
    fmt(command, fix=fix)
    lint(command, fix=fix)
    unit(command, all_=all_)
    cov(command)


@task
def dependencies(command: Context) -> None:
    """Install dependencies."""
    command.run("uv sync --all-groups", pty=True)


@task
def update(command: Context) -> None:
    """Update dependencies."""
    command.run("uv lock --upgrade --all-groups", pty=True)


@task
def clean(command: Context) -> None:
    """Clean development environment, removing temporary files."""
    command.run("find . -type d -name '__pycache__' -exec rm -rf {} +")
    command.run("rm -rf dist/ site/ .pytest_cache/ .cache/plugin/social/*.png")
    # These will probably go away
    command.run("rm -rf resources/")


@task(
    help={"serve": "Serve documentation on local HTTP server."},
)
def docs(command: Context, *, serve: bool = False) -> None:
    """Generate documentation."""
    if serve:
        command.run("mkdocs serve --livereload", pty=True)
    else:
        command.run("mkdocs build", pty=True)


@task(
    clean,
    help={
        "wheel": "Build package wheel.",
        "sdist": "Build package source distribution.",
        "container": "Build OCI container image.",
    },
)
def build(
    command: Context,
    *,
    wheel: bool = False,
    sdist: bool = False,
    container: bool = False,
) -> None:
    """Build distributables. Defaults to building sdist and wheel."""
    if wheel or sdist:
        cmd = "uv build"
        if wheel:
            cmd += " --wheel"
        if sdist:
            cmd += " --sdist"
        command.run(cmd, pty=True)
    # FIXME: Due to calling clean first, container build will always fail unless wheel
    # or dist is also built.
    if container:
        command.run(
            f"{OCI_BUILDER} build -t {OCI_IMAGE_NAME}:$(uv version --short) .", pty=True
        )


@task(
    help={"short": "Only show version number."},
)
def version(command: Context, *, short: bool = False) -> None:
    """Display package version."""
    cmd = "uv version"
    if short:
        cmd += " --short"
    command.run(cmd, pty=True)


@task
def bump(command: Context) -> None:
    """Bump package version."""
    cmd = "cz bump"
    command.run(cmd, pty=True)


@task
def commit(command: Context) -> None:
    """Commit changes in Git using Commitizen."""
    cmd = "cz commit -- --signoff"
    command.run(cmd, pty=True)


@task
def publish(command: Context) -> None:
    """Publish package to remote repository."""
    command.run("uv publish", pty=True)


@task
def deploy(command: Context) -> None:
    """Full clean build and publish."""
    clean(command)
    build(command)
    publish(command)


@task(default=True)
def run(command: Context) -> None:
    """Run the module's main object."""
    command.run("python -m openvoicepacks", pty=True)


if __name__ == "__main__":
    run(None)
