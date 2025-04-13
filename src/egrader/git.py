"""Functions for handling Git functionality."""

from sh import ErrorReturnCode
from sh import git as sh_git


class GitError(Exception):
    """Error raised when a Git command fails."""


def git(*args):
    """Run git with the specified arguments."""
    try:
        return sh_git("--no-pager", *args)
    except ErrorReturnCode as erc:
        raise GitError(
            f"The following error occurred when executing the {erc.full_cmd!r} command:"
            f"\n\n{erc.stderr.decode('UTF-8')}"
        ) from erc


def git_at(repo_path, *args):
    """Run git at location given by repo_path with the specified arguments."""
    return git("-C", repo_path, *args)
