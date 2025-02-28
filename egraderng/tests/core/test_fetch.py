# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Test the core fetch operations."""


from egrader import eg_config
from egrader.core.fetch import _load_repos


def test_load_repos(repo_file_valid):
    """Test the function to load the repos file."""
    repos = _load_repos(repo_file_valid)

    assert eg_config.id_col in repos.columns
    assert eg_config.repo_col in repos.columns
