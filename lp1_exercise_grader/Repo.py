from typing import List
from .Commit import Commit
from .Project import Project

class Repo:
    """A student repository, corresponds to a C# solution."""

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.exists: bool = False
        self.solution_exists: bool = False
        self.commits: List[Commit] = []
        self.projects: List[Project] = []

    def add_commit(self, commit: Commit):
        self.commits.append(commit)

    def add_project(self, project: Project):
        self.projects.append(project)