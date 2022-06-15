from pathlib import Path
from types import MappingProxyType
from typing import Final

import requests
import validators

OPT_E_SHORT: Final[str] = "e"
OPT_E_LONG: Final[str] = "existing"
OPT_E_STOP: Final[str] = "stop"
OPT_E_UPDT: Final[str] = "update"
OPT_E_OVWR: Final[str] = "overwrite"

FILE_VALIDATED_GIT_URLS: Final[str] = "validated_git_urls.yml"
FOLDER_STUDENT_REPOS: Final[str] = "student_repos"

OUTPUT_FOLDER_DEFAULT_PREFIX: Final[str] = "out_"


class Student:
    """A student and his repositories."""

    def __init__(self, sid, git_url):
        # Set instance variables
        self.sid = sid
        self.git_url = git_url
        self.valid_url = False
        self.repos = {}

        # Validate URL if it's is well-formed and if it exists (200)
        if (
            validators.url(self.git_url)
            and requests.head(self.git_url).status_code < 400
        ):
            self.valid_url = True

    def __repr__(self):
        return "%s(sid=%r, git_url=%r, valid_url=%r, repos=%r)" % (
            self.__class__.__name__,
            self.sid,
            self.git_url,
            self.valid_url,
            self.repos,
        )

    def add_repo(self, repo_name, repo_path):
        self.repos[repo_name] = repo_path


def check_required_fp_exists(fp_to_check: Path) -> None:
    """Check if file path exists, and if not, raise exception"""
    if not fp_to_check.exists():
        raise FileNotFoundError(f"File '{fp_to_check}' does not exist!")


def get_output_fp(output_folder: str | None, rules_file: Path) -> Path:
    """Determine output path given by user or extract it from rules file name"""
    if output_folder is not None:
        return Path(output_folder)
    else:
        return Path(f"{OUTPUT_FOLDER_DEFAULT_PREFIX}{rules_file.stem}")


def get_student_repo_fp(base_fp: Path, student_id: str, repo_name: str) -> Path:
    """Determine the path to a student repository"""

    return base_fp.joinpath(FOLDER_STUDENT_REPOS, student_id, repo_name)


def get_valid_student_urls_fp(output_fp: Path):
    """Determine path for validated URLs yaml file"""

    return output_fp.joinpath(FILE_VALIDATED_GIT_URLS)
