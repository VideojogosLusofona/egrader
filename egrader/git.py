import sh


class GitError(Exception):
    """Error raised when a Git command fails"""


def git_cmd(*args):
    try:
        sh.git(*args)
    except sh.ErrorReturnCode as erc:
        raise GitError(
            f"The following error occurred when executing the '{erc.full_cmd}' command:"
            f"\n\n{erc.stderr.decode('UTF-8')}"
        ) from erc
