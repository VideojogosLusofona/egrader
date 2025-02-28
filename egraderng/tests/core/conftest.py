# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Fixtures to be used by test functions for core functionality."""

from egrader import eg_config

def repo_file_valid(faker):
    """Valid repo file."""
    data = {
        eg_config.id_col: [],
        eg_config.repo_col: [],
        "email": [],
        "name": []
    }
    for _ in range(20): # Use faker's csv generator instead
        data[eg_config.id_col].append(faker.)
        data[eg_config.repo_col].append(faker.)
        data[eg_config.email_col].append(faker.email())
        data[eg_config.name_col].append(faker.name())