# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""YAML loader."""

from pathlib import Path
from typing import Any

import yaml


def load_yaml(fp: Path | None = None) -> Any:
    """Load a yaml file."""
    if fp is None:
        return ["yaml", "yml"]
    try:
        with open(fp, "r", encoding="utf-8") as yaml_file:
            yaml_obj = yaml.safe_load(yaml_file)
    except yaml.scanner.ScannerError as se:
        raise SyntaxError(f"Syntax error{se.problem_mark} {se.context}: {se.problem}") from se

    return yaml_obj
