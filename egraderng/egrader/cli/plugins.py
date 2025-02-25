"""Handle the plugins command."""

import typer

app = typer.Typer()


@app.command()
def plugins():
    """List installed plugins."""
    print("List plugins")
