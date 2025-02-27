# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Test the command line application."""

import importlib

import pytest
from typer.testing import CliRunner

from egrader.main import app

runner = CliRunner()


@pytest.mark.parametrize("ver_opt", ["--version", "-v"])
def test_app(ver_opt):
    """Test the version option."""
    result = runner.invoke(app, [ver_opt])
    assert result.exit_code == 0
    assert importlib.metadata.version("egrader") in result.stdout
