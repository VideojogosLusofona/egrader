from datetime import datetime

class Commit:
    """A commit."""

    def __init__(self, sha: str, message: str, name: str, email: str, datetime: datetime) -> None:
        self.sha: str = sha
        self.message: str = message
        self.name: str = name
        self.email: str = email
        self.datetime: datetime = datetime