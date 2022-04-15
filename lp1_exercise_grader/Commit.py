class Commit:
    """A commit."""

    def __init__(self, sha, message, name, email, datetime):
        self.sha = sha
        self.message = message
        self.name = name
        self.email = email
        self.datetime = datetime
