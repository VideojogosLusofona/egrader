"""Handle the report command."""

import logging
from pathlib import Path

import typer
from typing_extensions import Annotated

logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def report(
    assess_folder: Annotated[
        Path,
        typer.Argument(
            help="Folder containing assessment results.",
            show_default=False,
            exists=True,
            dir_okay=True,
            readable=True,
        ),
    ],
):
    """Generate an assessment report."""
    logger.debug(f"Hello {assess_folder}")
