from argparse import ArgumentError
from inspect import getdoc
from pathlib import Path
from typing import Any, Dict, Final, List, Sequence, cast

import requests
import validators

OPT_E_SHORT: Final[str] = "e"
OPT_E_LONG: Final[str] = "existing"
OPT_E_STOP: Final[str] = "stop"
OPT_E_UPDT: Final[str] = "update"
OPT_E_OVWR: Final[str] = "overwrite"

_FILE_VALID_STUDENTS_GIT_: Final[str] = "validated_git_urls.yml"
_FILE_ASSESSED_STUDENTS_: Final[str] = "assessed_students.yml"
_FOLDER_STUDENT_REPOS_: Final[str] = "student_repos"


class StudentGit:
    """A student and his Git repositories."""

    def __init__(self, sid: str, url: str) -> None:
        # Set instance variables
        self.sid: str = sid
        self.url: str = url
        self.valid_url: bool = False
        self.repos: Dict[str, str] = {}

        # Validate URL if it's is well-formed and if it exists (200)
        if validators.url(self.url) and requests.head(self.url).status_code < 400:
            self.valid_url = True

    def __repr__(self) -> str:
        return "%s(sid=%r, url=%r, valid_url=%r, repos=%r)" % (
            self.__class__.__name__,
            self.sid,
            self.url,
            self.valid_url,
            self.repos,
        )

    def add_repo(self, repo_name: str, repo_path: str) -> None:
        self.repos[repo_name] = repo_path


class Assessment:
    """An already performed assessment."""

    def __init__(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        weight: float,
        grade_raw: float,
    ) -> None:
        # Set instance variables
        self.name: str = name
        self.description: str = description
        self.parameters: Dict[str, Any] = parameters
        self.weight: float = weight
        self.grade_raw: float = grade_raw

    def __repr__(self) -> str:
        return "%s(name=%r, description=%r, weight=%r, grade_raw=%r)" % (
            self.__class__.__name__,
            self.name,
            self.description,
            self.weight,
            self.grade_raw,
        )

    @property
    def grade_final(self) -> float:
        return self.grade_raw * self.weight


class AssessedRepo:
    """An assessed student repository."""

    def __init__(self, name: str, weight: float) -> None:
        # Set instance variables
        self.name: str = name
        self.weight: float = weight
        self.assessments: List[Assessment] = []
        self.inter_assessments: List[Assessment] = []
        self.local_path: str | None = None

    def __repr__(self) -> str:
        return "%s(name=%r, weight=%r, assessments=%r, inter_assessments=%r)" % (
            self.__class__.__name__,
            self.name,
            self.weight,
            self.assessments,
            self.inter_assessments,
        )

    def add_assessment(self, assessment: Assessment) -> None:
        self.assessments.append(assessment)

    def add_inter_assessment(self, assessment: Assessment) -> None:
        self.inter_assessments.append(assessment)

    def is_empty(self) -> bool:
        return len(self.assessments) + len(self.inter_assessments) == 0

    @property
    def grade_final(self) -> float:
        return self.grade_raw * self.weight

    @property
    def grade_raw(self) -> float:
        return sum([a.grade_final for a in self.assessments]) + sum(
            [a.grade_final for a in self.inter_assessments]
        )


class AssessedStudent:
    """An assessed student."""

    def __init__(self, sid: str) -> None:
        # Set instance variables
        self.sid: str = sid
        self.assessed_repos: List[AssessedRepo] = []

    def __repr__(self) -> str:
        return "%s(sid=%r, assessed_repos=%r)" % (
            self.__class__.__name__,
            self.sid,
            self.assessed_repos,
        )

    def add_assessed_repo(self, assessed_repo: AssessedRepo) -> None:
        self.assessed_repos.append(assessed_repo)

    @property
    def grade(self):
        return sum([r.grade_final for r in self.assessed_repos])


def check_required_fp_exists(fp_to_check: Path) -> None:
    """Check if file path exists, and if not, raise exception."""
    if not fp_to_check.exists():
        raise FileNotFoundError(f"File '{fp_to_check}' does not exist!")


def get_student_repo_fp(assess_fp: Path, student_id: str, repo_name: str) -> Path:
    """Determine the path to a student repository."""

    return assess_fp.joinpath(_FOLDER_STUDENT_REPOS_, student_id, repo_name)


def get_valid_students_git_fp(assess_fp: Path) -> Path:
    """Determine path for valid student Git URLs yaml file."""

    return cast(Path, assess_fp).joinpath(_FILE_VALID_STUDENTS_GIT_)


def get_assessed_students_fp(assess_fp: Path) -> Path:
    """Determine path for student assessments yaml file."""

    return assess_fp.joinpath(_FILE_ASSESSED_STUDENTS_)


def get_desc(func) -> str:
    """Get a short description of the assessment function."""

    desc: str | None = getdoc(func)

    if desc is not None and len(desc) > 0:
        desc = desc.split("\n")[0]
    else:
        desc = "Unavailable"

    return desc


def check_empty_args(args: Sequence[str]) -> None:
    """Check that argument list is empty, otherwise raise error."""

    if len(args) > 0:
        raise ArgumentError(None, f"Invalid arguments: {', '.join(args)}")
