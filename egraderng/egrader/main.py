"""The egrader command-line interface."""

from .cli import app


@app.callback()
def callback():
    """Callback for invoking egrader as a Typer app."""
