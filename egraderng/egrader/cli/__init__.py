# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""CLI commands."""

import typer

from .assess import app as assess_app
from .fetch import app as fetch_app
from .plugins import app as plugins_app
from .report import app as report_app

app = typer.Typer()

app.add_typer(fetch_app)
app.add_typer(assess_app)
app.add_typer(report_app)
app.add_typer(plugins_app)
