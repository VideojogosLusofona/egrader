"""Handle the plugins command."""

import logging

import typer

app = typer.Typer()
logger = logging.getLogger(__name__)


@app.command()
def plugins():
    """List installed plugins."""
    logger.debug("List plugins")
