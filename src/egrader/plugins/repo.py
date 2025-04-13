"""Repository plug-ins."""

import shlex
import sys
from datetime import date, datetime
from pathlib import Path
from subprocess import TimeoutExpired, run
from typing import Sequence

import numpy as np
from dateutil.parser import isoparse

from ..git import GitError, git_at
from ..types import StudentGit
from .helpers import interpret_datetime

_max_git_commits: int = np.iinfo(np.int32).max


def assess_min_commits(student: StudentGit, repo_path: str, minimum: int) -> float:
    """Check if repository has a minimum number of commits."""
    n_commits = git_at(repo_path, "rev-list", "--all", "--count")
    if int(n_commits) >= minimum:
        return 1
    else:
        return 0


def assess_commit_date_interval(
    student: StudentGit,
    repo_path: str,
    before_date: date | datetime | str,
    after_date: date | datetime | str = date.min,
    last_n_commits: int = _max_git_commits,
    strict: bool = False,
) -> float:
    """Return the percentage of commits performed on the specified date interval."""
    try:
        commit_dates_cmd = git_at(
            repo_path, "log", f"-{last_n_commits}", "--date=iso-strict", r"--format=%cd"
        )
    except GitError:
        return 0

    commit_dates = commit_dates_cmd.splitlines()

    within_interval: int = 0

    for commit_date in commit_dates:
        commit_dtiso: datetime = isoparse(commit_date.strip())
        after_dt = interpret_datetime(after_date, commit_dtiso.tzinfo)
        before_dt = interpret_datetime(before_date, commit_dtiso.tzinfo)

        if after_dt <= commit_dtiso <= before_dt:
            within_interval += 1
        elif strict:
            return 0

    return within_interval / len(commit_dates)


def assess_commits_email(student: StudentGit, repo_path: str) -> float:
    """Check commits were performed with the specified emails."""
    try:
        commits_emails_cmd: str = git_at(repo_path, "log", r"--format=%ae")
    except GitError:
        return 0

    # Convert returned command to list of emails
    commit_emails_lst = [email.strip() for email in commits_emails_cmd.splitlines()]

    # Grade is percentage of commits done with the student email
    return commit_emails_lst.count(student.email) / len(commit_emails_lst)


def assess_repo_exists(student: StudentGit, repo_path: str) -> float:
    """Check if a repository exists (always returns 1)."""
    return 1


def assess_files_exist(
    student: StudentGit, repo_path: str, filenames: Sequence[str], strict: bool = False
) -> float:
    """Check if the files or folders exist."""
    n_files_exist = 0

    for filename in filenames:
        fp = Path(repo_path, filename)

        if fp.exists():
            n_files_exist += 1
        elif strict:
            return 0

    return n_files_exist / len(filenames)


def assess_run_command(
    student: StudentGit,
    repo_path: str,
    command: str,
    input_stream: str | None = None,
    expect_exit_code: int = 0,
    expect_output: str | None = None,
    timeout: float = 6.5,
) -> float:
    """Run a command and check for exit code and/or expected output."""
    try:
        r = run(
            shlex.split(command),
            input=input_stream,
            capture_output=True,
            text=True,
            cwd=repo_path,
            timeout=timeout,
        )
    except (TimeoutExpired, FileNotFoundError):
        return 0

    except Exception as ex:
        print(
            f"Unexpected error '{ex}' running command '{command}' in "
            + f"folder '{repo_path}'",
            file=sys.stderr,
        )
        return 0

    if expect_exit_code != r.returncode:
        return 0

    if expect_output is not None and expect_output not in r.stdout + r.stderr:
        return 0

    return 1
