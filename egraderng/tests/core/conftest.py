# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Fixtures to be used by test functions for core functionality."""

import pandas as pd
import pytest

from egrader import eg_config as egc


@pytest.fixture
def repo_data_valid_df(faker):
    """Create valid repo data in Pandas dataframe format."""
    # Number of rows
    num_rows = 20

    # Generate data
    data = {
        egc.id_col: [faker.random_int(min=100000, max=999999) for _ in range(num_rows)],
        egc.repo_base_col: [
            f"https://github.com/{faker.user_name()}/{faker.word()}"
            for _ in range(num_rows)
        ],
        "email": [faker.email() for _ in range(num_rows)],
        "name": [faker.name() for _ in range(num_rows)],
    }

    # Return DataFrame with this data
    return pd.DataFrame(data)


@pytest.fixture
def repo_file_valid(repo_data_valid_df, tmp_path):
    """Create a valid repo file."""
    repo_file = tmp_path / "repos.csv"

    repo_data_valid_df.to_csv(repo_file, index=False)

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
