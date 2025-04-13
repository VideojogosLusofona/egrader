# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Git interface."""

from subprocess import CalledProcessError, run


class GitError(Exception):
    """Error raised when a Git command fails."""


def git(*args):
    """Run git with the specified arguments."""
    cmd = ["git", "--no-pager", *args]
    try:
        return run(cmd, capture_output=True, text=True, check=True)

    except CalledProcessError as cpe:
        raise GitError(f"Error executing the `{" ".join(cmd)}` command: {cpe.stderr}") from cpe


def git_at(repo_path, *args):
    """Run git at location given by `repo_path` with the specified arguments."""
    return git("-C", repo_path, *args)
