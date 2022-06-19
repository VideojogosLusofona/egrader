from typing import Any, Dict, List

import requests
import validators


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

    @property
    def repo_count(self) -> int:
        return len(self.repos)


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

    @property
    def assessment_count(self) -> int:
        return len(self.assessments) + len(self.inter_assessments)


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
    def grade(self) -> float:
        return sum([r.grade_final for r in self.assessed_repos])

    @property
    def assessment_count(self) -> int:
        return sum([r.assessment_count for r in self.assessed_repos])