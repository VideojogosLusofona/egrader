import requests
import validators
from yaml import SafeLoader, YAMLObject


class Student(YAMLObject):
    """A student and his repositories."""

    yaml_tag = "!Student"
    yaml_loader = SafeLoader

    def __init__(self, sid, git_url):
        self.sid = sid
        self.git_url = git_url
        self.valid_url = False

    def __repr__(self):
        return "%s(sid=%r, git_url=%r, valid_url=%r)" % (
            self.__class__.__name__,
            self.sid,
            self.git_url,
            self.valid_url,
        )

    def validate(self):

        # Check if URL is well-formed
        if validators.url(self.git_url):
            # Check if URL exists (200)
            if requests.head(self.git_url).status_code < 400:
                self.valid_url = True
