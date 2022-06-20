from datetime import date, datetime
from pathlib import Path

from dateutil.parser import isoparse

from ..git import git_at
from .helpers import interpret_datetime


def assess_min_commits(repo_path: str, minimum: int) -> float:
    """Check if repository has a minimum number of commits."""

    n_commits = git_at(repo_path, "rev-list", "HEAD", "--count")
    if int(n_commits) >= minimum:
        return 1
    else:
        return 0


def assess_commit_date_interval(
    repo_path: str, start_date: date | datetime | str, end_date: date | datetime | str
) -> float:
    """Check if the last commit was performed on the specified date interval."""

    lc_dt_cmd = git_at(repo_path, "log", "-1", "--date=iso-strict", r"--format=%cd")
    lc_dt_str = lc_dt_cmd.stdout.decode().strip()
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


def assess_file_exists(repo_path: str, filename: str) -> float:
    """Check if a file or folder exists."""

    fp = Path(repo_path, filename)

    if fp.exists():
        return 1
    else:
        return 0
