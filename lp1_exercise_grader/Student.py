from typing import List
from .Repo import Repo

class Student:
    """A student and his repositories."""

    def __init__(self, id: id, git_url: str) -> None:
        self.id: int = id
        self.git_url: str = git_url
        self.repos: List[Repo] = []

    def add_repo(self, repo: Repo):
        self.repos.append(repo)