class Student:
    """A student and his repositories."""

    def __init__(self, id, git_url):
        self.id = id
        self.git_url = git_url
        self.repos = []

    def add_repo(self, repo):
        self.repos.append(repo)