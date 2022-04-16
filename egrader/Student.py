import requests
import validators

class Student:
    """A student and his repositories."""

    def __init__(self, sid, git_url):
        self.sid = sid
        self.git_url = git_url
        self.valid_url = False

        # Check if URL is well-formed
        if validators.url(git_url):
            # Check if URL exists (200)
            if requests.head(git_url).status_code < 400:
                self.valid_url = True

        self.repos = []

    def add_repo(self, repo):
        self.repos.append(repo)
