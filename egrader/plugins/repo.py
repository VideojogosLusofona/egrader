from ..git import git_at


def assess_min_commits(repo_path: str, minimum: int) -> float:
    """Check if repository has a minimum number of commits."""

    n_commits = git_at(repo_path, "rev-list", "HEAD", "--count")
    if int(n_commits) >= minimum:
        return 1
    else:
        return 0
