"""The egrader command-line interface."""

from enum import Enum
from pathlib import Path

import typer
from typing_extensions import Annotated

app = typer.Typer()


class FetchMode(str, Enum):
    """Assessment modes."""

    stop = "stop"
    update = "update"
    overwrite = "overwrite"


@app.callback()
def callback():
    """Callback for invoking egrader as a Typer app."""


@app.command()
def fetch(
    urls: Annotated[
        Path,
        typer.Argument(
            help="TSV file with remote Git account URLs.", show_default=False
        ),
    ],
    rules: Annotated[
        Path,
        typer.Argument(help="YAML file with assessment rules.", show_default=False),
    ],
    assess_folder: Annotated[
        Path | None,
        typer.Argument(
            help="Folder where to place assessment results.",
            show_default="`rules` minus the .yaml extension.",
        ),
    ] = None,
    mode: Annotated[
        FetchMode,
        typer.Option(
            help="Action to take when one or more repositories to"
            + "fetch already exist locally."
        ),
    ] = FetchMode.stop,
    wait: Annotated[
        float,
        typer.Option(
            "--wait", "-w", help="Time in seconds to wait between clones/pulls."
        ),
    ] = 0.0,
):
    """Fetch projects from repositories."""
    print(f"{urls}\n{rules}\n{assess_folder}")


@app.command()
def assess(
    rules: Annotated[
        Path,
        typer.Argument(help="YAML file with assessment rules.", show_default=False),
    ],
    assess_folder: Annotated[
        Path | None,
        typer.Argument(
            help="Folder containing assessment results.",
            show_default="`rules` minus the .yaml extension.",
        ),
    ] = None,
):
    """Assess fetched projects."""
    print(f"{rules}\n{assess_folder}")


@app.command()
def report(
    assess_folder: Annotated[
        Path,
        typer.Argument(
            help="Folder containing assessment results.",
            show_default=False,
        ),
    ],
):
    """Generate an assessment report."""
    print(f"Hello {assess_folder}")


@app.command()
def plugins():
    """List installed plugins."""
    print("List plugins")
