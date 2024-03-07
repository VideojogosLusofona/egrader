"""Tests for repository plug-ins."""

from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pytest

from egrader.plugins.repo import (
    assess_commit_date_interval,
    assess_files_exist,
    assess_min_commits,
)
from egrader.types import StudentGit


def test_repo_assess_min_commits_no(git_repo, make_commit):
    """Test if a minimum number of commits is not confirmed."""
    make_commit(git_repo)
    stdgit = StudentGit("", "", "")
    result = assess_min_commits(stdgit, str(git_repo), 2)
    assert result == 0


def test_repo_assess_min_commits_yes(git_repo, make_commit):
    """Test if a minimum number of commits is confirmed."""
    make_commit(git_repo)
    make_commit(git_repo)
    make_commit(git_repo)
    stdgit = StudentGit("", "", "")
    result = assess_min_commits(stdgit, str(git_repo), 2)
    assert result == 1


@pytest.mark.parametrize("strict", [False, True])
def test_repo_assess_commit_date_interval_some(git_repo, make_commit, strict):
    """Test if the percentage of commits done in a date interval is correct."""
    # Interval for valid commits
    before_date: datetime = datetime.now() - timedelta(days=1)
    after_date: datetime = datetime.now() - timedelta(days=4)

    # Commits done before the after date
    n_commits_before = 2
    make_commit(git_repo, dt=after_date - timedelta(hours=1, minutes=30))
    make_commit(git_repo, dt=after_date - timedelta(seconds=30))

    # Commits done within the valid time interval
    n_commits_within = 5
    make_commit(git_repo, dt=after_date + timedelta(seconds=30))
    make_commit(git_repo, dt=after_date + timedelta(hours=1, minutes=30))
    make_commit(git_repo, dt=before_date - timedelta(days=1, hours=5))
    make_commit(git_repo, dt=before_date - timedelta(minutes=45))
    make_commit(git_repo, dt=before_date - timedelta(seconds=30))

    # Commits done after the before date
    n_commits_after = 1
    make_commit(git_repo, dt=before_date + timedelta(seconds=10))

    # Check if plugin returns the expected result
    n_commits = n_commits_before + n_commits_within + n_commits_after
    stdgit = StudentGit("", "", "")

    grade = assess_commit_date_interval(
        stdgit,
        str(git_repo),
        before_date=before_date,
        after_date=after_date,
        strict=strict,
    )

    if strict:
        assert grade == 0
    else:
        np.testing.assert_allclose(
            grade,
            n_commits_within / n_commits,
        )


@pytest.mark.parametrize("strict", [False, True])
def test_repo_assess_commit_date_interval_all(git_repo, make_commit, strict):
    """Test that all commits are done in the specified date interval."""
    # Interval for valid commits
    before_date: datetime = datetime.now() - timedelta(days=1)
    after_date: datetime = datetime.now() - timedelta(days=4)

    # Commits done within the valid time interval
    make_commit(git_repo, dt=after_date + timedelta(seconds=30))
    make_commit(git_repo, dt=after_date + timedelta(hours=1, minutes=30))
    make_commit(git_repo, dt=after_date + timedelta(hours=1, minutes=45))
    make_commit(git_repo, dt=before_date - timedelta(days=1, hours=5))
    make_commit(git_repo, dt=before_date - timedelta(minutes=45))
    make_commit(git_repo, dt=before_date - timedelta(seconds=30))

    # Check if plugin returns the expected result
    stdgit = StudentGit("", "", "")

    grade = assess_commit_date_interval(
        stdgit,
        str(git_repo),
        before_date=before_date,
        after_date=after_date,
        strict=strict,
    )

    assert grade == 1


@pytest.mark.parametrize("strict", [False, True])
def test_repo_assess_commit_date_interval_none(git_repo, make_commit, strict):
    """Test that no commits are done in the specified date interval."""
    # Interval for valid commits
    before_date: datetime = datetime.now() - timedelta(days=1)
    after_date: datetime = datetime.now() - timedelta(days=4)

    # Commits done outside the valid time interval
    make_commit(git_repo, dt=after_date - timedelta(hours=1, minutes=45))
    make_commit(git_repo, dt=after_date - timedelta(hours=1, minutes=30))
    make_commit(git_repo, dt=after_date - timedelta(seconds=30))
    make_commit(git_repo, dt=before_date + timedelta(seconds=30))
    make_commit(git_repo, dt=before_date + timedelta(minutes=45))
    make_commit(git_repo, dt=before_date + timedelta(days=1, hours=5))

    # Check if plugin returns the expected result
    stdgit = StudentGit("", "", "")

    grade = assess_commit_date_interval(
        stdgit,
        str(git_repo),
        before_date=before_date,
        after_date=after_date,
        strict=strict,
    )

    assert grade == 0


@pytest.mark.parametrize("strict", [False, True])
@pytest.mark.parametrize("percent", [0, 0.3, 0.7, 1])
def test_repo_assess_files_exist_ok(tmp_path, file_list, strict, percent):
    """Test if the percentage of files in a repository is correct."""
    # Number of files to create
    num_files_to_create = round(percent * len(file_list))

    # Create files
    for i in range(num_files_to_create):
        file_path = Path(tmp_path, file_list[i])
        with open(file_path, "w"):
            pass

    # Empty student just for testing
    stdgit = StudentGit("", "", "")

    # Invoke plugin
    grade = assess_files_exist(stdgit, tmp_path, file_list, strict)

    if strict and percent < 1:
        assert grade == 0
    else:
        np.testing.assert_allclose(
            grade,
            num_files_to_create / len(file_list),
        )
