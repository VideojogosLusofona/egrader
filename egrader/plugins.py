from pathlib import Path
from sys import maxsize

from .git import GitError, git_at


def check_min_commits(repo_fp: Path, minimum: int):
    git_at(repo_fp, "rev-list", "HEAD", "--count")
