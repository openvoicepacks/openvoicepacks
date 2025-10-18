Contributing to OpenVoicePacks
==============================

Thank you for your interest in contributing to OpenVoicePacks! We welcome improvements, bug fixes, new features, and documentation updates. Please read the following guidelines to help keep the project consistent and maintainable.

## Getting Started

**Grab development tools**
- Install [uv](https://docs.astral.sh/uv/), which is used for Python package and project management.
- Install [ffmpeg](https://www.ffmpeg.org/) and ensure it is in your `PATH`.

**Clone the repository:**
```bash
git clone https://github.com/benfairless/openvoicepacks.git && cd openvoicepacks
```

**Install dependencies:**
```bash
# Python dependencies
uv sync --dev
# Pre-commit hooks
uv run pre-commit install
```

**Run tests:**
```bash
uv run inv lint
uv run inv fmt
uv run inv unit
```

> TIP: You can see all available commands for `invoke` by running `uv run inv --list`.

## Code Style & Standards

- Use modern Python (3.13+) features and type annotations.
- All public methods and functions must have input validation and clear docstrings.
- Docstrings should follow the Google style.
- Docstrings for tests should follow the format: `Given [x], expected result`.
- Run `uv run inv lint` and `uv run inv fmt` before submitting a PR.

## Making Changes

**Fork the repository** and create your branch:
```bash
git checkout -b feat/your-feature-name
```

- **Make your changes** with clear, descriptive commits.
- **Add or update tests** in the `tests/` directory for new code.
- **Try to ensure test coverage is not reduced** without good reason.
- **Run the full test suite** and ensure all tests pass.
- **Check linting and formatting** before submitting.

## Submitting a Pull Request

- Open a PR against the `main` branch.
- Fill out the PR template, describing your changes and why they are needed.
- Ensure your branch is up to date with `main` before merging.
- Be responsive to review feedback and make requested changes promptly.

## Reporting issues / Suggesting improvements

- Use GitHub Issues for bug reports, feature requests, and questions.
- Include as much detail as possible (steps to reproduce, logs, environment info).

## Community Standards

- Be respectful and constructive in all communications.
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md) at all times.

## Contact

For questions or help, open an issue or reach out via GitHub Discussions.
