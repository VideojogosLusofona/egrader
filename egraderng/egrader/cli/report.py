"""Handle the report command."""

from pathlib import Path

import typer
from typing_extensions import Annotated

app = typer.Typer()


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
