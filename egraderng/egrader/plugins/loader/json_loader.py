# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""JSON loader."""

import json
from pathlib import Path
from typing import Any


def load_json(fp: Path | None = None) -> Any:
    """Load a JSON file."""
    if fp is None:
        return {"json"}
    with open(fp, "r", encoding="utf-8") as json_file:
        return json.load(json_file)
