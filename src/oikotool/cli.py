# SPDX-License-Identifier: MIT

import os
from pathlib import Path
from typing import Annotated, Optional

import typer

from oikotool.core import Oikotool

OIKOTOOL_APP_NAME = "oikotool"

app = typer.Typer(
    name=OIKOTOOL_APP_NAME,
    help="A tool to automate property listing processes on Oikotie.fi.",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode=None,
)

cache_dir = Path.home() / ".cache" / OIKOTOOL_APP_NAME


@app.command()
def check(
    url: Annotated[str, typer.Argument(help="Property listing query to check.")],
    name: Annotated[
        str, typer.Option("-n", "--name", help="Friendly name for the monitoring task.")
    ],
    limit: Annotated[
        int,
        typer.Option(
            "-l",
            "--limit",
            metavar="NUMBER",
            help="Number of listings to keep track of.",
        ),
    ] = 10,
    slack_url: Annotated[
        Optional[str],
        typer.Option(
            "-s",
            "--slack",
            metavar="URL",
            help="Slack webhook for notifications about new listings.",
        ),
    ] = None,
    healthchecks_url: Annotated[
        Optional[str],
        typer.Option(
            "-h",
            "--healthchecks",
            metavar="URL",
            help="Healthchecks.io ping address for status monitoring.",
        ),
    ] = None,
    uptime_url: Annotated[
        Optional[str],
        typer.Option(
            "-u",
            "--uptime",
            metavar="URL",
            help="Uptime Kuma push address for status monitoring.",
        ),
    ] = None,
    quiet: Annotated[
        bool,
        typer.Option(
            "-q",
            "--quiet",
            help="Suppress all console output except errors.",
        ),
    ] = False,
) -> None:
    """
    Check a property search query for new listings.
    """
    oikotool = Oikotool()
    oikotool.check(
        url=url,
        name=name,
        limit=limit,
        cache_dir=cache_dir,
        slack_url=slack_url,
        healthchecks_url=healthchecks_url,
        uptime_url=uptime_url,
        quiet=quiet,
    )


@app.command()
def save(
    path: Annotated[
        str,
        typer.Argument(help="Directory where the listing images will be saved."),
    ],
    url: Annotated[
        str, typer.Argument(help="Address of the property listing to be saved.")
    ],
    batch: Annotated[
        bool,
        typer.Option(
            "-b",
            "--batch",
            help="Batch mode that creates target subfolder automatically.",
        ),
    ] = False,
    quiet: Annotated[
        bool,
        typer.Option(
            "-q",
            "--quiet",
            help="Suppress all console output except errors.",
        ),
    ] = False,
) -> None:
    """
    Save images from a property listing to a specified directory.
    """
    oikotool = Oikotool()
    output = Path(path).absolute()
    oikotool.save(url=url, base_dir=output, batch=batch, quiet=quiet)


if "DEBUG" in os.environ:

    @app.command()
    def dump(
        url: Annotated[str, typer.Argument(help="Property listing query to process.")],
        limit: Annotated[
            int,
            typer.Option(
                "-l",
                "--limit",
                metavar="NUMBER",
                help="Maximum number of listings to include.",
            ),
        ] = 1,
    ) -> None:
        """
        Display raw API response for property listing query on console.
        """
        oikotool = Oikotool()
        oikotool.dump(url=url, limit=limit)

    @app.command()
    def slack(
        url: Annotated[str, typer.Argument(help="Property listing query to process.")],
        limit: Annotated[
            int,
            typer.Option(
                "-l",
                "--limit",
                metavar="NUMBER",
                help="Maximum number of listings to include.",
            ),
        ] = 1,
    ) -> None:
        """
        Process property listing query and output Slack messages to console.
        """
        oikotool = Oikotool()
        oikotool.slack(url=url, limit=limit)


def main() -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    app()
