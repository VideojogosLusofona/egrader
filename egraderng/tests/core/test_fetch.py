# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Test the core fetch operations."""


import pytest

from egrader.core import _load_repos


def test_load_repos(ver_opt):
    """Test the function to load the repos file."""
