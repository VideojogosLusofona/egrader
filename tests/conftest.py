import pytest
from egrader.git import git_at


@pytest.fixture
def git_repo_empty(tmp_path):
    git_at(tmp_path, "init")
    git_at(tmp_path, "config", "user.email", "github-actions[bot]@users.noreply.github.com")
    git_at(tmp_path, "config", "user.name", "github-actions")
    return tmp_path
