# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Handle the plugins command."""

import typer

from ..plugin_manager import PluginTypes

app = typer.Typer()


@app.command()
def plugins():
    """List installed plugins."""
    PluginTypes.print_all()
