from pathlib import Path

from .git import git_at


def assess_min_commits(repo_fp: Path, minimum: int) -> float:
    n_commits = git_at(repo_fp, "rev-list", "HEAD", "--count")
    if int(n_commits) >= minimum:
        return 1
    else:
        return 0
