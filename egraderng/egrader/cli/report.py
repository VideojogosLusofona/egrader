# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

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
