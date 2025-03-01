# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Test the core fetch operations."""


import re

import pytest

from egrader import eg_config
from egrader.core.fetch import load_user_data


def test_load_users_ok(repo_file_valid):
    """Test the function to load the users and repos file."""
    repos = load_user_data(repo_file_valid)

    assert eg_config.id_col in repos.columns
    assert eg_config.repo_base_col in repos.columns


def test_load_users_ko(repo_file_invalid, required_col):
    """Test the function to load a users and repos file without a required column."""
    with pytest.raises(
        KeyError,
        match=re.escape(
            f"Users file does not contain required `{required_col}` column."
        ),
    ):
        load_user_data(repo_file_invalid)
