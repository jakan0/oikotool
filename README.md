# Oikotool

Oikotool is a command-line tool to automate property searches on Oikotie.fi, a Finnish
real estate website.

## Features

- Check for new property listings based on a search query
- Save images from property listings
- Notify about new listings via Slack
- Integration with health monitoring services such as Healthchecks.io and Uptime Kuma

## Installation

Oikotool requires Python 3.10 or later and is currently distributed only through GitHub
releases. To install:

1. Visit the [Releases page](https://github.com/jakan0/oikotool/releases) of the
   Oikotool repository.
2. Download the latest `.whl` file (e.g., `oikotool-1.0.0-py3-none-any.whl`).
3. Follow the installation instructions below for either uv or pip.

### Using uv (Recommended)

[uv](https://docs.astral.sh/uv/) is the recommended way to install Oikotool. If you
don't have uv installed, you can install it following the instructions on the [uv
installation page](https://docs.astral.sh/uv/getting-started/installation/).

To install Oikotool using uv:

```shell
uv tool install oikotool-1.0.0-py3-none-any.whl
```

### Using pip

If you prefer to use pip, you can install Oikotool for the current user with:

```shell
pip install --user oikotool-1.0.0-py3-none-any.whl
```

## Usage

### Check for New Listings

```shell
oikotool check [OPTIONS] URL
```

Options:

- `-n, --name TEXT`: Friendly name for the monitoring task
- `-l, --limit NUMBER`: Number of listings to keep track of (default: 10)
- `-s, --slack URL`: Slack webhook for notifications about new listings
- `-h, --healthchecks URL`: Healthchecks.io ping address for status monitoring
- `-u, --uptime URL`: Uptime Kuma push address for status monitoring
- `-q, --quiet`: Suppress all console output except errors

### Save Listing Images

```shell
oikotool save [OPTIONS] PATH URL
```

Options:

- `-b, --batch`: Batch mode that creates target subfolder automatically
- `-q, --quiet`: Suppress all console output except errors

## Configuration

Oikotool stores its cache in `~/.cache/oikotool/`.

### Slack Integration

To enable Slack notifications:

1. Go to https://api.slack.com/apps/
2. Create a new app or select an existing one
3. Under "Features", find and activate "Incoming Webhooks"
4. Create a new webhook URL for your workspace and channel
5. Use this webhook URL with Oikotool's `--slack` option

The webhook URL you receive will look similar to this:

```
https://hooks.slack.com/services/TXXXXXXXXX/BXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXX
```

Note: The actual URL will contain unique identifiers for your workspace and channel.
Keep this URL confidential as it allows posting messages to your Slack channel.

## Development

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) for dependency management

### Setting Up the Development Environment

1. Clone the repository
2. Create the virtual environment

```shell
uv venv
```

3. Install the dependencies:

```shell
uv pip install --group dev .
```

### Code Quality

The project uses the following tools to maintain code quality and consistency:

1. [Ruff](https://docs.astral.sh/ruff/) for linting and formatting
2. [mypy](https://mypy-lang.org/) for static type checking

To run all code quality checks, use the following commands:

```shell
uv run ruff check --fix  # Lint and auto-resolve issues
uv run ruff format       # Format code
uv run mypy .            # Type checking
```

### Testing

The project uses pytest as a testing framework. The test suite includes unit tests and
integration tests to ensure the reliability and correctness of Oikotool.

To run the complete test suite:

```shell
uv run pytest
```

Test files are located in the `tests/` directory and follow the standard naming
convention `test_*.py`.

## Contributing

All contributions are expected to:

- Ensure all existing tests pass before submitting a pull request
- Include tests that reproduce the fixed issue when submitting bug fixes

## License

This project is licensed under the MIT License.
