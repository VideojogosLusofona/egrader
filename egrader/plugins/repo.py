"""Repository plug-ins."""

import shlex
from datetime import date, datetime
from pathlib import Path
from subprocess import TimeoutExpired, run
from typing import Sequence

from dateutil.parser import isoparse

from ..git import GitError, git_at
from ..types import StudentGit
from .helpers import interpret_datetime


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
    start_date: date | datetime | str,
    end_date: date | datetime | str,
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
    student: StudentGit, repo_path: str, filenames: Sequence[str]
) -> float:
    """Check if the files or folders exist."""
    n_files_exist = 0

    for filename in filenames:
        fp = Path(repo_path, filename)

        if fp.exists():
            n_files_exist += 1

    return n_files_exist / len(filenames)


def assess_run_command(
    student: StudentGit,
    repo_path: str,
    command: str,
    input_stream: str | None = None,
    expect_exit_code: int = 0,
    expect_output: str | None = None,
    timeout: float = 0.5,
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

    print(r)

    if expect_exit_code != r.returncode:
        return 0

    if expect_output is not None and expect_output not in r.stdout + r.stderr:
        return 0

    return 1
