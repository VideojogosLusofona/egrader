"""Fixtures and configurations to be used by intra-repo plugin tests."""

from datetime import datetime
from pathlib import Path

import pytest

from egrader.git import git_at


@pytest.fixture()
def git_repo(tmp_path, monkeypatch):
    """Create and configure an empty Git repository."""
    monkeypatch.setenv("GIT_AUTHOR_NAME", "github-actions")
    monkeypatch.setenv(
        "GIT_AUTHOR_EMAIL", "github-actions[bot]@users.noreply.github.com"
    )
    monkeypatch.setenv("GIT_COMMITTER_NAME", "github-actions")
    monkeypatch.setenv(
        "GIT_COMMITTER_EMAIL", "github-actions[bot]@users.noreply.github.com"
    )
    git_at(tmp_path, "init")
    return tmp_path


@pytest.fixture()
def make_commit(monkeypatch):
    """Fixture to make a simple commit."""
    now: datetime = datetime.now()

    def _make_commit(repo: Path, dt: datetime = now):
        """Helper function which makes a simple commit on the specified repository."""
        monkeypatch.setenv("GIT_COMMITTER_DATE", str(dt))
        some_file_path = Path(repo, "some_file.txt")
        with open(some_file_path, "a") as some_file:
            some_file.write("Some more text")
        git_at(repo, "add", some_file_path.name)
        git_at(repo, "commit", "-m", '"Yet another commit"', f"--date={dt}")

    return _make_commit
