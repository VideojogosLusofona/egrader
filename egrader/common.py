from typing import Final

import requests
import validators

OPT_E_SHORT: Final[str] = "e"
OPT_E_LONG: Final[str] = "existing"
OPT_E_STOP: Final[str] = "stop"
OPT_E_UPDT: Final[str] = "update"
OPT_E_OVWR: Final[str] = "overwrite"

FILE_VALIDATED_GIT_URLS: Final[str] = "validated_git_urls.yml"
FOLDER_STUDENTS: Final[str] = "students"


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
