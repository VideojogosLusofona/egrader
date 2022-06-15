import sh


class GitError(Exception):
    """Error raised when a Git command fails"""


def git_cmd(*args):
    """Run git with the specified arguments"""
    try:
        sh.git(*args)
    except sh.ErrorReturnCode as erc:
        raise GitError(
            f"The following error occurred when executing the '{erc.full_cmd}' command:"
            f"\n\n{erc.stderr.decode('UTF-8')}"
        ) from erc


def git_cmd_at(repo_path, *args):
    """Run git at location given by repo_path with the specified arguments"""
    git_cmd("-C", repo_path, *args)
