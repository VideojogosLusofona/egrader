"""The egrader command-line interface."""

import importlib.metadata

import typer

from .cli import app

__version__ = importlib.metadata.version("egrader")


def version_callback(value: bool):
    """Show version."""
    if value:
        print(f"egrader v{__version__}")
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
