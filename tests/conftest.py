import pytest
from egrader.git import git_at


@pytest.fixture
def git_repo_empty(tmp_path):
    git_at(tmp_path, "init")
    return tmp_path
