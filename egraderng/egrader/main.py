"""The egrader command-line interface."""

import typer

app = typer.Typer()


@app.callback()
def callback():
    """Callback for invoking egrader as a typer app."""


@app.command()
def fetch(name: str):
    """Fetch projects from repositories."""
    print(f"Hello {name}")


@app.command()
def assess(name: str, formal: bool = False):
    """Assess fetched projects."""
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


@app.command()
def report(name: str):
    """Generate an assessment report."""
    print(f"Hello {name}")


@app.command()
def plugins():
    """List installed plugins."""
    print("List plugins")
