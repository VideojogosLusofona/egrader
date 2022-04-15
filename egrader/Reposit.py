class Reposit:
    """A student repository, corresponds to a C# solution."""

    def __init__(self, name):
        self.name = name
        self.exists = False
        self.solution_exists = False
        self.commits = []
        self.projects = []

    def add_commit(self, commit):
        self.commits.append(commit)

    def add_project(self, project):
        self.projects.append(project)
