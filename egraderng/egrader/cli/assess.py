# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Handle the assess command."""

import logging
from pathlib import Path

import typer
from typing_extensions import Annotated

app = typer.Typer()
logger = logging.getLogger(__name__)


@app.command()
def assess(
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
            help="Folder containing assessment results.",
            show_default="`rules` minus the .yaml extension.",
            exists=True,
            dir_okay=True,
            writable=True,
        ),
    ] = None,
):
    """Assess fetched projects."""
    logger.debug(f"{rules}\n{assess_folder}")
