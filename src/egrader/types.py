"""Classes used in egrader."""

from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urlparse

# import requests
import validators
from yarl import URL


class StudentGit:
    """A student and his Git repositories."""

    def __init__(self, sid: str, email: str, url: str) -> None:
        """Initialize an instance of this class."""
        # Set instance variables
        self.sid: str = sid
        self.email: str = email
        self._url: str = ""
        self.url_type: str | None = None
        self.repos: Dict[str, str] = {}

        # Validate partial Git URL (only local file and http/https supported)
        u = urlparse(url)
        if u.scheme in {"file", ""}:
            # It's a file URL probably, let's check if it exists and is a folder
            p = Path(u.netloc, u.path)
            if p.exists() and p.is_dir():
                self.url_type = "file"
                self._url = str(p)
        elif (
            u.scheme in {"http", "https"}  # Is it a HTTP/HTTPS URL?
            and validators.url(url)  # Is it a well-formed URL?
            # and requests.head(url).status_code < 400  # Valid net resource (200)?
        ):
            self.url_type = u.scheme
            self._url = url

    def __repr__(self) -> str:
        """String representation of this instance for YAML serialization."""
        return "%s(sid=%r, email=%r, url=%r, url_type=%r, repos=%r)" % (
            self.__class__.__name__,
            self.sid,
            self.email,
            self._url,
            self.url_type,
            self.repos,
        )

    def add_repo(self, repo_name: str, repo_path: str) -> None:
        """Add a new repository to this student instance."""
        self.repos[repo_name] = repo_path

    def repo_url(self, repo_name: str) -> str:
        """Get full repository URL given the repository name."""
        if self.valid_url:
            if self.url_type == "file":
                return str(Path(self._url, repo_name))
            elif self.url_type in {"http", "https"}:
                return str(URL(self._url) / repo_name)
        raise ValueError(f"Student {self.sid} contains invalid URL.")

    @property
    def repo_count(self) -> int:
        """Number of repositories in this student instance."""
        return len(self.repos)

    @property
    def valid_url(self) -> bool:
        """Does this student have a valid URL?"""
        return self._url != "" and self.url_type is not None


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
        """Initialize an instance of this class."""
        # Set instance variables
        self.name: str = name
        self.description: str = description
        self.parameters: Dict[str, Any] = parameters
        self.weight: float = weight
        self.grade_raw: float = grade_raw

    def __repr__(self) -> str:
        """String representation of this instance for YAML serialization."""
        return "%s(name=%r, description=%r, weight=%r, grade_raw=%r)" % (
            self.__class__.__name__,
            self.name,
            self.description,
            self.weight,
            self.grade_raw,
        )

    @property
    def grade_final(self) -> float:
        """Final grade for this assessment."""
        return self.grade_raw * self.weight


class AssessedRepo:
    """An assessed student repository."""

    def __init__(self, name: str, weight: float) -> None:
        """Initialize an instance of this class."""
        # Set instance variables
        self.name: str = name
        self.weight: float = weight
        self.assessments: List[Assessment] = []
        self.inter_assessments: List[Assessment] = []
        self.local_path: str | None = None

    def __repr__(self) -> str:
        """String representation of this instance for YAML serialization."""
        return "%s(name=%r, weight=%r, assessments=%r, inter_assessments=%r)" % (
            self.__class__.__name__,
            self.name,
            self.weight,
            self.assessments,
            self.inter_assessments,
        )

    def add_assessment(self, assessment: Assessment) -> None:
        """Add an assessment to this repository."""
        self.assessments.append(assessment)

    def add_inter_assessment(self, assessment: Assessment) -> None:
        """Add an inter-repository assessment to this repository."""
        self.inter_assessments.append(assessment)

    def is_empty(self) -> bool:
        """Does this repository have any assessments?"""
        return len(self.assessments) + len(self.inter_assessments) == 0

    @property
    def grade_final(self) -> float:
        """Final grade for this repository."""
        return self.grade_raw * self.weight

    @property
    def grade_raw(self) -> float:
        """Raw grade for this repository."""
        return sum([a.grade_final for a in self.assessments]) + sum(
            [a.grade_final for a in self.inter_assessments]
        )

    @property
    def assessment_count(self) -> int:
        """Number of assessment performed in this repository."""
        return len(self.assessments) + len(self.inter_assessments)


class AssessedStudent:
    """An assessed student."""

    def __init__(self, sid: str) -> None:
        """Initialize an instance of this class."""
        # Set instance variables
        self.sid: str = sid
        self.assessed_repos: List[AssessedRepo] = []

    def __repr__(self) -> str:
        """String representation of this instance for YAML serialization."""
        return "%s(sid=%r, assessed_repos=%r)" % (
            self.__class__.__name__,
            self.sid,
            self.assessed_repos,
        )

    def add_assessed_repo(self, assessed_repo: AssessedRepo) -> None:
        """Add an assessed repository to this student."""
        self.assessed_repos.append(assessed_repo)

    @property
    def grade(self) -> float:
        """This student's grade."""
        return sum([r.grade_final for r in self.assessed_repos])

    @property
    def assessment_count(self) -> int:
        """Number of assessments performed for this student."""
        return sum([r.assessment_count for r in self.assessed_repos])
