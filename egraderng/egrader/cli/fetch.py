"""Handle the fetch command."""

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


@app.command()
def fetch(
    urls: Annotated[
        Path,
        typer.Argument(
            help="TSV file with remote Git account URLs.",
            show_default=False,
            exists=True,
            file_okay=True,
            readable=True,
        ),
    ],
    rules: Annotated[
        Path,
        typer.Argument(
            help="YAML file with assessment rules.",
            show_default=False,
            exists=True,
            file_okay=True,
            readable=True,
        ),
    ],
    assess_folder: Annotated[
        Path | None,
        typer.Argument(
            help="Folder where to place assessment results.",
            show_default="`rules` minus the .yaml extension.",
            dir_okay=True,
            writable=True,
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
