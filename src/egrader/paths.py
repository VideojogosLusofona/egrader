"""Path-checking functions."""

from pathlib import Path
from typing import Final

_FILE_VALID_STUDENTS_GIT: Final[str] = "validated_git_urls.yml"
_FILE_ASSESSED_STUDENTS: Final[str] = "assessed_students.yml"
_FOLDER_STUDENT_REPOS: Final[str] = "student_repos"


def check_required_fp_exists(fp_to_check: Path) -> None:
    """Check if file path exists, and if not, raise exception."""
    if not fp_to_check.exists():
        raise FileNotFoundError(f"File {fp_to_check!r} does not exist!")


def get_student_repo_fp(assess_fp: Path, student_id: str, repo_name: str) -> Path:
    """Determine the path to a student repository."""
    return assess_fp.joinpath(_FOLDER_STUDENT_REPOS, student_id, repo_name)


def get_student_repos_fp(assess_fp: Path) -> Path:
    """Determine the path containing all student repositories."""
    return assess_fp.joinpath(_FOLDER_STUDENT_REPOS)


def get_valid_students_git_fp(assess_fp: Path) -> Path:
    """Determine path for valid student Git URLs yaml file."""
    return assess_fp.joinpath(_FILE_VALID_STUDENTS_GIT)


def get_assessed_students_fp(assess_fp: Path) -> Path:
    """Determine path for student assessments yaml file."""
    return assess_fp.joinpath(_FILE_ASSESSED_STUDENTS)
