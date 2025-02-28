# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Fetch functionality."""

import logging
from pathlib import Path

import pandas as pd

from .config import eg_config as egc

logger = logging.getLogger(__name__)


def _load_repos(repos_fp: Path) -> pd.DataFrame:
    """Load users and repositories from the specified CSV file.

    Args:
      repos_fp: Repositories CSV file, requires at least the `id` and `repo`
        columns.

    Returns:
      pd.DataFrame: Dataframe with users, repositories, and possibly additional
        data to be used by specific plugins.
    """
    df = pd.read_csv(repos_fp)

    if egc.id_col not in df.columns:
        raise KeyError(
            f"Repositories file does not contain required `{egc.id_col}` column."
        )

    if egc.repo_col not in df.columns:
        raise KeyError(
            f"Repositories file does not contain required `{egc.repo_col}` column."
        )

    return df


def fetch_op(repos_fp: Path, rules_fp: Path, assess_fp: Path) -> None:
    """Fetch (clone or update) the specified repositories.

    Args:
      repos_fp: Repositories file.
      rules_fp: Rules file.
      assess_fp: Assessment folder.
    """
    repos_df = _load_repos(repos_fp)

    logger.debug(repos_df)
