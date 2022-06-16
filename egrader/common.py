from pathlib import Path
from typing import Dict, Final, List

import requests
import validators

OPT_E_SHORT: Final[str] = "e"
OPT_E_LONG: Final[str] = "existing"
OPT_E_STOP: Final[str] = "stop"
OPT_E_UPDT: Final[str] = "update"
OPT_E_OVWR: Final[str] = "overwrite"

FILE_VALID_STUDENTS_GIT: Final[str] = "validated_git_urls.yml"
FILE_ASSESSED_STUDENTS: Final[str] = "assessed_students.yml"
FOLDER_STUDENT_REPOS: Final[str] = "student_repos"

OUTPUT_FOLDER_DEFAULT_PREFIX: Final[str] = "out_"


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
        self, name: str, description: str, weight: float, grade_raw: float
    ) -> None:
        # Set instance variables
        self.name: str = name
        self.description: str = description
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
        self.grade_raw: float = 0
        self.inter_repo_mod: float = 1  # Unused for now
        self.assessments: List[Assessment] = []
        self.exists = False

    def __repr__(self) -> str:
        return (
            "%s(name=%r, weight=%r, grade_raw=%r, inter_repo_mod=%r, assessments=%r)"
            % (
                self.__class__.__name__,
                self.name,
                self.weight,
                self.grade_raw,
                self.inter_repo_mod,
                self.assessments,
            )
        )

    def add_assessment(self, assessment: Assessment) -> None:
        self.exists = True
        self.assessments.append(assessment)
        self.grade_raw += assessment.grade_final

    @property
    def grade_final(self) -> float:
        return self.grade_raw * self.weight * self.inter_repo_mod


class AssessedStudent:
    """An assessed student."""

    def __init__(self, sid: str) -> None:
        # Set instance variables
        self.sid: str = sid
        self.grade: float = 0
        self.assessed_repos: List[AssessedRepo] = []

    def __repr__(self) -> str:
        return "%s(sid=%r, grade=%r, assessed_repos=%r)" % (
            self.__class__.__name__,
            self.sid,
            self.grade,
            self.assessed_repos,
        )

    def add_assessed_repo(self, assessed_repo: AssessedRepo) -> None:
        self.assessed_repos.append(assessed_repo)
        self.grade += assessed_repo.grade_final


def check_required_fp_exists(fp_to_check: Path) -> None:
    """Check if file path exists, and if not, raise exception."""
    if not fp_to_check.exists():
        raise FileNotFoundError(f"File '{fp_to_check}' does not exist!")


def get_output_fp(output_folder: str | None, rules_file: Path) -> Path:
    """Determine output path given by user or extract it from rules file name."""
    if output_folder is not None:
        return Path(output_folder)
    else:
        return Path(f"{OUTPUT_FOLDER_DEFAULT_PREFIX}{rules_file.stem}")


def get_student_repo_fp(base_fp: Path, student_id: str, repo_name: str) -> Path:
    """Determine the path to a student repository."""

    return base_fp.joinpath(FOLDER_STUDENT_REPOS, student_id, repo_name)


def get_valid_students_git_fp(output_fp: Path) -> Path:
    """Determine path for valid student Git URLs yaml file."""

    return output_fp.joinpath(FILE_VALID_STUDENTS_GIT)


def get_assessed_students_fp(output_fp: Path) -> Path:
    """Determine path for student assessments yaml file."""

    return output_fp.joinpath(FILE_ASSESSED_STUDENTS)
