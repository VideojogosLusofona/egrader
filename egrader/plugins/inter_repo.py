"""Inter-repository plug-ins."""

from typing import List, Sequence, Tuple

from ..git import git_at


def assess_more_commits_bonus(
    repo_paths: Sequence[str], bonuses: Sequence[float]
) -> Sequence[float]:
    """Add bonuses to repositories with more commits."""
    # Number of repositories to inter-assess
    n_repos = len(repo_paths)

    # Make bonus list the same size as the number of repositories
    bonus_lst: Sequence[float]

    if len(bonuses) > n_repos:
        bonus_lst = bonuses[:n_repos]
    elif len(bonuses) < n_repos:
        bonus_lst = list(bonuses) + (n_repos - len(bonuses)) * [0.0]
    else:
        bonus_lst = bonuses[:]

    # Determine number of commits in each repository and associate them with
    # the repositories index in repo_paths
    idx_commits: List[Tuple[int, int]] = list(
        enumerate([int(git_at(rp, "rev-list", "HEAD", "--count")) for rp in repo_paths])
    )

    # Sort by number of commits, higher to lower
    idx_commits.sort(key=lambda ic: -ic[1])

    # Associate the repo indexes (sorted by number of commits) with the
    # user-specified bonuses
    idx_bonus = list(zip([ic[0] for ic in idx_commits], bonus_lst, strict=True))

    # Resort bonuses by repo index
    idx_bonus.sort()

    # Return bonuses associated with each repo
    return [ib[1] for ib in idx_bonus]
