# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Core functionality."""

from .config import eg_config
from .fetch import fetch_op, load_repo_names, load_user_data

__all__ = ["eg_config", "fetch_op", "load_repo_names", "load_user_data"]
