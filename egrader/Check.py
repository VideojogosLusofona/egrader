import requests
import validators
from yaml import SafeLoader, YAMLObject


class Check(YAMLObject):
    """Checks done in a student repository."""

    yaml_tag = "!Check"
    yaml_loader = SafeLoader

    def __init__(self, name, result, message):
        self.name = name
        self.result = result
        self.message = message

    def __repr__(self):
        return "%s(name=%r, result=%r, message=%r)" % (
            self.__class__.__name__,
            self.name,
            self.result,
            self.message,
        )
