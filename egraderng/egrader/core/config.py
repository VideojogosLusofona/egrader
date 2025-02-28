# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""App-wide configuration."""

from types import SimpleNamespace

from rich.console import Console

# Create a global config object
eg_config = SimpleNamespace()
eg_config.console = Console(highlight=False)
eg_config.id_col = "id"
eg_config.repo_base_col = "repo_base"
