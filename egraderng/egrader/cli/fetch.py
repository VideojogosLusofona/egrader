# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Handle the fetch command."""

import shutil
from enum import Enum
from pathlib import Path

import typer
from typing_extensions import Annotated

from ..core.fetch import fetch_op

app = typer.Typer()


class FetchMode(str, Enum):
    """Assessment modes."""

    stop = "stop"
    update = "update"
    overwrite = "overwrite"


@app.command()
def fetch(
    repos: Annotated[
        Path,
        typer.Argument(
            help="CSV/TSV file with user IDs and respective repository links.",
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
    if assess_folder is None:
        assess_folder = Path(rules.stem)

    if assess_folder.exists():

        if assess_folder.is_file():
            raise typer.BadParameter(
                f"Assessment folder `{assess_folder}` is a file. "
                + "Only folders are allowed."
            )

        if mode == FetchMode.stop:

            raise typer.BadParameter(
                f"Assessment folder `{assess_folder}` already exists. "
                + "Delete it or use an alternative --mode option."
            )

        if mode == FetchMode.overwrite:
            shutil.rmtree(assess_folder)

    else:
        assess_folder.mkdir()

    fetch_op(repos, rules, assess_folder)
