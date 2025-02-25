"""Handle the assess command."""

from pathlib import Path

import typer
from typing_extensions import Annotated

app = typer.Typer()


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
