"""YAML handling functionality."""

from pathlib import Path
from typing import Any

import yaml


def load_yaml(yaml_fp: Path, safe: bool = True) -> Any:
    """Load a yaml file."""
    try:
        with open(yaml_fp, "r") as yaml_file:
            if safe:
                yaml_obj = yaml.safe_load(yaml_file)
            else:
                yaml_obj = yaml.load(yaml_file, yaml.CLoader)
    except yaml.scanner.ScannerError as se:
        raise SyntaxError(
            f"Syntax error{se.problem_mark} {se.context}: {se.problem}"
        ) from se

    return yaml_obj
