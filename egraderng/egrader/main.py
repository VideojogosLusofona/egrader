# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""The egrader command-line interface."""

import importlib.metadata

import typer

from .cli import app
from .core import eg_config as egc

__version__ = importlib.metadata.version("egrader")


def version_callback(value: bool):
    """Show version."""
    if value:
        egc.console.print(f"[grey42]egrader[/] [i]v{__version__}[/i]")
        raise typer.Exit()


@app.callback()
def callback(
    version: bool | None = typer.Option(  # noqa B008
        None,
        "--version",
        "-v",
        help="Show the application version",
        callback=version_callback,
        is_eager=True,
    )
):
    """Callback for invoking egrader as a Typer app."""
