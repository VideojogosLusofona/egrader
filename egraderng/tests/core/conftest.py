# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Fixtures to be used by test functions for core functionality."""

import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pytest

from egrader.core import git, git_at


@pytest.fixture
def git_repo(tmp_path):
    """Create a Git repository with commits and convert it to a bare repo."""
    repo_path = tmp_path / "testrepo"
    repo_path.mkdir()

    # Create a regular Git repository
    git_at(str(repo_path), "init")

    # Create a file in the repository
    test_file = repo_path / "test.txt"
    test_file.write_text("Hello, Git!")

    # Add file to staging area and create a test commit
    git_at(str(repo_path), "add", str(test_file))
    git_at(str(repo_path), "commit", "-m", "First commit")

    # Provide the repo for tests
    return repo_path


@pytest.fixture
def git_repo_bare(git_repo, tmp_path):
    """Create a bare Git repository for cloning."""
    # Obtain a path for the bare repo
    bare_repo_path = tmp_path / "testrepo.git"

    # Clone the regular repository into a bare repository
    git("clone", "--bare", str(git_repo), str(bare_repo_path))

    # Allow HTTP(S) cloning
    git_at(str(bare_repo_path), "update-server-info")

    # Provide the repo for tests
    return bare_repo_path


@pytest.fixture
def git_http_server(git_repo_bare):
    """Fixture to start an in-process HTTP server serving the repo."""

    class RepoHTTPHandler(SimpleHTTPRequestHandler):
        """This handler serves the files under the bare Git repo."""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(git_repo_bare), **kwargs)

    # Start server
    server = HTTPServer(("localhost", 0), RepoHTTPHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    # Test runs while server is running
    yield f"http://localhost:{server.server_address[1]}"  # /{git_repo_bare.name}

    # Shutdown server
    server.shutdown()
    thread.join()
