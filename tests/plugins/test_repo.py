"""Tests for repository plug-ins."""

from pathlib import Path

from egrader.git import git_at
from egrader.plugins.repo import assess_min_commits
from egrader.types import StudentGit


def do_tmpfile_commit(tmp_file_path: Path):
    """Helper functions which makes a simple commit on the specified repository."""
    with open(tmp_file_path, "a") as tmp_file:
        tmp_file.write("Some more text")
    git_at(tmp_file_path.parent, "add", tmp_file_path.name)
    git_at(tmp_file_path.parent, "commit", "-m", '"Yet another commit"')


def test_repo_assess_min_commits_no(git_repo_empty):
    """Test if a minimum number of commits is not confirmed."""
    some_file_path = Path(git_repo_empty, "some_file.txt")
    do_tmpfile_commit(some_file_path)
    stdgit = StudentGit("", "", "")
    result = assess_min_commits(stdgit, str(git_repo_empty), 2)
    assert result == 0


def test_repo_assess_min_commits_yes(git_repo_empty):
    """Test if a minimum number of commits is confirmed."""
    some_file_path = Path(git_repo_empty, "some_file.txt")
    do_tmpfile_commit(some_file_path)
    do_tmpfile_commit(some_file_path)
    do_tmpfile_commit(some_file_path)
    stdgit = StudentGit("", "", "")
    result = assess_min_commits(stdgit, str(git_repo_empty), 2)
    assert result == 1
