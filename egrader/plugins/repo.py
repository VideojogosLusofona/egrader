"""Repository plug-ins."""

from datetime import date, datetime
from pathlib import Path
from typing import Sequence

from dateutil.parser import isoparse

from ..git import GitError, git_at
from .helpers import interpret_datetime


def assess_min_commits(repo_path: str, minimum: int) -> float:
    """Check if repository has a minimum number of commits."""
    n_commits = git_at(repo_path, "rev-list", "--all", "--count")
    if int(n_commits) >= minimum:
        return 1
    else:
        return 0


def assess_commit_date_interval(
    repo_path: str, start_date: date | datetime | str, end_date: date | datetime | str
) -> float:
    """Check if the last commit was performed on the specified date interval."""
    try:
        lc_dt_cmd = git_at(repo_path, "log", "-1", "--date=iso-strict", r"--format=%cd")
    except GitError:
        return 0

    lc_dt_str = lc_dt_cmd.strip()
    lc_dt: datetime = isoparse(lc_dt_str)

    start_dt = interpret_datetime(start_date, lc_dt.tzinfo)
    end_dt = interpret_datetime(end_date, lc_dt.tzinfo)

    if start_dt < lc_dt < end_dt:
        return 1
    else:
        return 0


def assess_repo_exists(repo_path: str) -> float:
    """Check if a repository exists (always returns 1)."""
    return 1


def assess_files_exist(repo_path: str, filenames: Sequence[str]) -> float:
    """Check if the files or folders exist."""
    n_files_exist = 0

    for filename in filenames:
        fp = Path(repo_path, filename)

        if fp.exists():
            n_files_exist += 1

    return n_files_exist / len(filenames)
