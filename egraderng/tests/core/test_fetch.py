# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Test the core fetch operations."""


import re

import pandas as pd
import pytest

from egrader import eg_config as egc
from egrader.core import git, load_user_data

# ######## #
# Fixtures #
# ######## #


@pytest.fixture
def repo_data_valid_df(faker):
    """Create valid repo data in Pandas dataframe format."""
    # Number of rows
    num_rows = 20

    # Generate data
    data = {
        egc.id_col: [faker.random_int(min=100000, max=999999) for _ in range(num_rows)],
        egc.repo_base_col: [
            f"https://github.com/{faker.user_name()}/{faker.word()}" for _ in range(num_rows)
        ],
        "email": [faker.email() for _ in range(num_rows)],
        "name": [faker.name() for _ in range(num_rows)],
    }

    # Return DataFrame with this data
    return pd.DataFrame(data)


@pytest.fixture(params=[",", ";", "\t"])
def repo_file_valid(repo_data_valid_df, tmp_path, request):
    """Create a valid repo file."""
    repo_file = tmp_path / "repos.csv"

    repo_data_valid_df.to_csv(repo_file, sep=request.param, index=False)

    return repo_file


@pytest.fixture(params=[egc.id_col, egc.repo_base_col])
def required_col(request):
    """Required columns in the repos file."""
    return request.param


@pytest.fixture
def repo_file_invalid(repo_data_valid_df, tmp_path, required_col):
    """Create an invalid repo file."""
    repo_file = tmp_path / "repos.csv"

    repo_data_invalid_df = repo_data_valid_df.drop(columns=[required_col])
    repo_data_invalid_df.to_csv(repo_file, index=False)

    return repo_file


# ##### #
# Tests #
# ##### #


def test_load_users_ok(repo_file_valid):
    """Test the function to load the users and repos file."""
    repos = load_user_data(repo_file_valid)

    assert egc.id_col in repos.columns
    assert egc.repo_base_col in repos.columns


def test_load_users_ko(repo_file_invalid, required_col):
    """Test the function to load a users and repos file without a required column."""
    with pytest.raises(
        KeyError,
        match=re.escape(f"Users file does not contain required `{required_col}` column."),
    ):
        load_user_data(repo_file_invalid)


def test_clone(git_http_server, tmp_path):
    """Test a clone from a locally run HTTP Git server."""
    local_repo_path = tmp_path / "cloned"
    git("clone", git_http_server, str(local_repo_path))
    assert local_repo_path.exists()
