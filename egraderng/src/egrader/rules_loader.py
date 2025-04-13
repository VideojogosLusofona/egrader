# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Rules files loader module."""

import logging
from pathlib import Path
from typing import Any

from .plugin_manager import PluginLoadError, PluginTypes

logger = logging.getLogger(__name__)


def load_rules(rules_fp: Path) -> Any:
    """Load rules file."""
    ext = rules_fp.suffix[1:]

    for loader_name, loader_function in PluginTypes.Loader.load_functions(set()).items():
        if ext in loader_function():
            logger.info(f"Using `{loader_name}` to load `{rules_fp}`")
            return loader_function(rules_fp)

    raise PluginLoadError(f"Unable to load rules file of type `{ext}`")
