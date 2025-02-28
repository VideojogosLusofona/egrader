# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Fetch functionality."""

import logging
from collections.abc import Sequence
from pathlib import Path

import pandas as pd

from .config import eg_config as egc

logger = logging.getLogger(__name__)


def load_user_data(userdata_fp: Path) -> pd.DataFrame:
    """Load users and base repository addresses from the specified CSV file.

    Args:
      userdata_fp: User data CSV file, requires at least the `id` and `repo_base`
        columns.

    Returns:
      Dataframe with users, repositories, and possibly additional data to be
        used by specific plugins.
    """
    df = pd.read_csv(userdata_fp)

    if egc.id_col not in df.columns:
        raise KeyError(
            f"Repositories file does not contain required `{egc.id_col}` column."
        )

    if egc.repo_base_col not in df.columns:
        raise KeyError(
            f"Repositories file does not contain required `{egc.repo_base_col}` column."
        )

    return df


def load_repo_names(rules_fp: Path) -> Sequence[str]:
    """Load repository names from rules file.

    Args:
      rules_fp: Rules file.

    Returns:
      A sequence of repository names.
    """
    return []


def fetch_op(
    userdata_df: pd.DataFrame, repo_names: Sequence[str], assess_fp: Path
) -> None:
    """Fetch (clone or update) user repositories.

    Args:
      userdata_df: Data frame with user data, contains the base repository addresses.
      repo_names: Names of the repositories to fetch from each user.
      assess_fp: Assessment folder.
    """
    logger.debug(userdata_df)
